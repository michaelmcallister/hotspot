######################################################################################
####                                                                              ####  
####                             VIC Postcode Area Data ETL                       ####
####                                                                              ####
######################################################################################

# Loading required libraries----------------------------------------------------------
import geopandas as gpd

path = "POA_2021_AUST_GDA2020_SHP.zip"
g = gpd.read_file(path)

code_col = "POA_CODE21"

# just VIC postcodes
vic = g[g[code_col].astype(str).str.match(r"^(3\d{3}|8\d{3})$")].copy()

# area in km2
vic = vic.to_crs("EPSG:3577")
vic["area_km2"] = vic.geometry.area / 1_000_000

# centroids back to lat/lon
cent = vic.to_crs("EPSG:4326").geometry.centroid
vic["lat"] = cent.y
vic["long"] = cent.x

# keep fields
out = vic[[code_col, "area_km2", "long", "lat"]].rename(columns={code_col: "postcode"})
out = out.sort_values("postcode").reset_index(drop=True)


# Export 
out.to_csv("vic_postcodes_area.csv", index=False)
out.head()