#!/usr/bin/env python
# coding: utf-8

# # Data Wrangling and Cleansing for Motorcycle Hotspot
# 
# The data wrangling for this task involved cleasning and joining multiple data sets, along with a variety of transformations.
# 
# As always the data wrangling process is iterative and exploratory. As such only the iterationa and transformations that were used in the final product are shown here.

# ### Modules

# In[1]:


import pandas as pd
import re
from thefuzz import fuzz, process
import geopandas as gpd


# ### Datasets

# In[2]:


# https://opendata.transport.vic.gov.au/dataset/victorian-integrated-survey-of-travel-and-activity-vista/resource/6b8ec11b-a94d-465a-93ae-a3c514ff84bc
vista = pd.read_csv('vista.csv')
# https://opendata.transport.vic.gov.au/dataset/174fbf40-bef0-434a-8af0-891c7f3d2323/resource/539ca066-f4d2-4e59-b61a-899970a353c6/download/household_vista_2023_2024.csv
home = pd.read_csv('home_id.csv')
# Postcode datatset found by other teammamtes
postcode = pd.read_csv('postcode.csv')
# https://www.kaggle.com/api/v1/datasets/download/emmanuelfwerr/motorcycle-technical-specifications-19702022?dataset_version_number=7...
bikes = pd.read_csv("all_bikez_curated.csv")

stolen = pd.read_csv("vehicle_thefts.csv", index_col = "_id")
# https://www.crimestatistics.vic.gov.au/crime-statistics/latest-victorian-crime-data/download-data
charged = pd.read_excel('Data_Tables_LGA_Criminal_Incidents_Year_Ending_March_2025.xlsx', sheet_name="Table 05")
LGA = pd.read_excel('Data_Tables_LGA_Criminal_Incidents_Year_Ending_March_2025.xlsx', sheet_name="Table 02")


# In[3]:


vista.head()


# In[4]:


home.head()


# In[5]:


postcode.head()


# In[6]:


bikes.head()


# In[7]:


stolen.head()


# In[8]:


charged.head()


# ## Extracting Information from vista.
# 
# Vista was able to give us data about proportions of people in each LGA who ride. The purpose of this is that crime data doesn't specify type of vehicle stolen. So by caluclating the proprtion of riders to drivers in each LGA we can approximate what proprotion of vehicle thefts in each LGA would be bikes as opposed to cars.
# 
# The process involved joining Vista with home and postcode.

# In[9]:


total = len(vista)
riders = vista[vista["mbikelicence"] == "Yes"]
rider = len(riders)
proportion = rider/total
print(f"Riders make up {rider} out of {total} total drivers, which is a proportion of {proportion}.")


# Vista has anonymous household data. Home is a similar dataset that shows all of the home id numbers and the LGA that they're from.

# In[10]:


home_subset = home[["hhid", "homelga"]]
merged_inner = pd.merge(vista, home_subset, on="hhid", how="inner")
merged_inner.head()


# I used an inner join which will automatically drop the rows that don't match, but we now have a list of people and their LGA.

# In[11]:


# Numerator: count where mbikelicence == "Yes"
num = merged_inner[merged_inner["mbikelicence"] == "Yes"].groupby(["homelga"]).size()

# Denominator: count where carlicence == "Full Licence"
den = merged_inner[merged_inner["carlicence"].isin(["Full Licence", "Green Probationary Licence", "Red Probationary Licence"])].groupby(["homelga"]).size()


# In[12]:


result = pd.DataFrame({
    "num": num,
    "den": den
})


# In[13]:


result["proportion"] = result["num"] / result["den"]


# In[14]:


result = result.reset_index()
print(result)


# The next step is to change the Nan to the mean value, and change the LGA to only include the word, not the district ion parenthesis.

# In[15]:


mean_val = result["proportion"].mean(skipna=True)
result["proportion"] = result["proportion"].fillna(mean_val)
result["homelga"] = result["homelga"].str.replace(r"\s+\(.*\)", "", regex=True)

print(result)


# In[16]:


result_subset = result[["homelga", "proportion"]]
result_subset.head()


# In[17]:


postcode.head()


# In[18]:


postcode.state.unique()


# During the exploratory process I doscvered that Moreland had been changed to Merri-bek so i needed to change that on the pd. Some LGAs also Listed "Vic." in the row, so I removed that.

# In[19]:


VIC = postcode[postcode["state"] == "VIC"]
VIC.loc[VIC["lgaregion"] == "Moreland", "lgaregion"] = "Merri-bek"
VIC["lgaregion"] = VIC["lgaregion"].str.replace(r"\s+\(Vic\.\)", "", regex=True)

VIC.head()


# In[20]:


VIC.info()


# In[21]:


VIC['lgaregion'].unique()


# In[22]:


VIC.type.count


# In[23]:


# Remove redundant columns
VIC_subset = VIC[["postcode", "locality","type",  "long", "lat", "lgaregion"]]
VIC_subset.head()
VIC_subset.to_csv('vic_postcode.csv', index=False)


# At this point I'm taking start merging postcode information with crime information.

# In[24]:


LGA.head()


# In[25]:


# Filter for motor vehicle thefts
LGA_B41 = LGA[LGA['Offence Subgroup'] == "B41 Motor vehicle theft"]
LGA_B41.head()


# In[26]:


LGA_merged = pd.merge(LGA_B41, result_subset, left_on="Local Government Area", right_on="homelga", how="left")
LGA_merged.head()


# In[27]:


LGA_merged["proportion"] = LGA_merged["proportion"].fillna(mean_val)
LGA_merged.head()


# In[28]:


#Proportion is the approximate proortion of riders to drivers in that LGA
LGA_thefts = LGA_merged[["Local Government Area", "Incidents Recorded", "LGA Rate per 100,000 population", "proportion"]]
LGA_thefts.head()


# In[29]:


LGA_thefts["Motorcycle Theft Rate"] = LGA_thefts["LGA Rate per 100,000 population"] * LGA_thefts["proportion"]
LGA_thefts.head()


# In[30]:


#Now I merge my postcode information into the crime data.
vic_merged= pd.merge(VIC_subset, LGA_thefts[["Local Government Area", "Motorcycle Theft Rate"]], left_on="lgaregion",
                    right_on="Local Government Area", how="left")
vic_merged.head()


# In[31]:


vic_merged.info()


# In[32]:


vic_merged.isna().sum()


# In[33]:


vic_merged.type.unique()


# In[34]:


# Some EDA shows that Delivery Area is the only type of postcode that we need.
vic_merged.drop(vic_merged[vic_merged['type'] != "Delivery Area"].index, inplace=True)
vic_merged[vic_merged.isna().any(axis=1)]


# In[35]:


mean_motorcycle = vic_merged["Motorcycle Theft Rate"].mean(skipna=True)


# In[36]:


merged_filtered = vic_merged[vic_merged["Motorcycle Theft Rate"].isna()]
merged_filtered


# In[37]:


# I wanted to view all the rows so that I could see where the null values were and tryi to manage them
pd.set_option("display.max_rows", None)  # show all rows
display(merged_filtered)   


# In[38]:


pd.reset_option("display.max_rows")
vic_merged["Motorcycle Theft Rate"] = vic_merged["Motorcycle Theft Rate"].fillna(mean_motorcycle)
vic_merged.isna().sum()
vic_merged.head()


# In[39]:


#Now that we have filtered to only one type we no longer need type column.
vic_merged.drop(columns=["type"], inplace=True)
vic_merged.head()


# In[40]:


#Save file
vic_merged.to_csv('cleaned_rate.csv', index = False)


# In[41]:


vic_merged = vic_merged.drop_duplicates(subset=["postcode", "locality"], keep="first")
vic_merged.head()


# In[42]:


len(vic_merged)


# In[43]:


def normalize_column(df, col, epsilon=1e-6):
    """
    Normalize a DataFrame column to (epsilon, 1 - epsilon) using min-max scaling.
    Avoids exact 0 or 1 values.
    """
    min_val = df[col].min()
    max_val = df[col].max()
    norm = (df[col] - min_val) / (max_val - min_val)  # standard [0,1]

    # Rescale to (epsilon, 1 - epsilon)
    norm = norm * (1 - 2*epsilon) + epsilon
    return norm



# In[44]:


vic_merged["postcode_risk"] = normalize_column(vic_merged, "Motorcycle Theft Rate")
vic_merged.head()


# In[45]:


pcode_default_risk = vic_merged["postcode_risk"].mean()
print(pcode_default_risk)


# In[46]:


# Taken from other notebook
model_default_risk = 0.035548815012942186


# In[47]:


default_risk = pd.DataFrame({
    "model_default_risk": [model_default_risk],
    "postcode_default_risk": [pcode_default_risk]
})

default_risk.head()


# In[48]:


default_risk.to_csv('default_risk.csv', index=False)


# In[49]:


#Start working on Charged...


# In[50]:


charged.head()


# In[51]:


charged25 = charged[charged['Year'] == 2025]
a = len(charged)
b = len(charged25)

print(f"we have retained {b} out of {a} total rows")


# In[52]:


# Sum per LGA
sum_df = charged25.groupby("Local Government Area")["Incidents Recorded"].sum().reset_index(name="Total")

# Last entry per LGA (by row order)
last_df = charged25.groupby("Local Government Area")["Incidents Recorded"].last().reset_index(name="Unsolved")

# Last entry per LGA (by row order)
first_df = charged25.groupby("Local Government Area")["Incidents Recorded"].first().reset_index(name="Charges Laid")

# Merge
charged_agg = pd.merge(sum_df, last_df, on="Local Government Area")
charged_agg = pd.merge(charged_agg, first_df, on="Local Government Area")
charged_agg["Unsolved Proportion"] = charged_agg["Unsolved"] / charged_agg["Total"]
charged_agg["Charged Proportion"] = charged_agg["Charges Laid"] / charged_agg["Total"]
charged_agg["No Charges Proportion"] = 1 - (charged_agg["Unsolved Proportion"] + charged_agg["Charged Proportion"])


charged_agg.head()


# In[53]:


default_unsolved = charged_agg["Unsolved Proportion"].mean()
default_charged = charged_agg["Charged Proportion"].mean()
default_no_charges = charged_agg["No Charges Proportion"].mean()
print(f"Mean Unsolved: {default_unsolved}, Mean Charged: {default_charged}, Mean No Charges: {default_no_charges}" )


# In[54]:


#charged_agg.to_csv('LGA_charges.csv', index=False)


# In[56]:


carparks = pd.read_csv('carparks.csv')
carparks.head()


# In[57]:


len(carparks)


# In[58]:


carparks.census_year.unique().max()


# In[59]:


carparks_current = carparks[carparks['census_year'] == 2023]
len(carparks_current)


# In[60]:


carparks_current.parking_type.unique()


# In[61]:


# We're only interested in commercial caprparks that are publicly available.
com_carparks = carparks_current[carparks_current['parking_type'] == "Commercial"]
com_carparks.head()


# In[62]:


len(com_carparks)


# In[63]:


col_to_drop = ["census_year", "block_id", "property_id", "base_property_id"]
com_carparks.drop(col_to_drop, axis=1, inplace=True)
com_carparks.head()


# In[64]:


com_carparks.reset_index(drop=True)


# In[65]:


import re


# Regex pattern:
# (1) Street: everything up until the ALL CAPS word
# (2) Suburb: the ALL CAPS word
# (3) Postcode: the last 4 digits
pattern = r"^(.*?)\s+([A-Z]+)\s+[A-Z]{2,3}\s+(\d{4})$"

# Extract into new columns
com_carparks[["street_address", "suburb", "postcode"]] = com_carparks["building_address"].str.extract(pattern)

com_carparks.head()


# In[66]:


#com_carparks.to_csv('cleaned_carparks.csv', index=False)#


# In[67]:


import geopandas as gpd
import pandas as pd

# Load your GeoJSON
geojson_gdf = gpd.read_file("lights.geojson")

# Load shapefile with postcodes
postcode_gdf = gpd.read_file("POSTCODE_POLYGON.shp")


# In[68]:


geojson_gdf = geojson_gdf.to_crs(postcode_gdf.crs)


# In[69]:


joined = gpd.sjoin(geojson_gdf, postcode_gdf[["POSTCODE", "geometry"]], how="left", predicate="within")

# Convert to pandas DataFrame (if you don’t need geometry anymore)
df = pd.DataFrame(joined.drop(columns="geometry"))

df.head()


# In[70]:


df.info()


# In[71]:


df.label.describe()


# In[72]:


df.label.max()


# In[73]:


df.label.min()


# In[77]:


df.label_float = df.label.astype(float)


# In[78]:


df.label_float.mean()


# In[79]:


col_to_keep = ["geo_point_2d", "ext_id", "label", "POSTCODE"]
lights = df[col_to_keep]
lights.head()


# In[80]:


#lights.to_csv('cleaned_lights.csv', index=False)


# In[ ]:




