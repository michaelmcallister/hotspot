######################################################################################
####                                                                              ####  
####                             Motorbike Hotspot Data ETL                       ####
####                                                                              ####
######################################################################################

# Loading required libraries----------------------------------------------------------
import pandas as pd
import numpy as np
from pathlib import Path

# Retrieving the current working directory---------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent


######################################################################################
####                                  Data Loading                                ####

# Loading Postcode datasets-----------------------------------------------------------
# Postcode data - https://www.matthewproctor.com/Content/postcodes/australian_postcodes.xlsx
postcode_data = pd.read_excel(f'{SCRIPT_DIR}/Source data/australian_postcodes.xlsx')

# Postcode crime incidents - https://files.crimestatistics.vic.gov.au/2025-06/Data_Tables_LGA_Criminal_Incidents_Year_Ending_March_2025.xlsx
postcode_crime_incidents = pd.read_excel(f'{SCRIPT_DIR}/Source data/Data_Tables_LGA_Criminal_Incidents_Year_Ending_March_2025.xlsx', sheet_name = 'Table 03')

# Postcode recorded offences - https://files.crimestatistics.vic.gov.au/2025-06/Data_Tables_LGA_Recorded_Offences_Year_Ending_March_2025.xlsx
postcode_recorded_offences = pd.read_excel(f'{SCRIPT_DIR}/Source data/Data_Tables_LGA_Recorded_Offences_Year_Ending_March_2025.xlsx', sheet_name = 'Table 03')

# Loading verified victorian postcode latitude and longitude data
postcode_area = pd.read_csv(f'{SCRIPT_DIR}/Source data/vic_postcodes_area.csv')

# Loading cleaned car park data
postcode_carparks = pd.read_csv(f'{SCRIPT_DIR}/Source data/cleaned_carparks.csv')

# Loading cleaned street light data
postcode_lights = pd.read_csv(f'{SCRIPT_DIR}/Source data/cleaned_lights.csv')


######################################################################################
####                                Data Cleaning                                 ####

# Functions---------------------------------------------------------------------------
# Creating a function to calculate the Haversine distance between two points
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000.0 # Earth radius in meters
    lat1 = np.radians(lat1.astype(float))
    lon1 = np.radians(lon1.astype(float))
    lat2 = np.radians(lat2.astype(float))
    lon2 = np.radians(lon2.astype(float))

    # Latitude and longitude differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance

# Cleaning postcode data--------------------------------------------------------------
# Cleaning the postcode data so each row is a distinct postcode using the verified latitude and longitude data from 'postcode_area'
postcode_clean = (postcode_data.
    loc[lambda df: df["State"] == "VIC"]. #Filtering to Victorian postcodes
    rename(columns = {"Lat": "ref_lat", "Long": "ref_long", "Postcode": "postcode"}). #Renaming columns for clarity and joining consistency
    merge(postcode_area, on = 'postcode', how = 'inner'). #Joining in the verified lat/long data
    assign(ref_distance = lambda df: haversine_distance(df['lat'], df['long'], df['ref_lat'], df['ref_long']), #Calculating the distance between the lat/long in the postcode data and the verified lat/long
           lga_count = lambda df: df.groupby(['postcode', 'LGA Region'])['LGA Region'].transform('size'), #LGAs by postcode
           locality_count = lambda df: df.groupby(['postcode', 'Locality'])['Locality'].transform('size')). #Locality counts by postcode
    sort_values(['postcode', 'ref_distance', 'lga_count', 'locality_count', 'ID'], ascending = [True, True, False, False, True]). #Sorting by postcode, distance from verified lat/long, LGA count, locality count and ID as a tiebreaker to select the row with the smallest distance from the verified lat/long
    groupby('postcode'). #Grouping by postcode to get unique values
    head(1). #Selecting the row with the smallest distance from the verified lat/long
    reset_index(drop = True). #Ungrouping the dataframe
    drop(columns = ['ID', 'ref_distance', 'ref_lat', 'ref_long', 'SA3 CODE 2021', 'SA3 NAME 2021', #Removing unneeded or duplicate columns
                    'SA4 CODE 2021', 'SA4 NAME 2021', 'RA 2011', 'RA 2016', 'MMM 2015', "Lat (Google)", "Long (Google)",
                    'lga_count', 'locality_count']).
    rename(columns = lambda x: x.lower().replace(" ", "_"))) #Renaming columns for consistency

# Cleaning postcode crime incidents data------------------------------------------------
# Cleaning the postcode crime incidents data to only include theft subgroups for melbourne postcodes
postcode_crime_incidents_clean = (postcode_crime_incidents.
    rename(columns = {"Postcode": "postcode"}).
    merge(postcode_area[['postcode']], on = 'postcode', how = 'inner'). #Joining in the cleaned postcode data to filter to Victorian postcodes
    loc[lambda df: 
            (df['Year'] == pd.Timestamp.today().year) & #Filtering to the current year
            (df['Offence Subgroup'].isin([ #Selecting theft related offence subgroups
                'A51 Aggravated robbery', 'A52 Non-Aggravated robbery', 'B41 Motor vehicle theft', 'B42 Steal from a motor vehicle',
                'B311 Residential aggravated burglary', 'B312 Non-residential aggravated burglary', 'B319 Unknown aggravated burglary',
                'B321 Residential non-aggravated burglary', 'B322 Non-residential non-aggravated burglary', 'B329 Unknown non-aggravated burglary',
                'B43 Steal from a retail store', 'B44 Theft of a bicycle', 'B49 Other theft']))].
    groupby(['Year', 'postcode', 'Offence Division', 'Offence Subdivision', 'Offence Subgroup']).
    agg(incident_count = ('Incidents Recorded','sum')). # Consolidating incidents recorded by postcode and offence subgroup
    reset_index().
    rename(columns = lambda x: x.lower().replace(" ", "_"))) #Renaming columns for consistency

# Cleaning postcode recorded offences data------------------------------------------------ USE THIS ONE
# Cleaning the postcode recorded offences data to only include theft subgroups for melbourne postcodes
postcode_recorded_offences_clean = (postcode_recorded_offences.
    rename(columns = {"Postcode": "postcode"}).
    merge(postcode_area[['postcode']], on = 'postcode', how = 'inner'). #Joining in the cleaned postcode data to filter to Victorian postcodes
    loc[lambda df: 
            (df['Year'] == pd.Timestamp.today().year) & #Filtering to the current year
            (df['Offence Subgroup'].isin([ #Selecting theft related offence subgroups
                'A51 Aggravated robbery', 'A52 Non-Aggravated robbery', 'B41 Motor vehicle theft', 'B42 Steal from a motor vehicle',
                'B311 Residential aggravated burglary', 'B312 Non-residential aggravated burglary', 'B319 Unknown aggravated burglary',
                'B321 Residential non-aggravated burglary', 'B322 Non-residential non-aggravated burglary', 'B329 Unknown non-aggravated burglary',
                'B43 Steal from a retail store', 'B44 Theft of a bicycle', 'B49 Other theft']))].
    groupby(['postcode', 'Offence Division', 'Offence Subdivision', 'Offence Subgroup']).
    agg(offence_count = ('Offence Count','sum')). # Consolidating incidents recorded by postcode and offence subgroup
    reset_index().
    rename(columns = lambda x: x.lower().replace(" ", "_"))) #Renaming columns for consistency

# Combining the cleaned crime incidents and recorded offences data----------------------
postcode_crime_data_clean = (postcode_crime_incidents_clean.
    merge(postcode_recorded_offences_clean, on = ['postcode', 'offence_division', 'offence_subdivision', 'offence_subgroup'], how = 'outer'). #Merging the two datasets together with a full join to retain all data
    assign(**{col: lambda df, col = col: df[col].fillna(0) for col in ["incident_count", "offence_count"]})) #Cleaning NA values to be 0 instead of NA if any missing data is present

# Creating counts of secure parking for each postcode-----------------------------------
# Creating a dataframe with the overall postcode car park counts
postcode_carpark_counts = (postcode_carparks.
    groupby('postcode').
    agg(carpark_count = ('parking_spaces', 'sum')). #Counting the number of secure (already filtered in prior cleaning) carparks in each postcode
    reset_index().
    rename(columns = lambda x: x.lower().replace(" ", "_"))) #Renaming columns for consistency

# Creating counts of street lights for each postcode------------------------------------
# Creating a dataframe with the overall postcode street light counts
postcode_light_coverage = (postcode_lights.
    rename(columns = {'POSTCODE':'postcode'}).
    merge(postcode_area, on = 'postcode', how = 'inner'). #Joining in the cleaned postcode data to get km2
    groupby(['postcode', 'area_km2']).
    agg(light_count = ('label', 'count')). #Counting the number of lights in each postcode
    reset_index().
    assign(lights_per_km2 = lambda df: (df['light_count'] / df['area_km2']).round(2)). #Calculating the number of lights per km2 in each postcode
    rename(columns = lambda x: x.lower().replace(" ", "_"))) #Renaming columns for consistency


########################################################################################
####                                    Data Export                                 ####

# Saving cleaned postcode geo data------------------------------------------------------
postcode_clean.to_csv(f'{SCRIPT_DIR}/Cleaned data/cleaned_postcode_data.csv', index = False)

# Saving cleaned postcode crime data----------------------------------------------------
postcode_recorded_offences_clean.to_csv(f'{SCRIPT_DIR}/Cleaned data/cleaned_postcode_crime_data.csv', index = False) #Went with recorded offences data as it is more comprehensive and incidents are not needed

# Saving cleaned postcode car park data-------------------------------------------------
postcode_carpark_counts.to_csv(f'{SCRIPT_DIR}/Cleaned data/cleaned_postcode_carpark_data.csv', index = False)

# Saving cleaned postcode street light coverage-----------------------------------------
postcode_light_coverage.to_csv(f'{SCRIPT_DIR}/Cleaned data/cleaned_postcode_streetlight_data.csv', index = False)
