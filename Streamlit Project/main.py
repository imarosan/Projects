"""
Name:       Yerden
CS230:      Section XXX
Data:       airports.csv

"""
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic
import matplotlib.pyplot as plt

def grand_database(data):
    # Sidebar filters
    continent_options = data['continent'].dropna().unique().tolist()
    continent = st.sidebar.selectbox("Select Continent", [''] + continent_options)
    if continent:
        country_options = data[data['continent'] == continent]['iso_country'].dropna().unique().tolist()
    else:
        country_options = []
    country = st.sidebar.selectbox("Select Country", [''] + country_options)
    size_options = data['type'].dropna().unique().tolist()
    size = st.sidebar.selectbox("Select Airport Type", [''] + size_options)
    max_elevation = float(data['elevation_ft'].max())
    min_elevation = float(data['elevation_ft'].min())
    elevation_range = st.sidebar.slider('Elevation Range', min_value=min_elevation , max_value=max_elevation, value=(min_elevation, max_elevation))
    filtered_airports = filter_airports(continent, country, size, data)
    filtered_df = filtered_airports[(filtered_airports['elevation_ft'] >= elevation_range[0]) & (filtered_airports['elevation_ft'] <= elevation_range[1])]
    st.title("The Grand Data Base")
    st.subheader("You can use the parameters in the sidebar to sort the data base")
    st.dataframe(filtered_df)

def sort_elevation(data):
    None
def show_map(data):
    st.title("Specific Airport")
    data[["lon", "lat"]] = data["coordinates"].apply(lambda x: pd.Series(str(x).split(',')))
    search_bar = st.selectbox("Search for Airport Name", options=data['name'].tolist())
    filtered_data = data[data['name'] == search_bar]
    if len(filtered_data) == 1:
        #creating information about specific airport
        st.header("Information")
        st.write(filtered_data[['name', 'type', 'iso_country', 'elevation_ft']])
        st.header("Map")

        # Plotting the coordinates on a map
        map_coordinates(filtered_data)
def airport_distance(data):
    st.title("Airport Distance Calculator")

    # Sidebar inputs
    airport_options = data['name'].dropna().unique().tolist()
    airport_1 = st.sidebar.selectbox("Select Airport 1", airport_options)
    airport_2 = st.sidebar.selectbox("Select Airport 2", airport_options)
    row_1 = data[data['name'] == airport_1]
    row_1[["lon", "lat"]] = row_1["coordinates"].apply(lambda x: pd.Series(str(x).split(',')))
    row_2 = data[data['name'] == airport_2]
    row_2[["lon", "lat"]] = row_2["coordinates"].apply(lambda x: pd.Series(str(x).split(',')))
    if airport_1 and airport_2:
        # Get the coordinates of the selected airports
        coords_1 = get_coordinates(row_1)
        coords_2 = get_coordinates(row_2)
        st.write(f"Coordinate Airport 1 {coords_1}")
        st.write(f"Coordinate Airport 2 {coords_2}")
        if coords_1 and coords_2:
            # Calculate the distance between the two airports
            distance = calculate_distance(coords_1, coords_2)

            # Display the distance
            st.success(f"The distance between {airport_1} and {airport_2} is {distance:.2f} km.")
            combined_df = pd.concat([row_1, row_2], axis=0)
            map_coordinates(combined_df)
        else:
            st.warning("Failed to retrieve coordinates for the selected airports.")
    else:
        st.info("Please select two airports to calculate the distance.")

def get_coordinates(row):
    latitude = row['lat'].values[0]
    longitude = row['lon'].values[0]
    return (latitude, longitude)

def calculate_distance(coords_1, coords_2):
    return geodesic(coords_1, coords_2).kilometers

def all_airports(data):
    st.title("Airport Coordinate Plotter")

    # Sidebar filters
    continent_options = data['continent'].dropna().unique().tolist()
    continent = st.sidebar.selectbox("Select Continent", [''] + continent_options)

    if continent:
        country_options = data[data['continent'] == continent]['iso_country'].dropna().unique().tolist()
    else:
        country_options = []
    country = st.sidebar.selectbox("Select Country", [''] + country_options)

    size_options = data['type'].dropna().unique().tolist()
    size = st.sidebar.selectbox("Select Airport Type", [''] + size_options)

    # Filter the airports based on user selection
    filtered_airports = filter_airports(continent, country, size, data)

    # Plotting the coordinates on a map
    map_coordinates(filtered_airports)
def filter_airports(continent, country, size, data):
    filtered_df = data.copy()

    if continent:
        filtered_df = filtered_df[filtered_df['continent'] == continent]
    if country:
        filtered_df = filtered_df[filtered_df['iso_country'] == country]
    if size:
        filtered_df = filtered_df[filtered_df['type'] == size]

    return filtered_df

def map_coordinates(data):
    # Create a map centered on the coordinates of the first airport
    data[["lon", "lat"]] = data["coordinates"].apply(lambda x: pd.Series(str(x).split(',')))
    if not data.empty:
        map_center = [data['lat'].iloc[0], data['lon'].iloc[0]]
        map_airports = folium.Map(location=map_center, zoom_start=5)

        # Add markers for each airport
        for index, row in data.iterrows():
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=row['name'],
                icon=folium.Icon(color='blue', icon='plane')
            ).add_to(map_airports)

        # Display the map
        folium_static(map_airports)
    else:
        st.warning("No airports found based on the selected filters.")
def graphs(data):
    st.title("Histogram with User Entry")

    # User input for data
    data_option = st.selectbox("Select Data", ("Continent", "Country", "Type"))

    # Assign data based on user selection
    if data_option == "Continent":
        plot = count_repeated_values(data, 'continent')
    elif data_option == "Country":
        plot = count_repeated_values(data, 'iso_country')
    elif data_option == "Type":
        plot = count_repeated_values(data, 'type')
    fig, ax = plt.subplots()
    plt.bar(plot['Value'], plot['Count'])
    plt.xticks(fontsize=6)
    plt.xlabel(data_option)
    plt.ylabel('Count')
    plt.title(f'Number of Airport vs {data_option}')
    for i, v in enumerate(plot['Count']):
        plt.text(i, v, str(v), ha='center', va='bottom', fontsize=5)
    st.pyplot(fig)
    st.title("Compare Countries Airport Elevation")
    # Group countries and find their mean elevation
    chart_data = data[["iso_country", "elevation_ft"]]
    sorted_data = chart_data.groupby('iso_country').mean().reset_index()
    select_countries = st.multiselect('Select Countries', options=sorted_data['iso_country'].tolist())
    sorted_countries = sorted_data[sorted_data['iso_country'].isin(select_countries)]
    if len(sorted_countries) > 0:
        st.header("Aiport Average Elevation")
        st.bar_chart(sorted_countries.set_index('iso_country'))

def count_repeated_values(data, column_name):
    column_counts = data[column_name].value_counts()
    repeated_values = pd.DataFrame({'Value': column_counts.index, 'Count': column_counts.values})
    filtered_df = repeated_values[repeated_values['Count'] > 1].head(20)
    return filtered_df

def main():
    data = pd.read_csv("airports.csv")
    pages = {
        'Grand DataBase': grand_database,
        'All Airports': all_airports,
        'Specific Airport': show_map,
        'Distance Airports': airport_distance,
        'Graphs With Parameters': graphs
    }
    nav_container = st.container()
    with nav_container:
        st.sidebar.title('Navigation')
        page = st.sidebar.radio('Select Section', list(pages.keys()))
    pages[page](data)
main()
