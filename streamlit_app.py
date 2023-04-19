import pandas as pd
import folium
from folium.plugins import MeasureControl
import streamlit as st
from streamlit_folium import folium_static
from math import radians, cos, sin, asin, sqrt



st.title("My first Streamlit app")
st.write("Streamlit is fun")

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

st.write("My map")
#st.table(airports)


import streamlit as st
import folium
from folium.plugins import PolyLineTextPath
from math import radians, sin, cos, sqrt

# load data
airports = pd.read_csv('https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat', header=None,
                       names=['Airport ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude', 'Altitude',
                              'Timezone', 'DST', 'Tz database time zone', 'Type', 'Source'])
airports = airports[['Name', 'Latitude', 'Longitude']]
airports = airports.dropna()

# create a map centered on Africa
m = folium.Map(location=[0, 20], zoom_start=2)

# add start and end airport markers to the map
start_airport = st.selectbox('Select a start airport', airports['Name'])
end_airport = st.selectbox('Select an end airport', airports['Name'])
start_airport_lat, start_airport_lon = airports[airports['Name'] == start_airport][['Latitude', 'Longitude']].values[0]
end_airport_lat, end_airport_lon = airports[airports['Name'] == end_airport][['Latitude', 'Longitude']].values[0]

folium.Marker(
    location=[start_airport_lat, start_airport_lon],
    icon=folium.Icon(color='green')
).add_to(m)

folium.Marker(
    location=[end_airport_lat, end_airport_lon],
    icon=folium.Icon(color='red')
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

# add curved line to show flight path with flight time text
def add_flight_path(speed):
    flight_time = distance / speed

    # remove previous flight path if it exists
    for layer in m._children.values():
        if hasattr(layer, '_leaflet_id') and layer._leaflet_id.startswith('plugins.PolyLineTextPath'):
            m.remove_layer(layer)

    # add curved line to show flight path with flight time text
    coords = [(start_airport_lat, start_airport_lon), (end_airport_lat, end_airport_lon)]
    flight_path = PolyLineTextPath(
        positions=coords,
        text=f"Flight time: {flight_time:.2f} hours",
        offset=8,
        repeat=True,
        attributes={
            'fill': 'blue',
            'font-weight': 'bold',
            'font-size': '16'
        }
    ).add_to(m)

    st.write(f"Flight distance: {distance:.2f} km")
    st.write(f"Flight time: {flight_time:.2f} hours")

# add slider to select flight speed
speed = st.slider('Select flight speed (km/h)', min_value=500, max_value=
