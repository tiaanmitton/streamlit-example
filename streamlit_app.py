import pandas as pd
import folium
from folium.plugins import MeasureControl
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




import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static


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

# add flight line between start and end airports
flight_line = folium.PolyLine(
    locations=[[start_airport_lat, start_airport_lon], [end_airport_lat, end_airport_lon]],
    weight=3,
    color='blue'
).add_to(m)


# display the map
folium_static(m)
