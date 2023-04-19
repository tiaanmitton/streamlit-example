
import pandas as pd
import folium
from folium.plugins import MeasureControl
import streamlit as st
from streamlit_folium import folium_static
from math import radians, cos, sin, asin, sqrt





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


# create a map centered on Africa
m = folium.Map(location=[0, 20], zoom_start=2)

# add start and end airport markers to the map
airport_names = airports['Name'].tolist()
airport_names.sort()

start_airport = st.multiselect('Select a Departure Airport', airport_names, search=True)
end_airport = st.multiselect('Select a Destination Airport', airport_names, search=True)

if start_airport and end_airport:
    start_airport_data = airports[airports['Name'] == start_airport[0]][['Latitude', 'Longitude']]
    end_airport_data = airports[airports['Name'] == end_airport[0]][['Latitude', 'Longitude']]
    start_airport_lat, start_airport_lon = start_airport_data.iloc[0]['Latitude'], start_airport_data.iloc[0]['Longitude']
    end_airport_lat, end_airport_lon = end_airport_data.iloc[0]['Latitude'], end_airport_data.iloc[0]['Longitude']

    folium.Marker(
        location=[start_airport_lat, start_airport_lon],
        icon=folium.Icon(color='green'),
        tooltip=start_airport[0]
    ).add_to(m)

    folium.Marker(
        location=[end_airport_lat, end_airport_lon],
        icon=folium.Icon(color='red'),
        tooltip=end_airport[0]
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
