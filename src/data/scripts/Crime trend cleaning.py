######################################################################################
####                                                                              ####  
####                             Motorbike Hotspot Data ETL                       ####
####                                                                              ####
######################################################################################

# Loading required libraries----------------------------------------------------------
import pandas as pd
from pathlib import Path

# Retrieving the current working directory---------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent


######################################################################################
####                                  Data Loading                                ####

# Loading Postcode crime data---------------------------------------------------------
# Yearly trend crime data for motor vehicle theft
trend_crime_data = pd.read_excel(f'{SCRIPT_DIR}/Source data/Data_Tables_LGA_Recorded_Offences_Year_Ending_March_2025.xlsx', sheet_name = 'Table 03')


######################################################################################
####                                Data Cleaning                                 ####

# Aggregate trend crime metrics
agg_crime_data_trend = (trend_crime_data.
    loc[lambda df: 
            (df['Offence Subgroup'] == 'B41 Motor vehicle theft') & 
            (df['Year'] >= pd.Timestamp.today().year - 4)].
    groupby(['Year', 'Postcode']).
    agg(yearly_thefts = ('Offence Count', 'sum')).
    sort_values(['Postcode', 'Year']).
    reset_index().
    rename(columns = lambda x: x.lower().replace(" ", "_"))) #Renaming columns for consistency


########################################################################################
####                                    Data Export                                 ####

# Saving cleaned crime data-------------------------------------------------------------
agg_crime_data_trend.to_csv(f'{SCRIPT_DIR}/Cleaned data/yearly_postcode_thefts.csv', index = False)

