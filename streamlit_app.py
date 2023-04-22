import pandas as pd
import folium
from folium.plugins import MeasureControl
import streamlit as st
from streamlit_folium import folium_static
from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt
import altair as alt



st.title("u19096667 Tiaan Mitton Dashboard")

#Load data and add headers
airlines = pd.read_csv('airlines.dat', header=None)
airline_col = ['Airline ID', 'Name', 'Alias', 'IATA', 'ICAO', 'Callsign', 'Country', 'Active']
airlines.columns = airline_col

airports = pd.read_csv('airports.dat', header=None)
airport_col = ['Airport ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude', 'Altitude', 'Timezone', 'DST', 'Tz database time zone', 'Type', 'Source']
airports.columns = airport_col

countries = pd.read_csv('countries.dat', header=None)
country_col = ['Name', 'ISO Code', 'DAFIF Code']
countries.columns = country_col

planes = pd.read_csv('planes.dat', header=None)
plane_col = ['Name', 'IATA code', 'ICAO code']
planes.columns = plane_col

routes = pd.read_csv('routes.dat', header=None)
route_col = ['Airline', 'Airline ID', 'Source airport', 'Source airport ID', 'Destination airport', 'Destination airport ID', 'Codeshare', 'Stops', 'Equipment']
routes.columns = route_col

st.write("Flight time calculator:")





# Convert the Airport ID's to string for the join
airports['Airport ID'] = airports['Airport ID'].astype(str)
routes['Source airport ID'] = routes['Source airport ID'].astype(str)
routes['Destination airport ID'] = routes['Destination airport ID'].astype(str)

# Join the airports table twice to the routes table
source_airport_info = airports[['Airport ID', 'Latitude', 'Longitude']]
source_airport_info.columns = ['Source airport ID', 'Source Latitude', 'Source Longitude']

destination_airport_info = airports[['Airport ID', 'Latitude', 'Longitude']]
destination_airport_info.columns = ['Destination airport ID', 'Destination Latitude', 'Destination Longitude']

joined_table = pd.merge(routes, source_airport_info, on='Source airport ID', how='left')
join = pd.merge(joined_table, destination_airport_info, on='Destination airport ID', how='left')

# Clean the latitude data
join['Source Latitude'] = join['Source Latitude'].dropna().astype(float)
join['Source Longitude'] = join['Source Longitude'].dropna().astype(float)
join['Destination Latitude'] = join['Destination Latitude'].dropna().astype(float)
join['Destination Longitude'] = join['Destination Longitude'].dropna().astype(float)

# Load the joined table
routes = join.dropna()

import geopy.distance

# create a map centered on Africa
m = folium.Map(location=[0, 20], zoom_start=2)

# create a sidebar panel for airport selection
with st.sidebar:
    # add start and end airport selectors to the sidebar panel
    start_airport = st.selectbox('Select a Departure Airport', airports['Name'])
    end_airport = st.selectbox('Select a Destination Airport', airports['Name'])

    # get latitude and longitude of start and end airports
    start_airport_lat, start_airport_lon = airports[airports['Name'] == start_airport][['Latitude', 'Longitude']].values[0]
    end_airport_lat, end_airport_lon = airports[airports['Name'] == end_airport][['Latitude', 'Longitude']].values[0]

# create a list of airport coordinates to calculate the map bounds
airport_coords = [
    (start_airport_lat, start_airport_lon),
    (end_airport_lat, end_airport_lon)
]

# get the maximum and minimum latitude and longitude values
min_lat, min_lon = min(airport_coords)
max_lat, max_lon = max(airport_coords)

# calculate the center of the map
center_lat, center_lon = (min_lat + max_lat) / 2, (min_lon + max_lon) / 2

# calculate the zoom level to fit both airports on the map
zoom = int(min(8, 1.5 / max(abs(max_lat - min_lat), abs(max_lon - min_lon))) + 2)

# create the map with the calculated center and zoom level
m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)

# Add a dropdown to select map tiles
tile_layers = {
    "OpenStreetMap": folium.TileLayer(),
    "Stamen Terrain": folium.TileLayer(name="Stamen Terrain", tiles="Stamen Terrain"),
    "Stamen Toner": folium.TileLayer(name="Stamen Toner", tiles="Stamen Toner"),
    "Stamen Watercolor": folium.TileLayer(name="Stamen Watercolor", tiles="Stamen Watercolor"),
}

select_layer = st.sidebar.selectbox("Select a map style", list(tile_layers.keys()))

# Set the selected layer as the active layer
tile_layers[select_layer].add_to(m)

folium.Marker(
    location=[start_airport_lat, start_airport_lon],
    icon=folium.Icon(color='green'),
    tooltip=start_airport
).add_to(m)

folium.Marker(
    location=[end_airport_lat, end_airport_lon],
    icon=folium.Icon(color='red'),
    tooltip=end_airport
).add_to(m)

# add curved line to show flight path
coords = [(start_airport_lat, start_airport_lon), (end_airport_lat, end_airport_lon)]
flight_path = folium.PolyLine(
    locations=coords,
    color='blue',
    weight=3,
    opacity=0.7,
    smooth_factor=1
).add_to(m)



# calculate flight time
def haversine(lat1, lon1, lat2, lon2):
    R = 6372.8 # Earth radius in kilometers
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))
    return R * c

distance = haversine(start_airport_lat, start_airport_lon, end_airport_lat, end_airport_lon)
speed = 800 # average speed of a commercial airliner in km/h
flight_time = distance / speed

st.write(f"Flight distance: {distance:.2f} km")
st.write(f"Flight time: {flight_time:.2f} hours")

# display the map
folium_static(m)




# Sort airports by altitude
airports = airports.sort_values('Altitude', ascending=False)

# Create a bar chart using Altair
chart = alt.Chart(airports).mark_bar().encode(
    x=alt.X('Altitude:Q', title='Altitude'),
    y=alt.Y('Name:N', title='Airport'),
    color=alt.condition(
        alt.datum.Altitude < airports['Altitude'].quantile(0.05),
        alt.value('blue'), alt.value('red')
    )
).properties(
    width=800,
    height=500
)

# Display the chart using Streamlit
st.altair_chart(chart)
