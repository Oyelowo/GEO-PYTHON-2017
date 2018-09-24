# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 18:14:05 2017

@author: oyeda
"""
import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString, Polygon, MultiPoint


#Problem 3: Reading coordinates from a file and creating a geometries

#Write your codes into a single file_coords_to_geom.py -file and upload the script
# to your personal GitHub Exercise-1 repository.

#One of the "classical" problems in GIS is the situation where you have a set of
#coordinates in a file and you need to get them into a map (or into a GIS-software).
#Python is a really handy tool to solve this problem as with Python it is basically
#possible to read data from any kind of input datafile (such as csv-, txt-, excel-,
#or gpx-files (gps data) or from different databases). So far, I haven't faced any
#kind of data or file that would be impossible to read with Python.

#Thus, let's see how we can read data from a file and create Point -objects from 
#them that can be saved e.g. as a new Shapefile (we will learn this next week). 
#Our dataset travelTimes_2015_Helsinki.txt consist of travel times between specific 
#locations in Helsinki Region. The first four rows of our data looks like this:
    
    
    
#Tasks

#Save the travelTimes_2015_Helsinki.txt into your computer.
#Read 4 columns, i.e. 'from_x', 'from_y', 'to_x', 'to_y' from the data into Python using Pandas.
#Create two lists called orig_points and dest_points
#Iterate over the rows of your numpy array and add Shapely Point -objects into the orig_points 
#-list and dest_point -list representing the origin locations and destination locations accordingly.
file=r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment1\travelTimes_2015_Helsinki.txt"
data = pd.read_csv(file, usecols=[5,6,7,8], sep=";" )
data.head()


orig_dest_points = pd.DataFrame(index=range(len(data)),columns=["ori", "des"])
for i in range(len(data)):
    origins = (Point(data.iloc[i,0], data.iloc[i, 1]))
    orig_dest_points.loc[i, 'ori']= origins
    destinations = (Point(data.iloc[i,2], data.iloc[i, 3]))
    orig_dest_points.loc[i, 'des']= destinations
    
origi= orig_dest_points[['ori']]
desti = orig_dest_points[['des']]

#THIS IS ANOTHER WAY OF DOING IT
origin = []
destination= []

for idx, row in data.iterrows():
    points_o = Point(row['from_x'], row['from_y'])
    origin.append(points_o)
    
    points_d = Point(row['to_x'], row['to_y'])
    destination.append(points_d)
    



#OBS: ITRIED SOME OTHER WAYS:
############################################################################
############################################################################
#for i in range(0,len(data)):
#    print(i)

#I also did in other ways

#for i in data:
#    orig_points= data[['from_y', 'from_x']].apply(tuple, axis=1)
#   
#    
#for i in data:
#    dest_points= data[['to_y', 'to_x']].apply(tuple, axis=1)
#    
#
#len(data)
#
#s=data.values #convert to array
#data.columns
#data.index
##Point(orig_points)
##Straightforward methods
#orig_points = []
#dest_points = []
#
#data['orig_points'] = list(zip(data.from_y, data.from_x))
#data['dest_points'] = list(zip(data.to_y, data.to_x))
#
#origi = []
#desti = []
#
#origi.append(data.loc[:,('from_y','from_x')].apply(tuple, axis=1))
#desti.append(data.loc[:,('to_y','to_x')].apply(tuple, axis=1))
#
#orig_points= list(zip(data.from_y, data.from_x))
#dest_points = list(zip(data.to_y, data.to_x))
#
#orig_points2 = []
#dest_points2 = []
#orig_points2=(data[['from_y', 'from_x']].apply(tuple, axis=1))
#dest_points2=(data[['to_y', 'to_x']].apply(tuple, axis=1))
#
