import json
import pandas as pd
import plotly.express as px
from pathlib import Path

"""
Author: Colin Yee
Date: 3/10/23

Background:
**Plotly** is a data visualization library that allows users to create interactive charts and graphs.
Users can interact with the charts by zooming, panning, hovering, and clicking on the data points to get 
additional information. Plotly also allows users to add annotations, text, and images to their charts, making 
it easy to highlight important data points or trends.

**GeoJSON** is a file format for encoding geographical data structures like points, lines, and polygons into a JSON format. 
It consist of objects representing features with properties like name and location data. 
They are used to display and manipulate geographical data. 

The code below essentially:
1. Finds the correct GeoJson and Criminal Logs Data (you may need to change the paths appropriately)
2. Loads the GeoJson into Json Fomat and the criminal logs into a dataframe.
3. Creates a very basic, barebones map in Plotly using the geojson and criminal logs.
"""

"""
The **Path** library is a Python module for working with file and directory paths.
Path.cwd() returns the current working directory as a Path object. 
The current working directory is the directory in which the Python script is currently running.
"""
# Loads the geojson into a JSON object
geojsonPath = Path.cwd()/'limitespdq.geojson' # You might need to change this depending on where and how you are running this code
    # Path('/limitespdq.geojson')
geojson = json.load(open(geojsonPath, "r")) # The GeoJSON data contains the boundaries of the different precincts.

# Loads the criminal logs into a pandas dataframe
# You will probably need to manipulate the dataframe to get something good from it :D
criminalLogsPath = Path.cwd()/'actes-criminels.csv'
    # Path('/actes-criminels.csv')
df = pd.read_csv(criminalLogsPath)

"""
choropleth_mapbox is a function in Plotly that generates a choropleth map 
using Mapbox tilesets. (You don't need to know what that means. It just makes a cool map :D ).
It's different from choropleth because it adds that extra interactivity with the map!
Parameters:
    1. *data_frame*
        Data to be used for the map (should be a pandas dataframe w/ location data)
    2. *geojson*
        GeoJSON data that defines the boundaries of the regions on the map.
    3. *color*
        Column in the dataframe whose values used to assign colors to marks.
    3. *locations*
        Column in the dataframe that contains the location data (e.g. country/district names)
    4. *featureidkey*
        Property in GeoJSON data that contains the identifier for each region. 
        Maps the data in the dataframe to the map.
    5. *center*
        Center point of the map in latitude and longitude
    6. *mapbox_style*
        Design/style of your map. There are many different style of maps to choose from!
    7. *zoom*
        Initial zoom level of the map

    There are many other function parameters like *labels*, *range_color*, *title*, *hover_data*, and *opacity*.
    You can find more information here: 
    https://plotly.github.io/plotly.py-docs/generated/plotly.express.choropleth_mapbox.html
"""
fig = px.choropleth_mapbox(df, geojson=geojson, 
                           color = "PDQ", # Might need to change depending on what you want to measure
                           locations="PDQ", featureidkey="properties.PDQ",
                           center={'lat': 45.508888, 'lon': -73.561668}, # Can change the coordinates to make city more centered
                           mapbox_style="carto-positron", # Another option is called "open-street-map" :o
                           zoom=9
                           )

# .update_layout() updates the layout of the figure (includes all non-date components of the visualization)
# We are just setting the plot to take up the entire avaliable space, with no padding or spacing around the edges.
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Let's see our graph in action!
fig.show()

"""
You can find more information about Plotly on:
    their documentation: https://plotly.com/python/
                         https://plotly.com/python/mapbox-county-choropleth/

    our resource sheet: https://docs.google.com/document/d/1Odq2DBz4SXfB8UXYkBcLW8zqWkYaDYZ81UDeE4b0W4c/edit?usp=sharing
"""