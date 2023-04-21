
import pandas as pd
import folium
from folium.plugins import MeasureControl
import streamlit as st
from streamlit_folium import folium_static
from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt




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





# create a sidebar panel for airport selection
with st.sidebar:
    # add start and end airport selectors to the sidebar panel
    start_airport = st.selectbox('Select a Departure Airport', airports['Name'])
    end_airport = st.selectbox('Select a Destination Airport', airports['Name'])
    
    # get latitude and longitude of start and end airports
    start_airport_lat, start_airport_lon = airports[airports['Name'] == start_airport][['Latitude', 'Longitude']].values[0]
    end_airport_lat, end_airport_lon = airports[airports['Name'] == end_airport][['Latitude', 'Longitude']].values[0]
    
    # check if there is a direct route between the selected airports
    route_exists = False
    for index, row in routes.iterrows():
        if row['Source airport ID'] == start_airport.index[0] and row['Destination airport ID'] == end_airport.index[0]:
            route_exists = True
            break
    
    if not route_exists:
        st.warning("There is no direct route between the selected airports.")
        st.stop()


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






# # calculate airports per country
# airports_per_country = airports.groupby('Country')['Name'].count()

# # calculate airports per city
# airports_per_city = airports.groupby(['Country', 'City'])['Name'].count()

# # create a bar chart showing airports per country
# fig1, ax1 = plt.subplots()
# ax1.bar(airports_per_country.index, airports_per_country.values)
# ax1.set_xticklabels(airports_per_country.index, rotation=90)
# ax1.set_title('Airports per Country')
# st.pyplot(fig1)

# # create a bar chart showing airports per city
# fig2, ax2 = plt.subplots()
# ax2.bar(airports_per_city.index.get_level_values('City'), airports_per_city.values)
# ax2.set_xticklabels(airports_per_city.index.get_level_values('City'), rotation=90)
# ax2.set_title('Airports per City')
# st.pyplot(fig2)
