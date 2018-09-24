# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 15:02:12 2017

@author: oyeda
"""

import geopandas as gpd
import matplotlib.pyplot as plt

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

#Finally we can make a visualization using the .plot() -function in Geopandas.

# Visualize the travel times into 9 classes using "Quantiles" classification scheme
# Add also a little bit of transparency with `alpha` parameter
# (ranges from 0 to 1 where 0 is fully transparent and 1 has no transparency)
my_map = grid.plot(column="car_r_t", linewidth=0.03, cmap="Reds", scheme="quantiles", k=9, alpha=0.9)

# Add roads on top of the grid
# (use ax parameter to define the map on top of which the second items are plotted)
roads.plot(ax=my_map, color="grey", linewidth=1.5)

# Add metro on top of the previous map
metro.plot(ax=my_map, color="red", linewidth=2.5)

# Remove the empty white-space around the axes
plt.tight_layout()

# Save the figure as png file with resolution of 300 dpi
outfp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\static_map.png"
plt.savefig(outfp, dpi=300)


#==============================================================================
# Simple interactive point plot
# First, we learn the basic logic of plotting in Bokeh by making a simple 
# interactive plot with few points.
# 
#==============================================================================
#Import necessary functionalities from bokeh.

from bokeh.plotting import figure, save
#First we need to initialize our plot by calling the figure object.

# Initialize the plot (p) and give it a title
p = figure(title="My first interactive plot!")

# Let's see what it is
p

#Next we need to create lists of x and y coordinates that we want to plot.

# Create a list of x-coordinates
x_coords = [0,1,2,3,4]

# Create a list of y-coordinates
y_coords = [5,4,1,2,0]


#==============================================================================
# Note
# 
# In Bokeh drawing points, lines or polygons are always done using list(s) of x and y coordinates.
# Now we can plot those as points using a .circle() -object. Let’s give it a red color and size of 10.
# 
#==============================================================================
p.circle(x=x_coords, y=y_coords, size=10, color="red")

#Finally, we can save our interactive plot into the disk with save -function that we 
#imported in the beginning. All interactive plots are typically saved as html 
#files which you can open in a web-browser.

# Give output filepath
outfp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\points.html"

# Save the plot by passing the plot -object and output path
save(obj=p, filename=outfp)
#Now open your interactive points.html plot by double-clicking it which should open 
#it in a web browser.





#==============================================================================
# It is interactive. You can drag the plot by clicking with left mouse and dragging. 
# There are also specific buttons on the right side of the plot by default which 
# you can select on and off:
# 
# Pan button allows you to switch the dragging possibility on and off (on by default).
# 
# BoxZoom button allows you to zoom into an area that you define by left dragging with mouse an area of your interest.
# 
# Save button allows you to save your interactive plot as a static low resolution .png file.
# 
# WheelZoom button allows you to use mouse wheel to zoom in and out.
# 
# Reset button allows you to use reset the plot as it was in the beginning.
# 
#==============================================================================


#==============================================================================
# Creating interactive maps using Bokeh and Geopandas
# Now we now khow how to make a really simple interactive point plot using Bokeh. 
# What about creating such a map from a Shapefile of points? Of course we can do that, 
# and we can use Geopandas for achieving that goal which is nice!
# 
# Creating an interactive Bokeh map from Shapefile(s) contains typically following steps:
# 
# Read the Shapefile into GeoDataFrame
# Calculate the x and y coordinates of the geometries into separate columns
# Convert the GeoDataFrame into a Bokeh DataSource
# Plot the x and y coordinates as points, lines or polygons (which are in Bokeh words: 
#     circle, multi_line and patches)
# Let’s practice these things and see how we can first create an interactive point map, 
# then a map with lines, and finally a map with polygons where we also add those points 
# and lines into our final map.
# 
# Point map
# Let’s first make a map out of those addresses that we geocoded in the Lesson 3. 
# That Shapefile is provided for you in the data folder that you downloaded.
# 
# Read the data using geopandas which is the first step.
#==============================================================================

import geopandas as gpd


# File path
points_fp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\addresses.shp"

# Read the data
points = gpd.read_file(points_fp)
#Let’s see what we have.

points.head()


#Okey, so we have the address and id columns plus the geometry column as attributes.
#
#Now, as a second step, we need to calculate the x and y coordinates of those points.
#Unfortunately there is not a ready made function in geopandas to do that.
#
#Thus, let’s create our own function called getPointCoords() which will return 
#the x or y coordinate of a given geometry. It shall have two parameters: geom 
#and coord_type where the first one should be a Shapely geometry object and 
#coord_type should be either 'x' or 'y'.

def getPointCoords(row, geom, coord_type):
    """Calculates coordinates ('x' or 'y') of a Point geometry"""
    if coord_type == 'x':
        return row[geom].x
    elif coord_type == 'y':
        return row[geom].y

#Okey great. Let’s then use our function in a similar manner as we did before 
#when classifying data using .apply() function.

# Calculate x coordinates
points['x'] = points.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)

# Calculate y coordinates
points['y'] = points.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)

# Let's see what we have now
points.head()

#
#Okey great! Now we have the x and y columns in our GeoDataFrame.
#
#The third step, is to convert our DataFrame into a format that Bokeh can understand. 
#Thus, we will convert our DataFrame into ColumnDataSource which is a Bokeh-specific 
#way of storing the data.
#
#Note
#
#Bokeh ColumnDataSource do not understand Shapely geometry -objects. Thus, we need
# to remove the geometry -column before convert our DataFrame into a ColumnDataSouce.
#Let’s make a copy of our points GeoDataFrame where we drop the geometry column.

# Make a copy and drop the geometry column
p_df = points.drop('geometry', axis=1).copy()

# See head
p_df.head(2)

from bokeh.models import ColumnDataSource

# Point DataSource
psource = ColumnDataSource(p_df)

# What is it?
psource


#Okey, so now we have a ColumnDataSource object that has our data stored in a way 
#that Bokeh wants it.
#
#Finally, we can make a Point map of those points in a fairly similar manner as 
#in the first example. Now instead of passing the coordinate lists, we can pass 
#the data as a source for the plot with column names containing those coordinates.

# Initialize our plot figure
p = figure(title="A map of address points from a Shapefile")

# Add the points to the map from our 'psource' ColumnDataSource -object
p.circle('x', 'y', source=psource, color='red', size=10)

#Great it worked. Now the last thing is to save our map as html file into our computer.

# Output filepath
outfp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\point_map.html"

# Save the map
save(p, outfp)

#Now you can open your point map in the browser in a similar manner as in the 
#previous example. Your map should look like following:

    
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

from bokeh.models import HoverTool
#Next, we need to initialize our tool.

my_hover = HoverTool()
#Then, we need to tell to the HoverTool that what information it should show to us. 
#These are defined with tooltips like this:

my_hover.tooltips = [('Address of the point', '@address')]
#From the above we can see that tooltip should be defined with a list of tuple(s) 
#where the first item is the name or label for the information that will be shown, 
#and the second item is the column-name where that information should be read in 
#your data. The @ character in front of the column-name is important because it 
#tells that the information should be taken from a column named as the text that 
#comes after the character.

#Lastly we need to add this new tool into our current plot.

p.add_tools(my_hover)
#Great! Let’s save this enhanced version of our map as point_map_hover.html and see the result.

# File path
outfp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\point_map_hover.html"

save(p, outfp)

#As you can see now the plot shows information about the points and the content 
#is the information derived from column address.
#
#Hint
#
#Of course, you can show information from multiple columns at the same time. This 
#is achieved simply by adding more tooltip variables when defining the tooltips, such as:

#==============================================================================
# my_hover2.tooltips = [('Label1', '@col1'), ('Label2', '@col2'), ('Label3', '@col3')]
#==============================================================================
 
 
#==============================================================================
# Line map
# Okey, now we have made a nice point map out of a Shapefile. Let’s see how we 
# can make an interactive map out of a Shapefile that represents metro lines in 
# Helsinki. We follow the same steps than before, i.e. 1) read the data, 2) 
#     calculate x and y coordinates, 3) convert the DataFrame into a 
#     ColumnDataSource and 4) make the map and save it as html.
#==============================================================================

#Read the data using geopandas which is the first step.

import geopandas as gpd

# File path
metro_fp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\metro.shp"

# Read the data
metro = gpd.read_file(metro_fp)
#Let’s see what we have.

metro.head()


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
        
#Note
#
#Wondering about what happens here? Take a tour to our earlier materials about LineString attributes. By default Shapely returns the coordinates as a numpy array of the coordinates. Bokeh does not understand arrays, hence we need to convert the array into a list which is why we apply list() -function.
#Let’s now apply our function in a similar manner as previously.

# Calculate x coordinates of the line
metro['x'] = metro.apply(getLineCoords, geom='geometry', coord_type='x', axis=1)

# Calculate y coordinates of the line
metro['y'] = metro.apply(getLineCoords, geom='geometry', coord_type='y', axis=1)

# Let's see what we have now
metro.head() 


#The third step. Convert the DataFrame (without geometry column) into a ColumnDataSource 
#which, as you remember, is a Bokeh-specific way of storing the data.

# Make a copy and drop the geometry column
m_df = metro.drop('geometry', axis=1).copy()

# Point DataSource
msource = ColumnDataSource(m_df)
#Finally, we can make a map of the metro line and save it in a similar manner 
#as earlier but now instead of plotting circle we need to use a .multiline() -object.
#Let’s define the line_width to be 3.

# Initialize our plot figure
p = figure(title="A map of the Helsinki metro")

# Add the lines to the map from our 'msource' ColumnDataSource -object
p.multi_line('x', 'y', source=msource, color='red', line_width=3)

# Output filepath
outfp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\metro_map.html"

# Save the map
save(p, outfp)
#Now you can open your point map in the browser and it should look like following: 

    
#==============================================================================
# Todo
# 
# Task:
# 
# As you can see we didn’t apply HoverTool for the plot. Try to apply it yourself and use a column called NUMERO from our data as the information.
# Polygon map with Points and Lines
#==============================================================================

#It is of course possible to add different layers on top of each other. 
#Let’s visualize a map showing accessibility in Helsinki Region and place 
#a metro line and the address points on top of that.

#1st step: Import necessary modules and read the Shapefiles.

from bokeh.plotting import figure, save
from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper
import geopandas as gpd
import pysal as ps

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

#2nd step: Let’s now apply the functions that we have created and parse the 
#x and y coordinates for all of our datasets.


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
pt_classif = grid[['pt_r_tt']].apply(classifier)

# Rename the classified column
pt_classif.columns = ['pt_r_tt_ud']

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
from bokeh.palettes import RdYlBu11 as palette
from bokeh.models import LogColorMapper

# Create the color mapper
color_mapper = LogColorMapper(palette=palette)
#Now we are ready to visualize our polygons and add the metro line and the 
#points on top of that. Polygons are visualized using patches objects in Bokeh.

# Initialize our figure
p = figure(title="Travel times with Public transportation to Central Railway station")

# Plot grid
p.patches('x', 'y', source=gsource,
         fill_color={'field': 'pt_r_tt_ud', 'transform': color_mapper},
         fill_alpha=1.0, line_color="black", line_width=0.05)

# Add metro on top of the same figure
p.multi_line('x', 'y', source=msource, color="red", line_width=2)

# Add points on top (as black points)
p.circle('x', 'y', size=3, source=psource, color="black")

# Save the figure
outfp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment5\data\travel_time_map.html"
save(p, outfp)


#Cool, now we have an interactive map with three layers! As you see, this map 
#does not yet have the same functionalities as the map on top of this page and 
#we won’t go into details how to do them now. If you are interested how to make 
#such a map, you can read the docs for producing advanced bokeh map from here.
#
#Now we move forward to see how we can share interactive maps on GitHub.