# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 01:18:49 2017

@author: oyeda
"""


import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import osmnx as ox
import networkx as nx
from shapely.geometry import box
#import numpy as np
#from UliEngineering.Math.Coordinates import BoundingBox


fp= r'C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment7'
orig = pd.read_csv(fp+"\origins.txt", sep=",")
dest= pd.read_csv(fp+"\destinations.txt", sep=",")


# =============================================================================
# Problem 1 (8 points)
# 
# There exists two csv-files in the /data folder. The files contain coordinates 
# of the origin and destination points in certain area in the world.
# 
# In the first problem you should:
# 
# Find out the area where the points are located.
# Where are points located (name of the region)? Write your answer here:
# Retrieve OpenStreetMap data (streets that can be driven with car) from the area
#  where the points are located
# Using the UTM projection: Plot the street network (gray color) and on top of 
# that the origin points with red color and destination points with blue color.
# Upload your script and the figure that you visualized to your own GitHub 
# repository for Exercise 7.
# =============================================================================



#orig = gpd.GeoDataFrame(orig)
orig['geometry']= ''

#for idx, rows  in orig.iterrows():
#    #print(rows['x'],rows['y'] )
#    rows['geometry'] =  Point(rows['x'],rows['y'])
#    print(rows['geometry'])
   
for i in range(len(orig)):
    xy=Point(orig.iloc[i,orig.columns.get_loc('x')],orig.iloc[i,orig.columns.get_loc('y')])
    #or simply as below. i only use the above, incase the column number changes
    #xy=Point(data_k.iloc[i,1],data_k.iloc[i,0])
    orig.loc[i,'geometry']=xy




#dest = gpd.GeoDataFrame(dest)
dest['geometry']= ''

#for idx, rows  in orig.iterrows():
#    #print(rows['x'],rows['y'] )
#    rows['geometry'] =  Point(rows['x'],rows['y'])
#    print(rows['geometry'])
   
for i in range(len(dest)):
    xy=Point(dest.iloc[i,dest.columns.get_loc('x')],dest.iloc[i,dest.columns.get_loc('y')])
    #or simply as below. i only use the above, incase the column number changes
    #xy=Point(data_k.iloc[i,1],data_k.iloc[i,0])
    dest.loc[i,'geometry']=xy
    
orig_dest = orig.append(dest)
orig_dest= orig_dest.reset_index(drop=True)

#convert to geodataframe and select geometry as the geometry column
orig_dest=gpd.GeoDataFrame(orig_dest, geometry="geometry")


#find the bounding box
orig_dest.bounds.head()

#this creates like a somewhat polygon which is the ounding box geometry
bbox = box(*orig_dest.unary_union.bounds)

#check for the area
bbox.area
print(bbox.representative_point)
import folium

# Create a Map instance
m = folium.Map(location=(orig.y[3], orig.x[3]) , tiles='Stamen Toner',
                   zoom_start=11, control_scale=True , prefer_canvas=True)
m.save(fp+"/area_of_interest.html")


#create a bounding box with buffer of 0.02km. This is because the shortest path could be
#along outside of the bounding box
bbox_buf=bbox.buffer(0.06)

#show
bbox_buf
#print(bbox)

#Okey so now we have retrieved only such streets where it is possible to drive 
#with a car. Let’s confirm this by taking a look at the attributes of the street network. 
#Easiest way to do this is to convert the graph (nodes and edges) into GeoDataFrames

#create the box from the points
graph= ox.graph_from_polygon(bbox_buf, network_type="drive")
#graph2= ox.graph_from_place("Tallinn", network_type="drive")
#type(graph)


#Get the nodes from the graph that has not been reprojected. This will be useful when setting
#the initial crs of the origins and destinations
nodes_not_repro = ox.graph_to_gdfs(graph, edges=False)
nodes_not_repro.crs

#Okey, now we can confirm that as a result our street network indeed only contains 
#such streets where it is allowed to drive with a car as there are no e.g. 
#cycleways of footways included in the data. We can also see that the CRS of 
#the GeoDataFrame seems to be WGS84 (i.e. epsg: 4326).
#
#Let’s continue and find the shortest path between two points based on the distance. 
#As the data is in WGS84 format, we might first want to reproject our data into 
#metric system so that our map looks better. Luckily there is a handy function 
#in osmnx called project_graph() to project the graph data in UTM format.
#checkk what's in the highway column

graph_proj =ox.project_graph(graph)
#graph_proj2 =ox.project_graph(graph2)
#graph.crs
#graph_proj.crs

nodes_proj, edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=True)
#nodes_proj, edges_proj = ox.graph_to_gdfs(graph_proj, edges=True)
nodes_proj[['x', 'y']]
nodes_proj.crs

#fig, ax=ox.plot_shape(graph)
fig, ax = ox.plot_graph(graph_proj)
plt.tight_layout()

#If you want edges alone.
#edges = ox.graph_to_gdfs(graph_proj, nodes=False, edges=True)

#checkwhat is in the columns
edges_proj.columns

#check the coordinate system if it has been reprojected
edges_proj.crs



#edges_proj['highway'].value_counts()



#check the data
edges_proj.head()
nodes_proj.head()

#dont reset their indexes because it will be needed agaain when we need the nodes id as index. 
#otherwise, they have to be reset.
#nodes_proj = nodes_proj.reset_index(drop=True)

len(orig)
len(dest)


#now, we can use the crs of the nodes that had not been reprojected earlier, to set the initial
#crs of the origins and destinations, as they are also in WGS 84, which was used to build
#the bounding box for the initial graph which had not been reprojected. 
#it is important to set this initial crs before converting because the coordinates are in
#'epsg:4326'
orig_gpd=gpd.GeoDataFrame(orig, geometry="geometry", crs=nodes_not_repro.crs)
orig_gpd.crs


#from fiona.crs import from_epsg

#Do thesame for the destination
dest_gpd=gpd.GeoDataFrame(dest, geometry="geometry", crs=nodes_not_repro.crs)

#the aove can also be done manaully when creating the geodataframae but I prefer the more
#automatic way because it geets te crs directly and one does not have to search and type manually
#dest_gpd=gpd.GeoDataFrame(dest, geometry="geometry", crs={'init': 'epsg:4326'})
dest_gpd.crs


#now, we can reproject to the  origins and destinations in UTM format to align 
#with the reprojected graph.
orig_proj = ox.project_gdf(orig_gpd)
dest_proj = ox.project_gdf(dest_gpd)
orig_proj.x
#check the crs
orig_proj.crs
dest_proj.crs


#The reprojection can be also been done  as shown below.
orig_proj2 = orig_gpd.to_crs(crs=nodes_proj.crs)
dest_proj2 = dest_gpd.to_crs(crs=nodes_proj.crs)

#let's see buildings too
#buildings= ox.buildings_from_polygon(bbox)

#reproject the buildings.
#buildings_proj = buildings.to_crs(crs=nodes_proj.crs)
#buildings_proj.crs

#plot the graph without nodes(edges only)
fig, ax=ox.plot_graph(graph_proj, node_alpha=0)

#add the origin nodes
orig_proj.plot(ax=ax, color="red", linewidth=1.5, zorder=5)

#add the destination nodes
dest_proj.plot(ax=ax, color="blue", linewidth=2.5, zorder=10)
#dest_proj.plot(ax=ax, markersize=24, color='blue')

#buildings_proj.plot(ax=ax, facecolor='khaki', alpha=0.7)
plt.tight_layout()

#save
plt.savefig(fp + '\origins_and_destinations.png')



# =============================================================================
# #result = pd.merge(nodes_proj, orig_gpd, left_on=['lon', 'lat'], right_on['x','y'])
# #origi=[]
# #cc=zip(nodes_proj,orig_gpd)
# #
# #for i,j in zip(nodes_proj,orig_gpd):
# #    print(j)
# #
# #for idx, rows in nodes_proj.iterrows():
# #for idx2,rows2 in orig_gpd.iterrows():
# ##for idx, rows in nodes_proj.iterrows():
# #    print(idx2)
#         
# 
# #Using the UTM projection: Plot the street network (gray color) and on top of 
# #that the origin points with red color and destination points with blue color.
# 
# #plot it
# #fig, ax = plt.subplots()
# #edges_proj.plot(ax=ax, linewidth=0.75, color='gray')
# #
# #nodes_proj.plot(ax=ax, markersize=2, color='red')
# #
# #buildings_proj.plot(ax=ax, facecolor='khaki', alpha=0.7)
# #
# #
# #route_geom.plot(ax=ax, linewidth=4, linestyle='--', color='red')
# #
# #
# #od_points.plot(ax=ax, markersize=24, color='green')
# 
# =============================================================================


# =============================================================================
# Problem 2 (12 points)
# In this problem we practice conducting shortest path routing.
# 
# In the second problem you should:
# 
# Calculate the shortest paths between all origin points (16) and destination 
# points (20) using the distance of the road segments as the impedance measure 
# (in total 320 routes).
# 
# Create a GeoDataFrame where you should store all the LineString geometries of 
# the shortest path routes, and the distance of the route in meters.
# 
# Plot all the routes on top of the street network.
# 
# Calculate the total distance of all the routes (i.e. sum of all route distances)
# 
# What is the total distance of all routes? Answer here:
# Upload your script and the figure that you visualized to your own GitHub 
# repository for Exercise 7.
# =============================================================================


#Now copy dest and orig
origCopy = orig_proj.copy()
destCopy = dest_proj.copy()

#origCopy.geometry.x
ori_nodes=[]
distance=[]
for i,rows in origCopy.iterrows():
    #get the distance of the points to the nodes too. but without returning the distance
    #one object could be specified to avoid getting the nodes as list of nodes and distance of
    #points to nodes too. but here, i want to return the nearest nodes and the distance of points
    #to the nearest nodes
    yx, dist=ox.get_nearest_node(graph_proj, (rows.geometry.y, rows.geometry.x), method='euclidean', return_dist=True)
    ori_nodes.append(yx)
    distance.append(dist)
    
origCopy['orig_nodes']=ori_nodes
origCopy['dist_orig_node'] = distance


dest_nodes=[]
distance2=[]
for i,rows in destCopy.iterrows():
    yx, distance2=ox.get_nearest_node(graph_proj, (rows.geometry.y, rows.geometry.x), method='euclidean', return_dist=True)
    dest_nodes.append(yx)
 
destCopy['dest_nodes']=dest_nodes
destCopy['dist_dest_nodes']=distance2

#destCopy['geometry']



#create a key to merge one to all
origCopy['key']= 1
destCopy['key']= 1

#merge to a new dataframe
orig_dest_all=pd.merge(origCopy, destCopy, on="key")

#orig_dest_all= gpd.GeoDataFrame(orig_dest_all, crs=nodes_proj.crs)
orig_dest_all.crs

#rou = nx.shortest_path(G=graph_proj, source=oo, target=xc, weight='length')
#od_nodes = gpd.GeoDataFrame([o_closest, t_closest], geometry='geometry', crs=nodes_proj.crs)    

routes=[]
for i,rows in orig_dest_all.iterrows():
    #use distance as the impedance instead of length
    rou = nx.shortest_path(G=graph_proj, source=rows['orig_nodes'], target=rows['dest_nodes'], weight='distance')
    routes.append(rou)
orig_dest_all['routes']=routes


#i first had issue with an origin and destinationsharing similar nearest node
#and couldnt create a route or  lineString from it. I used this to check
#for that row.
#for i in routes:
#    if(len(i)==1):
#        print(i)
        
    


# =============================================================================
# #beacause the index had been reset earlier, I have to set the osmid as the index
# #with this, Ican locate the nodes with that id
# #nodes_proj_osmid = nodes_proj.set_index('osmid')
# =============================================================================


# =============================================================================
# for i in range(len(routes)):
#     yy=LineString(list(nodes_proj.loc[routes[i]].geometry.values))
#     orig_dest_all.iloc[i, 'distances']=yy
#     
#     yy=nodes_proj.loc[routes[i]]
#     route_geom.loc[0, 'geometry'] = route_line
# =============================================================================

ls=[]
dist=[]
for i, rows in orig_dest_all.iterrows():
#    aa=rows['routes']
    each_route=rows.routes
    if len(each_route)==1:
        each_line=0
        ls.append(each_line)
        dist.append(0)
    else:
        each_line=LineString(list(nodes_proj.loc[each_route].geometry.values))
        ls.append(each_line)
        dist.append(each_line.length)
#len(dist)
#len(ls)       
orig_dest_all['line_geom']=ls
orig_dest_all['dist_geom']=dist


# =============================================================================
#This could be used to calculate the distance separately but has been included 
#already in the first loop
# dist=[]
# for i, rows in orig_dest_all.iterrows():
#     if rows.line_geom==0:
#         dist.append(0)
#     else:
#         each_dist= rows.line_geom.length
#         dist.append(each_dist)
#         print(dist)
#orig_dest_all['dist_geom']=dist
# =============================================================================
        
#insert the distance of each line string




line_geom=gpd.GeoDataFrame(orig_dest_all,geometry='line_geom')

#create 319 different colours for the lines
color_map=ox.plot.get_colors(319, cmap='viridis', start=0.0, stop=1.0, alpha=1.0, return_hex=False)

fig, ax = ox.plot_graph(graph_proj, node_alpha=0)
line_geom.plot(ax=ax, color=color_map)
#line_geom.plot(ax=ax, color='green')

orig_proj.plot(ax=ax, color="red", linewidth=0.02, zorder=5)

#add the destination nodes
dest_proj.plot(ax=ax, color="blue", linewidth=0.03, zorder=10)
#dest_proj.plot(ax=ax, markersize=24, color='blue')'

plt.title("Shortest Route analysis")

plt.tight_layout()
plt.savefig(fp + '\shortest_paths.png')

#Calculate the total distance
all_dist=sum(orig_dest_all['dist_geom'])

print('The total distance of all the routes (i.e. sum of all route distances) is {0}m'.format(round(all_dist,2)))





# =============================================================================
# 
# for i, rows in orig_dest_all.iterrows():
#     fig, ax = ox.plot_graph(graph_proj, node_alpha=0)
#     ax = ox.plot_graph_route(graph_proj, rows['routes'])
#     
#     plt.tight_layout()
# =============================================================================
    
  

# =============================================================================
#Check this later. Should also work as expected.
# list_ori_nodes=[]
##orig_dest_all['orig_nodes'] =''
# for i in range(len(orig_dest_all)):
#     yx= ox.get_nearest_node(graph_proj, (orig_dest_all.iloc[i,orig_dest_all.columns.get_loc('y_x')],orig_dest_all.iloc[i,orig_dest_all.columns.get_loc('x_x')]), method='euclidean',  return_dist=True)
#     #orig_dest_all['orig_nodes']= yx
#     list_ori_nodes.append(yx)
#     
#      list_dest_nodes=[]
# #orig_dest_all['orig_nodes'] =''
# for i in range(len(orig_dest_all)):
#     yx= ox.get_nearest_node(graph_proj, (orig_dest_all.iloc[i,orig_dest_all.columns.get_loc('y_y')],orig_dest_all.iloc[i,orig_dest_all.columns.get_loc('x_y')]), method='euclidean',  return_dist=True)
#     #orig_dest_all['orig_nodes']= yx
#     list_dest_nodes.append(yx)
## =============================================================================

