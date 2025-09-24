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
# Loading verified victorian postcode latitude and longitude data
postcode_area = pd.read_csv(f'{SCRIPT_DIR}/Source data/vic_postcodes_area.csv').drop(columns = ['area_km2'])


######################################################################################
####                                Data Wrangling                                ####

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

# Calculating the distance between postcodes data--------------------------------------
postcode_distance = (postcode_area.
    rename(columns = lambda x: f'primary_{x}' ).
    merge(postcode_area.rename(columns = lambda x: f'secondary_{x}'), how = 'cross'). #Creating a cross join to get all combinations of postcodes
    loc[lambda df: df["primary_postcode"] != df["secondary_postcode"]]. #Removing rows where the primary and secondary postcodes are the same
    assign(distance_meters = lambda df: haversine_distance(df['primary_lat'], df['primary_long'], df['secondary_lat'], df['secondary_long']).round(2)). #Calculating the distance between the primary and secondary postcodes
    sort_values(['primary_postcode', 'distance_meters']).
    drop(columns = ['primary_lat', 'primary_long', 'secondary_lat', 'secondary_long']))


########################################################################################
####                                    Data Export                                 ####

# Saving postcode distance data---------------------------------------------------------
postcode_distance.to_csv(f'{SCRIPT_DIR}/Cleaned data/postcode_distances.csv', index = False)
