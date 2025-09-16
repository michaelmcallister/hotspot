#!/usr/bin/env python3
import pandas as pd

# G-NAF data taken from https://data.gov.au/data/dataset/geocoded-national-address-file-g-naf/resource/d93d995d-ae32-4cac-8e30-081a18bb2173
base_path = "/Users/michaelmcallister/Downloads/g-naf_aug25_allstates_gda94_psv_1020/G-NAF/G-NAF AUGUST 2025/Standard"

# Just scoped to Victoria
addresses = pd.read_csv(f"{base_path}/VIC_ADDRESS_DETAIL_psv.psv", sep='|', low_memory=False)
streets = pd.read_csv(f"{base_path}/VIC_STREET_LOCALITY_psv.psv", sep='|', low_memory=False)
localities = pd.read_csv(f"{base_path}/VIC_LOCALITY_psv.psv", sep='|', low_memory=False)

df = addresses.merge(streets, on='STREET_LOCALITY_PID', how='left')
# After merging, LOCALITY_PID becomes LOCALITY_PID_x (from addresses) and LOCALITY_PID_y (from streets)
# We'll use LOCALITY_PID_x to match with localities
df = df.merge(localities, left_on='LOCALITY_PID_x', right_on='LOCALITY_PID', how='left')

# Build address components separately
def build_street_address(row):
    parts = []

    # Might not have a flat, check first
    if pd.notna(row['FLAT_NUMBER']):
        flat = str(int(row['FLAT_NUMBER'])) if row['FLAT_NUMBER'] == row['FLAT_NUMBER'] else str(row['FLAT_NUMBER'])
        if pd.notna(row['FLAT_TYPE_CODE']):
            parts.append(f"{row['FLAT_TYPE_CODE']} {flat}")
        else:
            parts.append(f"Unit {flat}")

    if pd.notna(row['NUMBER_FIRST']):
        num = str(int(row['NUMBER_FIRST'])) if row['NUMBER_FIRST'] == row['NUMBER_FIRST'] else str(row['NUMBER_FIRST'])
        if pd.notna(row['NUMBER_LAST']):
            num_last = str(int(row['NUMBER_LAST'])) if row['NUMBER_LAST'] == row['NUMBER_LAST'] else str(row['NUMBER_LAST'])
            num = f"{num}-{num_last}"
        parts.append(num)

    if pd.notna(row['STREET_NAME']):
        street = row['STREET_NAME']
        if pd.notna(row['STREET_TYPE_CODE']):
            street += f" {row['STREET_TYPE_CODE']}"
        parts.append(street)

    return ' '.join(parts) if parts else ''

print("Building addresses...")
df['ADDRESS'] = df.apply(build_street_address, axis=1)
df['SUBURB'] = df['LOCALITY_NAME'].fillna('')
df['POSTCODE'] = df['POSTCODE'].apply(lambda x: str(int(x)) if pd.notna(x) else '')

result = df[['ADDRESS', 'SUBURB', 'POSTCODE']].copy()
result = result[(result['ADDRESS'] != '') & (result['SUBURB'] != '') & (result['POSTCODE'] != '')]
result = result.drop_duplicates().sort_values(['SUBURB', 'ADDRESS'])

output_file = '../victorian_addresses.csv'
print(f"Saving {len(result)} addresses to {output_file}...")
result.to_csv(output_file, index=False)
