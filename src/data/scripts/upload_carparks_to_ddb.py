#!/usr/bin/env python3
"""
Usage examples:
  python src/data/scripts/upload_carparks_to_dynamo.py --csv src/data/cleaned_carparks.csv

  # Actually write (remove dry-run)
  python scripts/upload_carparks_to_dynamo.py --apply
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from typing import Iterable, Dict

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.client import BaseClient
from pathlib import Path


def read_rows(path: str) -> Iterable[Dict[str, str]]:
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            addr = (row.get('street_address') or row.get('building_address') or '').strip()
            suburb = (row.get('suburb') or '').strip()
            postcode = str(row.get('postcode') or '').strip()
            if addr and suburb and postcode:
                yield {
                    'address': addr,
                    'suburb': suburb,
                    'postcode': postcode,
                    # Treat car parks as off-street parking for the existing type enum
                    'type': 'off-street',
                }


def ensure_counter_item(table) -> None:
    table.update_item(
        Key={'postcode': 'COUNTER', 'parking_id': 0},
        UpdateExpression='SET #c = if_not_exists(#c, :zero)',
        ExpressionAttributeNames={'#c': 'counter'},
        ExpressionAttributeValues={':zero': 0},
    )


def next_id(table) -> int:
    resp = table.update_item(
        Key={'postcode': 'COUNTER', 'parking_id': 0},
        UpdateExpression='SET #c = if_not_exists(#c, :zero) + :one',
        ExpressionAttributeNames={'#c': 'counter'},
        ExpressionAttributeValues={':zero': 0, ':one': 1},
        ReturnValues='UPDATED_NEW',
    )
    return int(resp['Attributes']['counter'])


def exists(table, item: Dict[str, str]) -> bool:
    resp = table.scan(
        ProjectionExpression='parking_id',
        FilterExpression=Attr('address').eq(item['address']) &
                         Attr('suburb').eq(item['suburb']) &
                         Attr('postcode').eq(item['postcode'])
    )
    return bool(resp.get('Items'))


def put_item(table, item: Dict[str, str]) -> int:
    pid = next_id(table)
    table.put_item(Item={
        'parking_id': pid,
        'postcode': item['postcode'],
        'address': item['address'],
        'suburb': item['suburb'],
        'type': item['type'],
        'created_at': datetime.now().isoformat(),
    })
    return pid


def main() -> None:
    ap = argparse.ArgumentParser(description='Upload car park addresses to DynamoDB (dry-run by default)')
    default_csv = str((Path(__file__).resolve().parent.parent / 'cleaned_carparks.csv'))
    ap.add_argument('--csv', default=default_csv)
    ap.add_argument('--apply', action='store_true', help='Perform writes (otherwise dry-run)')
    args = ap.parse_args()

    region = 'ap-southeast-2'
    client = boto3.client('dynamodb', region_name=region)
    table_name = 'user_contributions'
    ddb = boto3.resource('dynamodb', region_name=region)
    table = ddb.Table(table_name)

    rows = list(read_rows(args.csv))
    to_insert = []

    if args.apply:
        ensure_counter_item(table)

    for r in rows:
        if exists(table, r):
            continue
        to_insert.append(r)

    print(f"{len(to_insert)} new items detected")

    if not args.apply:
        print('Dry-run only. Use --apply to insert.')
        return

    inserted = 0
    for item in to_insert:
        put_item(table, item)
        inserted += 1

    print(f"Inserted {inserted} items into {table_name}.")


if __name__ == '__main__':
    main()
