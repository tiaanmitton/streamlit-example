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

st.write("My map")
#st.table(airports)


import pandas as pd
import folium
from folium.plugins import MeasureControl
import streamlit as st


# Create a map centered over Africa with a border
m = folium.Map(location=[8, 20], tiles='Stamen Terrain', width=500, height=500, zoom_start=3, control_scale=True)

# Create a dropdown menu for selecting the start airport
start_airport = st.selectbox('Start airport:', airports['Name'].tolist())

# Create a dropdown menu for selecting the end airport
end_airport = st.selectbox('End airport:', airports['Name'].tolist())

# Get the latitude and longitude of the start airport
start_airport_data = airports.loc[airports['Name'] == start_airport]
start_latitude = start_airport_data['Latitude'].values[0]
start_longitude = start_airport_data['Longitude'].values[0]

# Add a marker for the start airport
folium.Marker(location=[start_latitude, start_longitude], popup=start_airport, icon=folium.Icon(color='green')).add_to(m)

# Get the latitude and longitude of the end airport
end_airport_data = airports.loc[airports['Name'] == end_airport]
end_latitude = end_airport_data['Latitude'].values[0]
end_longitude = end_airport_data['Longitude'].values[0]

# Add a marker for the end airport
folium.Marker(location=[end_latitude, end_longitude], popup=end_airport, icon=folium.Icon(color='red')).add_to(m)

# Add a polyline between the start and end airports
folium.PolyLine(locations=[[start_latitude, start_longitude], [end_latitude, end_longitude]], color='red').add_to(m)

# Add a scale control to the map
m.add_child(MeasureControl())

# Display the map
st.markdown(m._repr_html_(), unsafe_allow_html=True)
