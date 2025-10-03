######################################################################################
####                                                                              ####  
####                             Motorbike Hotspot Data ETL                       ####
####                                                                              ####
######################################################################################

# Loading required libraries----------------------------------------------------------
import pandas as pd
from pathlib import Path
from plotly import express as px
from plotly import graph_objects as go
from plotly import io as pio
# Also need kaleido for image export

# Retrieving the current working directory---------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent


######################################################################################
####                                  Data Loading                                ####

# Loading crime datasets--------------------------------------------------------------
# Crime data
crime_data = pd.read_csv(f'{SCRIPT_DIR}/Cleaned data/cleaned_postcode_crime_data.csv')

# Yearly trend crime data for motor vehicle theft
trend_crime_data = (pd.read_excel(f'{SCRIPT_DIR}/Source data/Data_Tables_LGA_Recorded_Offences_Year_Ending_March_2025.xlsx', sheet_name = 'Table 03').
    loc[lambda df: 
            (df['Offence Subgroup'] == 'B41 Motor vehicle theft') & 
            (df['Year'] >= pd.Timestamp.today().year - 4)])

# Car park data
carpark_data = pd.read_csv(f'{SCRIPT_DIR}/Cleaned data/cleaned_postcode_carpark_data.csv')

# street light data
street_light_data = pd.read_csv(f'{SCRIPT_DIR}/Cleaned data/cleaned_postcode_streetlight_data.csv')

# Selected postcode
selected_postcode = 3000


######################################################################################
####                               Data Cleaning                                  ####

# Filtering to the selected postcode--------------------------------------------------
# Filtering crime data
filtered_crime_data = crime_data.loc[lambda df: df['postcode'] == selected_postcode]

# Filtering trend crime data
filtered_trend_crime_data = trend_crime_data.loc[lambda df: df['Postcode'] == selected_postcode]

# Filtering car park data
filtered_carpark_data = carpark_data.loc[lambda df: df['postcode'] == selected_postcode]

# Filtering street light data
filtered_street_light_data = street_light_data.loc[lambda df: df['postcode'] == selected_postcode]

# Creating aggregated metrics---------------------------------------------------------
# Aggregate single year metrics
agg_crime_data_subdivision = (filtered_crime_data.
    groupby('offence_subdivision').
    agg(yearly_offences = ('offence_count', 'sum')).
    reset_index())

# Aggregate trend metrics
agg_crime_data_trend = (filtered_trend_crime_data.
    groupby(['Year', 'Postcode']).
    agg(yearly_offences = ('Offence Count', 'sum')).
    reset_index())

# Pulling car park and street coverage values-----------------------------------------
# Car park counts
carparks = "No car park data available for this postcode." if filtered_carpark_data.empty else filtered_carpark_data.iloc[0]['carpark_count']

# Street light coverage
street_coverage = "No street light data available for this postcode." if filtered_street_light_data.empty else filtered_street_light_data.iloc[0]['lights_per_km2']


######################################################################################
####                             Data Visualisation                               ####

# Setting default plotly theme--------------------------------------------------------
pio.templates.default = "plotly_white"

# Setting the default colour scale
colour_scale = 'Viridis'

# Plotting Avg offences by subgroup---------------------------------------------------
plot_off_subgroup = px.bar(filtered_crime_data.sort_values('offence_count', ascending=True), 
    x='offence_count',
    y='offence_subgroup',
    orientation='h', 
    color='offence_count',
    color_continuous_scale=colour_scale,
    title='Yearly Offences by Theft Subgroup',
    labels={'offence_count':'Yearly Offences', 'offence_subgroup':''})

plot_off_subgroup.update_coloraxes(showscale=False) #Removing the legend
plot_off_subgroup.update_traces(hovertemplate=("<b>%{y}</b><br>" "Yearly offences: %{x:.1f}<br>" "<extra></extra>")) #Updating tooltips

plot_off_subgroup.show()

# Plotting Avg offences by subdivision------------------------------------------------
plot_off_subdivision = px.bar(agg_crime_data_subdivision.sort_values('yearly_offences', ascending=False), 
    x='offence_subdivision',
    y='yearly_offences',
    title=f'Yearly Offences by Theft Subdivision',
    labels={'yearly_offences':'Yearly Offences', 'offence_subdivision':''})

plot_off_subdivision.update_coloraxes(showscale=False) #Removing the legend
plot_off_subdivision.update_traces(marker_color='#778da9',
                                   hovertemplate=("<b>%{x}</b><br>" "Yearly offences: %{y:.1f}<br>" "<extra></extra>")) #Updating tooltips

plot_off_subdivision.show()

# Plotting Car park counts------------------------------------------------------------
if filtered_carpark_data.empty:
    plot_car_parks = go.Figure()
    
    plot_car_parks.add_annotation(
        text=("No car park data available for this postcode.<br>"
             "Currently data is only available for:<br>"
             "3000, 3002, 3003, 3004, 3006, 3008, 3010, 3050, 3051, 3052, 3053, 3181"),
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=12, color="#333333"),
        align="center")

    plot_car_parks.update_layout(
        paper_bgcolor="white",
        height=200,
        width=500,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False))
    
    plot_car_parks.show()

else:
    plot_car_parks = go.Figure(go.Indicator(
        mode = "number",
        value = carparks,
        title = {"text": "Total Secure Car Parks"},
        number={"valueformat": ",", "font": {"size": 56, "color": "#333333"}}))

    plot_car_parks.update_layout(paper_bgcolor='white', height=200, width=500, margin=dict(l=0,r=0,t=30,b=0))

    plot_car_parks.show()

# Plotting street light coverage-------------------------------------------------------
if street_light_data.empty:
    plot_light_coverage = go.Figure()
    
    plot_light_coverage.add_annotation(
        text=("No street light data available for this postcode.<br>"
             "Currently data is only available for:<br>"
             "3000, 3002, 3004, 3006, 3008, 3031, 3052, 3053, 3054, 3141"),
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=12, color="#333333"),
        align="center")

    plot_light_coverage.update_layout(
        paper_bgcolor="white",
        height=200,
        width=500,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False))
    
    plot_light_coverage.show()

else:
    plot_light_coverage = go.Figure(go.Indicator(
        mode = "number",
        value = street_coverage,
        title = {"text": "Street Lights per km²"},
        number={"valueformat": ",", "font": {"size": 56, "color": "#333333"}}))

    plot_light_coverage.update_layout(paper_bgcolor='white', height=200, width=500, margin=dict(l=0,r=0,t=30,b=0))

    plot_light_coverage.show()
    
# Creating a trend plot for yearly offences in the selected postcode------------------
plot_off_subgroup_trend = px.bar(agg_crime_data_trend.sort_values('Year', ascending=True), 
    x='Year',
    y='yearly_offences',
    color_discrete_sequence=['#07A377'],
    labels={'yearly_offences':'Offences', 'Year':''})

plot_off_subgroup_trend.update_layout(
    xaxis=dict(title='', tickfont=dict(size=16)),
    yaxis=dict(title='Offences', title_font=dict(size=16), tickfont=dict(size=14)))

plot_off_subgroup_trend.update_traces(hovertemplate=("Theft Offences: %{y:.0f}<br>" "<extra></extra>")) #Updating tooltips

plot_off_subgroup_trend.show()


######################################################################################
####                               Visual Export                                  ####

# Saving the subgroup chart-----------------------------------------------------------
Path(f'{SCRIPT_DIR}/Visuals/subgroup.json').write_text(plot_off_subgroup.to_json(), encoding='utf-8')

# Saving the subdivision chart----------------------------------------------------------
Path(f'{SCRIPT_DIR}/Visuals/subdivision.json').write_text(plot_off_subdivision.to_json(), encoding='utf-8')

# Saving the trend chart---------------------------------------------------------------
Path(f'{SCRIPT_DIR}/Visuals/trend.json').write_text(plot_off_subgroup_trend.to_json(), encoding='utf-8')

# Saving the car park card--------------------------------------------------------------
plot_car_parks.write_image(f'{SCRIPT_DIR}/Visuals/carparks.png', scale=2)

# Saving cleaned postcode street light coverage-----------------------------------------
plot_light_coverage.write_image(f'{SCRIPT_DIR}/Visuals/light_coverage.png', scale=2)
