# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 09:39:16 2017

@author: oyeda
"""
from bokeh.plotting import figure, save
from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper
import geopandas as gpd
import pysal as ps
from bokeh.models import HoverTool
from bokeh.palettes import RdYlBu11 as palette
from bokeh.models import LogColorMapper
import matplotlib.pyplot as plt

#Okey, so we have the address and id columns plus the geometry column as attributes.
#
#Now, as a second step, we need to calculate the x and y coordinates of those points.
#Unfortunately there is not a ready made function in geopandas to do that.
#
#Thus, let’s create our own function called getPointCoords() which will return 
#the x or y coordinate of a given geometry. It shall have two parameters: geom 
#and coord_type where the first one should be a Shapely geometry object and 
#coord_type should be either 'x' or 'y'.
#==============================================================================
def getPointCoords(row, geom, coord_type):
    """Calculates coordinates ('x' or 'y') of a Point geometry"""
    if coord_type == 'x':
        return row[geom].x
    elif coord_type == 'y':
        return row[geom].y

#Okey, so we have the address and id columns plus the geometry column as attributes.
#
#Second step is where calculate the x and y coordinates of the nodes of our lines.
#
#Let’s create our own function called getLineCoords() in a similar manner as 
#previously but now we need to modify it a bit so that we can get coordinates 
#out of the Shapely LineString object.

def getLineCoords(row, geom, coord_type):
    """Returns a list of coordinates ('x' or 'y') of a LineString geometry"""
    if coord_type == 'x':
        return list( row[geom].coords.xy[0] )
    elif coord_type == 'y':
        return list( row[geom].coords.xy[1] )
        
#Indeed, they do. Let’s proceed and parse the x and y values of our grid. 
#Let’s create own function for that as well.

def getPolyCoords(row, geom, coord_type):
    """Returns the coordinates ('x' or 'y') of edges of a Polygon exterior"""

    # Parse the exterior of the coordinate
    exterior = row[geom].exterior

    if coord_type == 'x':
        # Get the x coordinates of the exterior
        return list( exterior.coords.xy[0] )
    elif coord_type == 'y':
        # Get the y coordinates of the exterior
        return list( exterior.coords.xy[1] )

#==============================================================================


    
#==============================================================================
# #Adding interactivity to the map
#==============================================================================
#In Bokeh there are specific set of plot tools that you can add to the plot. 
#Actually all the buttons that you see on the right side of the plot are exactly 
#such tools. It is e.g. possible to interactively show information about the 
#plot objects to the user when placing mouse over an object as you can see from 
#the example on top of this page. The tool that shows information from the plot 
#objects is an inspector called HoverTool that annotate or otherwise report 
#information about the plot, based on the current cursor position.

#Let’s see now how this can be done.
#
#First we need to import the HoverTool from bokeh.models that includes .

#Next, we need to initialize our tool.



#As you can see now the plot shows information about the points and the content 
#is the information derived from column address.
#
#Hint
#
#Of course, you can show information from multiple columns at the same time. This 
#is achieved simply by adding more tooltip variables when defining the tooltips, such as:

#==============================================================================
#my_hover2.tooltips = [('Label1', '@col1'), ('Label2', '@col2'), ('Label3', '@col3')]
#==============================================================================
 
 
#==============================================================================
# Line map
# Okey, now we have made a nice point map out of a Shapefile. Let’s see how we 
# can make an interactive map out of a Shapefile that represents metro lines in 
# Helsinki. We follow the same steps than before, i.e. 1) read the data, 2) 
#     calculate x and y coordinates, 3) convert the DataFrame into a 
#     ColumnDataSource and 4) make the map and save it as html.
#==============================================================================


# File paths
grid_fp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\TravelTimes_to_5975375_RailwayStation.shp"
point_fp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\addresses.shp"
metro_fp =r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\metro.shp"

# Read files
grid = gpd.read_file(grid_fp)
points = gpd.read_file(point_fp)
metro = gpd.read_file(metro_fp)

#As usual, we need to make sure that the coordinate reference system is the same 
#in every one of the layers. Let’s use the CRS of the grid layer and apply it to 
#our points and metro line.

# Get the CRS of our grid
CRS = grid.crs

print(CRS)

# Convert the geometries of metro line and points into that one
points['geometry'] = points['geometry'].to_crs(crs=CRS)
metro['geometry'] = metro['geometry'].to_crs(crs=CRS)
#Okey now, the geometries should have similar values:

points['geometry'].head(1)
 

metro['geometry'].head(1)


grid['geometry'].head(1)



# Get the Polygon x and y coordinates
grid['x'] = grid.apply(getPolyCoords, geom='geometry', coord_type='x', axis=1)
grid['y'] = grid.apply(getPolyCoords, geom='geometry', coord_type='y', axis=1)

# Calculate x and y coordinates of the line
metro['x'] = metro.apply(getLineCoords, geom='geometry', coord_type='x', axis=1)
metro['y'] = metro.apply(getLineCoords, geom='geometry', coord_type='y', axis=1)

# Calculate x and y coordinates of the points
points['x'] = points.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)
points['y'] = points.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)
#Great, now we have x and y coordinates for all of our datasets. 
#Let’s see how our grid coordinates look like.

# Show only head of x and y columns
grid[['x', 'y']].head(2)

# Get the Polygon x and y coordinates

#Let’s now classify the travel times of our grid int 5 minute intervals until 
#200 minutes using a pysal classifier called User_Defined that allows to set our 
#own criteria for class intervals. But first we need to replace the No Data values 
#with a large number so that they wouldn’t be seen as the “best” accessible areas.

# Replace No Data values (-1) with large number (999)
grid = grid.replace(-1, 999)

# Classify our travel times into 5 minute classes until 200 minutes
# Create a list of values where minumum value is 5, maximum value is 200 and step is 5.
breaks = [x for x in range(5, 200, 5)]

# Initialize the classifier and apply it
classifier = ps.User_Defined.make(bins=breaks)
pt_classif = grid[['car_r_t']].apply(classifier)

# Rename the classified column
pt_classif.columns = ['car_r_t_ud']

# Join it back to the grid layer
grid = grid.join(pt_classif)
#What do we have now?

grid.head(2)

#Okey, so we have many columns but the new one that we just got is the last one, 
#i.e. pt_r_tt_ud that contains the classes that we reclassified based on the 
#public transportation travel times on 5 minute intervals.

#3rd step: Let’s now convert our GeoDataFrames into Bokeh ColumnDataSources 
#(without geometry columns)

# Make a copy, drop the geometry column and create ColumnDataSource
m_df = metro.drop('geometry', axis=1).copy()
msource = ColumnDataSource(m_df)

# Make a copy, drop the geometry column and create ColumnDataSource
p_df = points.drop('geometry', axis=1).copy()
psource = ColumnDataSource(p_df)

# Make a copy, drop the geometry column and create ColumnDataSource
g_df = grid.drop('geometry', axis=1).copy()
gsource = ColumnDataSource(g_df)


#==============================================================================
# Okey, now we are ready to roll and visualize our layers.
# 
# 4th step: For visualizing the Polygons we need to define the color palette that 
# we are going to use. There are many different ones available but we are now going 
# to use a palette called RdYlBu and use eleven color-classes for the values 
# (defined as RdYlBu11). Let’s prepare our color_mapper.
#==============================================================================

# Let's first do some coloring magic that converts the color palet into map numbers (it's okey not to understand)

# Create the color mapper
color_mapper = LogColorMapper(palette=palette)
#Now we are ready to visualize our polygons and add the metro line and the 
#points on top of that. Polygons are visualized using patches objects in Bokeh.

# Initialize our figure
p = figure(title="Travel times with Car to Central Railway station")

# Plot grid
p.patches('x', 'y', source=gsource,
         fill_color={'field': 'car_r_t_ud', 'transform': color_mapper},
         fill_alpha=1.0, line_color="black", line_width=0.05)

# Add metro on top of the same figure
p.multi_line('x', 'y', source=msource, color="red", line_width=2)

# Add points on top (as black points)
p.circle('x', 'y', size=3, source=psource, color="black")

# Save the figure
outfp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\solution\car_travel_time_map.html"
save(p, outfp)


#Cool, now we have an interactive map with three layers! As you see, this map 
#does not yet have the same functionalities as the map on top of this page and 
#we won’t go into details how to do them now. If you are interested how to make 
#such a map, you can read the docs for producing advanced bokeh map from here.
#
#Now we move forward to see how we can share interactive maps on GitHub.