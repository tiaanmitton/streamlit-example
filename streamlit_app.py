
#try later
import pandas as pd
import folium
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime
from folium.plugins import MarkerCluster
from folium.plugins import MeasureControl
from folium.plugins import Fullscreen
from folium import Marker
from folium import PolyLine
from math import radians, cos, sin, sqrt, atan2

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


# create a map centered on Africa
m = folium.Map(location=[0, 20], zoom_start=2)

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

# create a sidebar panel for airport selection
with st.sidebar:
    # add start and end airport selectors to the sidebar panel
    start_airport = st.selectbox('Select a Departure Airport', airports['Name'])
    end_airport = st.selectbox('Select a Destination Airport', airports['Name'])
    
    # get latitude and longitude of start and end airports
    start_airport_lat, start_airport_lon = airports[airports['Name'] == start_airport][['Latitude', 'Longitude']].values[0]
    end_airport_lat, end_airport_lon = airports[airports['Name'] == end_airport][['Latitude', 'Longitude']].values[0]

# check if there is a route between the two airports
route = routes[(routes['Source airport'] == start_airport) & (routes['Destination airport'] == end_airport)]

if len(route) > 0:
    # get airline ID and number of stops
    airline_id = route['Airline ID'].iloc[0]
    stops = route['Stops'].iloc[0]

    # add markers for start and end airports
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
route_exists = False

# check if there is a route between the selected airports
for route in routes:
    if route['Source airport'] == start_airport and route['Destination airport'] == end_airport:
        route_exists = True
        airline_id = route['Airline ID']
        num_stops = route['Stops']
        break

# add route information to the map
if route_exists:
    st.write(f"Airline: {airlines[airlines['Airline ID'] == airline_id]['Name'].values[0]}")
    st.write(f"Number of stops: {num_stops}")
    flight_path = folium.PolyLine(
        locations=coords,
        color='blue',
        weight=3,
        opacity=0.7,
        smooth_factor=1
    ).add_to(m)
else:
    st.write("There is no route between the selected airports")
    flight_path = folium.PolyLine(
        locations=coords,
        color='red',
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
