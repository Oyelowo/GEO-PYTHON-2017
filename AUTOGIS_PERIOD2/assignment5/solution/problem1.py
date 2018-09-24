# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 19:40:56 2017

@author: oyeda
"""

#==============================================================================
# Problem 1: Visualize a static map with multiple layers on it (8 points)
# 
# Play around with the data that was provided for you and used during the lesson
#  and create as interesting, good and beautiful STATIC map(s) that you can. 
# You can read a few useful hints about what to consider when creating maps from this post.
# 
# Upload your maps to the docs folder and create link to those map(s) in the index.md file. 
# Use your imagination, you can e.g. do some calculations on the current datasets 
# or use also the analyses that we have done earlier in the course.
# 
# But notice that the main aim here is that you try to do the visualizations as 
# best as you can, thus the subject what you are presenting is not important.
#==============================================================================



# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 15:02:12 2017

@author: oyeda
"""

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, Polygon

# Filepaths
grid_fp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\TravelTimes_to_5975375_RailwayStation.shp"
roads_fp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\roads.shp"
metro_fp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\metro.shp"

# Read files
grid = gpd.read_file(grid_fp)
roads = gpd.read_file(roads_fp)
metro = gpd.read_file(metro_fp)


#Then, we need to be sure that the files are in the same coordinate system.
# Let’s use the crs of our travel time grid.

# Get the CRS of the grid
gridCRS = grid.crs

# Reproject geometries using the crs of travel time grid
roads['geometry'] = roads['geometry'].to_crs(crs=gridCRS)
metro['geometry'] = metro['geometry'].to_crs(crs=gridCRS)

#exlude the grid without data on walking time
grid= grid.loc[grid.loc[:, "walk_t"]!=-1]

#Finally we can make a visualization using the .plot() -function in Geopandas.
#import matplotlib.legend as mlgd
# Visualize the travel times into 9 classes using "Quantiles" classification scheme
# Add also a little bit of transparency with `alpha` parameter
# (ranges from 0 to 1 where 0 is fully transparent and 1 has no transparency)
#my_map = grid.plot(column="car_r_t", linewidth=0.03, cmap="Reds", scheme="quantiles", k=9, alpha=0.9)
my_map = grid.plot(column="walk_t", linewidth=0.02, legend=True, cmap="RdYlGn", scheme="Quantiles", k=5, alpha=0.9)

# Add roads on top of the grid
# (use ax parameter to define the map on top of which the second items are plotted)
roads.plot(ax=my_map, color="grey", legend=True, linewidth=1.2)

# Add metro on top of the previous map
metro.plot(ax=my_map, color="yellow", legend=True, linewidth=2.0)

## Insert a circle on top of the Central Railway Station (coords in EurefFIN-TM35FIN)
station_x = 385752.214
station_y =  6672143.803
r_s= gpd.GeoDataFrame()

raut = Point(station_x, station_y)
r_s["geometry"]=""
r_s.loc[1,"geometry"]=raut
#r_s["geometry"]=r_s["geometry"].to_crs(crs=gridCRS)

r_s.plot(ax=my_map, color= "blue", legend=True, linewidth=3)
#plt.plot(r_s)


#plt.legend(["roads", "metro line","Rautatientori"])

plt.title("Walking Time to Helsinki Railway Station")


# Remove the empty white-space around the axes
plt.tight_layout()


#plt.show()

# Save the figure as png file with resolution of 300 dpi
outfp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\solution\static_map.png"
plt.savefig(outfp, dpi=300)

