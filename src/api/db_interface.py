from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import sqlite3
import uuid


class DatabaseInterface(ABC):
    @abstractmethod
    def fetch_all(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def execute(self, query: str, params: Dict[str, Any] = None) -> int:
        pass

    @abstractmethod
    def get_addresses_by_postcode(self, postcode: str, query: Optional[str] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def verify_address(self, address: str, suburb: str, postcode: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def insert_parking_contribution(self, data: Dict[str, Any]) -> int:
        pass

    @abstractmethod
    def upsert_parking_contribution(self, data: Dict[str, Any], facilities: List[int] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def insert_parking_facility(self, parking_id: int, facility_id: int):
        pass

    @abstractmethod
    def get_parking_by_postcode(self, postcode: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_facilities_for_parking(self, parking_id: int) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_parking_submissions_count(self) -> int:
        pass


class SQLiteDatabase(DatabaseInterface):
    def __init__(self, db_path: str):
        import sqlite3
        self.db_path = db_path

    def fetch_all(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or {})
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def execute(self, query: str, params: Dict[str, Any] = None) -> int:
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or {})
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def get_addresses_by_postcode(self, postcode: str, query: Optional[str] = None) -> List[Dict[str, Any]]:
        if query:
            return self.fetch_all("""
                SELECT address, suburb, postcode
                FROM victorian_addresses
                WHERE postcode = :postcode
                  AND LOWER(address) LIKE '%' || LOWER(:query) || '%'
                ORDER BY address
                LIMIT 20
            """, {"postcode": postcode, "query": query})
        else:
            return self.fetch_all("""
                SELECT address, suburb, postcode
                FROM victorian_addresses
                WHERE postcode = :postcode
                ORDER BY address
                LIMIT 20
            """, {"postcode": postcode})

    def verify_address(self, address: str, suburb: str, postcode: str) -> Optional[Dict[str, Any]]:
        results = self.fetch_all("""
            SELECT address, suburb, postcode
            FROM victorian_addresses
            WHERE UPPER(address) = UPPER(:address)
              AND UPPER(suburb) = UPPER(:suburb)
              AND postcode = :postcode
        """, {
            "address": address,
            "suburb": suburb,
            "postcode": postcode
        })
        return results[0] if results else None

    def insert_parking_contribution(self, data: Dict[str, Any]) -> int:
        return self.execute("""
            INSERT INTO user_contribution (address, suburb, postcode, type, lighting, cctv)
            VALUES (:address, :suburb, :postcode, :type, :lighting, :cctv)
        """, data)

    def upsert_parking_contribution(self, data: Dict[str, Any], facilities: List[int] = None) -> Dict[str, Any]:
        facilities = facilities or []

        existing = self.fetch_all("""
            SELECT parking_id, type, lighting, cctv
            FROM user_contribution
            WHERE address = :address AND suburb = :suburb AND postcode = :postcode
        """, {
            "address": data["address"],
            "suburb": data["suburb"],
            "postcode": data["postcode"]
        })

        if not existing:
            parking_id = self.insert_parking_contribution(data)

            for facility_id in facilities:
                self.insert_parking_facility(parking_id, facility_id)

            return {"parking_id": parking_id, "action": "inserted"}

        existing_record = existing[0]
        parking_id = existing_record["parking_id"]

        needs_update = (
            existing_record["type"] != data["type"] or
            existing_record["lighting"] != data.get("lighting") or
            existing_record["cctv"] != data.get("cctv")
        )

        existing_facilities = self.get_facilities_for_parking(parking_id)
        existing_facility_ids = {f["facility_id"] for f in existing_facilities}
        new_facility_ids = set(facilities)

        facilities_changed = existing_facility_ids != new_facility_ids

        if needs_update:
            self.execute("""
                UPDATE user_contribution
                SET type = :type, lighting = :lighting, cctv = :cctv, created_at = CURRENT_TIMESTAMP
                WHERE parking_id = :parking_id
            """, {
                **data,
                "parking_id": parking_id
            })
            action = "updated"
        else:
            action = "no_change"

        if facilities_changed:
            self.execute("""
                DELETE FROM user_contribution_facilities WHERE parking_id = :parking_id
            """, {"parking_id": parking_id})

            for facility_id in facilities:
                self.insert_parking_facility(parking_id, facility_id)

            if action == "no_change":
                action = "updated"

        return {"parking_id": parking_id, "action": action}

    def insert_parking_facility(self, parking_id: int, facility_id: int):
        self.execute("""
            INSERT INTO user_contribution_facilities (parking_id, facility_id)
            VALUES (:parking_id, :facility_id)
        """, {
            "parking_id": parking_id,
            "facility_id": facility_id
        })

    def get_parking_by_postcode(self, postcode: str) -> List[Dict[str, Any]]:
        return self.fetch_all("""
            SELECT parking_id, address, suburb, postcode, type, lighting, cctv, created_at
            FROM user_contribution
            WHERE postcode = :postcode
            ORDER BY created_at DESC
            LIMIT 20
        """, {"postcode": postcode})

    def get_facilities_for_parking(self, parking_id: int) -> List[Dict[str, Any]]:
        return self.fetch_all("""
            SELECT f.facility_id, f.facility_name
            FROM user_contribution_facilities ucf
            JOIN facilities f ON ucf.facility_id = f.facility_id
            WHERE ucf.parking_id = :parking_id
        """, {"parking_id": parking_id})

    def get_parking_submissions_count(self) -> int:
        result = self.fetch_all("""
            SELECT COUNT(*) as count
            FROM user_contribution
        """)
        return result[0]['count'] if result else 0


class PersistentDatabase(DatabaseInterface):
    """
    Production database that uses DynamoDB for user_contributions and SQLite for addresses/facilities. The latter is rebuilt after every deployment.
    """
    def __init__(self, db_path: str = None, table_name: str = None, region: str = None):
        import boto3

        self.db_path = db_path or os.environ.get('SQLITE_DB_PATH', '../data/hotspot.db')

        self.region = region or os.environ.get('AWS_DEFAULT_REGION', 'ap-southeast-2')
        self.table_name = table_name or os.environ.get('DYNAMODB_TABLE', 'user_contributions')

        self.dynamodb = boto3.resource('dynamodb', region_name=self.region)
        self.table = self.dynamodb.Table(self.table_name)

    def _sqlite_fetch_all(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or {})
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def _sqlite_execute(self, query: str, params: Dict[str, Any] = None) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or {})
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def fetch_all(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        return self._sqlite_fetch_all(query, params)

    def execute(self, query: str, params: Dict[str, Any] = None) -> int:
        return self._sqlite_execute(query, params)

    def get_addresses_by_postcode(self, postcode: str, query: Optional[str] = None) -> List[Dict[str, Any]]:
        if query:
            return self._sqlite_fetch_all("""
                SELECT address, suburb, postcode
                FROM victorian_addresses
                WHERE postcode = :postcode
                  AND LOWER(address) LIKE '%' || LOWER(:query) || '%'
                ORDER BY address
                LIMIT 20
            """, {"postcode": postcode, "query": query})
        else:
            return self._sqlite_fetch_all("""
                SELECT address, suburb, postcode
                FROM victorian_addresses
                WHERE postcode = :postcode
                ORDER BY address
                LIMIT 20
            """, {"postcode": postcode})

    def verify_address(self, address: str, suburb: str, postcode: str) -> Optional[Dict[str, Any]]:
        results = self._sqlite_fetch_all("""
            SELECT address, suburb, postcode
            FROM victorian_addresses
            WHERE UPPER(address) = UPPER(:address)
              AND UPPER(suburb) = UPPER(:suburb)
              AND postcode = :postcode
        """, {
            "address": address,
            "suburb": suburb,
            "postcode": postcode
        })
        return results[0] if results else None

    def insert_parking_contribution(self, data: Dict[str, Any]) -> int:
        from datetime import datetime

        # Matches the sqllite implementation by auto-incrementing the ID
        counter_response = self.table.update_item(
            Key={'postcode': 'COUNTER', 'parking_id': 0},
            UpdateExpression='SET #counter = if_not_exists(#counter, :zero) + :inc',
            ExpressionAttributeNames={'#counter': 'counter'},
            ExpressionAttributeValues={':zero': 0, ':inc': 1},
            ReturnValues='UPDATED_NEW'
        )

        parking_id = int(counter_response['Attributes']['counter'])

        item = {
            'parking_id': parking_id,
            'postcode': data['postcode'],
            'address': data['address'],
            'suburb': data['suburb'],
            'type': data['type'],
            'created_at': datetime.now().isoformat()
        }

        if data.get('lighting') is not None:
            item['lighting'] = data['lighting']
        if data.get('cctv') is not None:
            item['cctv'] = data['cctv']


        self.table.put_item(Item=item)

        return parking_id

    def upsert_parking_contribution(self, data: Dict[str, Any], facilities: List[int] = None) -> Dict[str, Any]:
        from boto3.dynamodb.conditions import Attr
        facilities = facilities or []

        response = self.table.scan(
            FilterExpression=Attr('address').eq(data['address']) &
                           Attr('suburb').eq(data['suburb']) &
                           Attr('postcode').eq(data['postcode'])
        )

        if not response['Items']:
            parking_id = self.insert_parking_contribution(data)

            if facilities:
                self.table.update_item(
                    Key={
                        'postcode': data['postcode'],
                        'parking_id': parking_id
                    },
                    UpdateExpression='SET facility_ids = :facilities',
                    ExpressionAttributeValues={
                        ':facilities': facilities
                    }
                )

            return {"parking_id": parking_id, "action": "inserted"}

        existing_item = response['Items'][0]
        parking_id = int(existing_item['parking_id'])

        needs_update = (
            existing_item.get('type') != data['type'] or
            existing_item.get('lighting') != data.get('lighting') or
            existing_item.get('cctv') != data.get('cctv')
        )

        existing_facilities = set(existing_item.get('facility_ids', []))
        new_facilities = set(facilities)
        facilities_changed = existing_facilities != new_facilities

        if needs_update or facilities_changed:
            update_expression = 'SET #type = :type'
            expression_attribute_names = {'#type': 'type'}
            expression_attribute_values = {':type': data['type']}

            if data.get('lighting') is not None:
                update_expression += ', lighting = :lighting'
                expression_attribute_values[':lighting'] = data['lighting']

            if data.get('cctv') is not None:
                update_expression += ', cctv = :cctv'
                expression_attribute_values[':cctv'] = data['cctv']

            if facilities_changed:
                update_expression += ', facility_ids = :facilities'
                expression_attribute_values[':facilities'] = facilities

            update_expression += ', created_at = :created_at'
            expression_attribute_values[':created_at'] = datetime.now().isoformat()

            self.table.update_item(
                Key={
                    'postcode': data['postcode'],
                    'parking_id': parking_id
                },
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values
            )

            return {"parking_id": parking_id, "action": "updated"}

        return {"parking_id": parking_id, "action": "no_change"}

    def insert_parking_facility(self, parking_id: int, facility_id: int):
        from boto3.dynamodb.conditions import Key, Attr

        response = self.table.scan(
            FilterExpression=Attr('parking_id').eq(parking_id)
        )

        if response['Items']:
            item = response['Items'][0]
            postcode = item['postcode']

            facilities = item.get('facility_ids', [])
            if facility_id not in facilities:
                facilities.append(facility_id)

            self.table.update_item(
                Key={
                    'postcode': postcode,
                    'parking_id': parking_id
                },
                UpdateExpression='SET facility_ids = :facilities',
                ExpressionAttributeValues={
                    ':facilities': facilities
                }
            )

    def get_parking_by_postcode(self, postcode: str) -> List[Dict[str, Any]]:
        from boto3.dynamodb.conditions import Key

        response = self.table.query(
            KeyConditionExpression=Key('postcode').eq(postcode),
            ScanIndexForward=False,
            Limit=20
        )

        items = response.get('Items', [])

        for item in items:
            if 'parking_id' in item:
                item['parking_id'] = int(item['parking_id'])
            if 'lighting' in item:
                item['lighting'] = int(item['lighting'])

        items.sort(key=lambda x: x.get('created_at', x.get('parking_id', 0)), reverse=True)

        return items[:20]

    def get_facilities_for_parking(self, parking_id: int) -> List[Dict[str, Any]]:
        from boto3.dynamodb.conditions import Attr

        response = self.table.scan(
            FilterExpression=Attr('parking_id').eq(parking_id)
        )

        if not response['Items']:
            return []

        item = response['Items'][0]
        facility_ids = item.get('facility_ids', [])

        if not facility_ids:
            return []

        facilities_list = []
        for fid in facility_ids:
            facilities = self._sqlite_fetch_all("""
                SELECT facility_id, facility_name
                FROM facilities
                WHERE facility_id = :facility_id
            """, {"facility_id": int(fid)})

            if facilities:
                facilities_list.append(facilities[0])

        return facilities_list

    def get_parking_submissions_count(self) -> int:
        try:
            resp = self.table.get_item(
                Key={"postcode": "COUNTER", "parking_id": 0},
                ConsistentRead=True,
                ProjectionExpression="#c",
                ExpressionAttributeNames={"#c": "counter"}
            )
            counter = resp.get("Item", {}).get("counter")
            if isinstance(counter, (int, float)):
                return int(counter)
        except Exception:
            pass

        try:
            response = self.dynamodb.meta.client.describe_table(TableName=self.table_name)
            return int(response.get("Table", {}).get("ItemCount", 0))
        except Exception:
            return 0

def get_database() -> DatabaseInterface:
    """Factory function to get the appropriate database implementation based on environment"""
    env = os.environ.get('ENVIRONMENT', 'development')
    from pathlib import Path

    db_path = os.environ.get('SQLITE_DB_PATH', '../data/hotspot.db')
    db_path = Path(db_path).resolve()
    if env == 'production':
        return PersistentDatabase(str(db_path))
    else:
        return SQLiteDatabase(str(db_path))
