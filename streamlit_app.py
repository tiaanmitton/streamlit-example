import pandas as pd
import streamlit as st

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

st.write("My table")
st.table(airports)


import folium
from folium.plugins import MeasureControl
from ipywidgets import interact, Dropdown

m = folium.Map(location=[37.7749, -122.4194], zoom_start=3)

# Create a dropdown menu for selecting the start airport
start_airport_dropdown = Dropdown(options=airports['Name'].tolist(), description='Start airport:')

# Create a dropdown menu for selecting the end airport
end_airport_dropdown = Dropdown(options=airports['Name'].tolist(), description='End airport:')

# Function to update the map based on the selected airports
def update_map(start_airport, end_airport):
    # Get the latitude and longitude of the start airport
    start_airport_data = airports.loc[airports['Name'] == start_airport]
    start_latitude = start_airport_data['Latitude'].values[0]
    start_longitude = start_airport_data['Longitude'].values[0]
    
    # Get the latitude and longitude of the end airport
    end_airport_data = airports.loc[airports['Name'] == end_airport]
    end_latitude = end_airport_data['Latitude'].values[0]
    end_longitude = end_airport_data['Longitude'].values[0]
    
    # Add a polyline between the start and end airports
    folium.PolyLine(locations=[[start_latitude, start_longitude], [end_latitude, end_longitude]], color='red').add_to(m)

# Add the dropdown menus to the map
start_airport_dropdown.observe(lambda change: update_map(change.new, end_airport_dropdown.value), names='value')
end_airport_dropdown.observe(lambda change: update_map(start_airport_dropdown.value, change.new), names='value')

# Add a scale control to the map
m.add_child(MeasureControl())

# Display the map and dropdown menus
display(start_airport_dropdown)
display(end_airport_dropdown)
display(m)

