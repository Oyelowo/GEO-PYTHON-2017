# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 16:39:37 2017

@author: oyeda
"""
import geopandas as gpd
from fiona.crs import from_epsg
import folium.plugins
from folium.plugins import MarkerCluster
#Interactive maps on Leaflet
#Whenever you go into a website that has some kind of interactive map, it is quite 
#probable that you are wittnessing a map that has been made with a JavaScipt library 
#called Leaflet (the other popular one that you might have wittnessed is called OpenLayers).

#There is also a Python module called Folium that makes it possible visualize data 
#that’s been manipulated in Python on an interactive Leaflet map.

#==============================================================================
# Creating a simple interactive web-map
#==============================================================================
#Let’s first see how we can do a simple interactive web-map without any data on it. '
#We just visualize OpenStreetMap on a specific location of the a world.

#First thing that we need to do is to create a Map instance. There are few 
#parameters that we can use to adjust how in our Map instance that will affect 
#how the background map will look like.



# Create a Map instance
m = folium.Map(location=[60.25, 24.8], tiles='Stamen Toner',
                   zoom_start=10, control_scale=True)
#The first parameter location takes a pair of lat, lon values as list as an input 
#which will determine where the map will be positioned when user opens up the map.
#zoom_start -parameter adjusts the default zoom-level for the map (the higher the 
#number the closer the zoom is). control_scale defines if map should have a scalebar or not.

#Let’s see what our map looks like. We can already now save the map without any content. 
#It will now just show the basemap in such a way that we initialized it. Let’s save the 
#map as /home/geo/base_map.html.

outfp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\base_map.html"

m.save(outfp)

#Take a look at the map by clicking it with right mouse and open it with Google 
#Chrome which then opens it up in a web browser.

#Let’s change the basemap style to Stamen Toner and change the location of our map slightly. 
#The tiles -parameter is used for changing the background map provider and map style 
#(see here for all possible ones).
 # Let's change the basemap style to 'Stamen Toner'
m = folium.Map(location=[40.730610, -73.935242], tiles='Stamen Toner',
                zoom_start=12, control_scale=True, prefer_canvas=True)

 # Filepath to the output
outfp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\base_map2.html"

# Save the map
m.save(outfp)

#Task
#
#Play around with the parameters and save the map and see how those changes affect 
#the look of the map.
#
#Adding layers to the map
#Adding layers to a web-map is fairly straightforward and similar procedure as 
#with Bokeh and we can use familiar tools to handle the data, i.e. Geopandas. 
#Our ultimate aim is to create a plot like this where population in Helsinki and 
#the address points are plotted on top of a web-map:
    
    
# Filepaths
fp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\Vaestotietoruudukko_2015.shp"
addr_fp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\addresses.shp"

# Read Data
data = gpd.read_file(fp)
ad = gpd.read_file(addr_fp)

# Re-project to WGS84
data['geometry'] = data['geometry'].to_crs(epsg=4326)
ad['geometry'] = ad['geometry'].to_crs(epsg=4326)



# Update the CRS of the GeoDataFrame
data.crs = from_epsg(4326)
ad.crs = from_epsg(4326)

# Make a selection (only data above 0 and below 1000)
data = data.ix[(data['ASUKKAITA'] > 0) & (data['ASUKKAITA'] <= 1000)]

# Create a Geo-id which is needed by the Folium (it needs to have a unique identifier for each row)
data['geoid'] = data.index.astype(str)
ad['geoid'] = ad.index.astype(str)

# Select data
data = data[['geoid', 'ASUKKAITA', 'geometry']]

# Save the file as geojson
jsontxt = data.to_json()
#Now we have our population data stored in the jsontxt variable as GeoJSON format 
#which basically contains the data as text in a similar way that it would be 
#written in the .geojson -file.

#Now we can start visualizing our data with Folium.
import folium

# Create a Clustered map where points are clustered


map_osm = folium.Map(location=[60.25, 24.8], tiles='Stamen Toner',
                   zoom_start=10, control_scale=True)

#The next was the former but did not work. I had to take off "folium." and also loaded "from folium.plugins import MarkerCluster"
#marker_cluster = folium.MarkerCluster().add_to(map_osm)
marker_cluster = MarkerCluster().add_to(map_osm)

#import folium
#print(folium.__file__)
#print(folium.__version__)

# Create Choropleth map where the colors are coming from a column "ASUKKAITA".
# Notice: 'geoid' column that we created earlier needs to be assigned always as the first column
# with threshold_scale we can adjust the class intervals for the values

#Here again, I changed, "geo_str" to "geo_data" to make it work.
map_osm.choropleth(geo_data=jsontxt, data=data, columns=['geoid', 'ASUKKAITA'], key_on="feature.id",
                   fill_color='YlOrRd', fill_opacity=0.9, line_opacity=0.2, line_color='white', line_weight=0,
                   threshold_scale=[100, 250, 500, 1000, 2000],
                   legend_name='Population in Helsinki', highlight=False, smooth_factor=1.0)


# Create Address points on top of the map
for idx, row in ad.iterrows():
    # Get lat and lon of points
    lon = row['geometry'].x
    lat = row['geometry'].y

    # Get address information
    address = row['address']
    # Add marker to the map
    folium.RegularPolygonMarker(location=[lat, lon], popup=address, fill_color='#2b8cbe', number_of_sides=6, radius=8).add_to(marker_cluster)

# Save the output
outfp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\pop15.html"
map_osm.save(outfp)
#That’s it! Now we have a cool interactive map with some markers on 
#it and grid showing the population in the Helsinki Region on top of a basemap. 
#Open it with your browser and see the result.

