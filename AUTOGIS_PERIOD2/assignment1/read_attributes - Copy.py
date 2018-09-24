# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 17:14:34 2017

@author: oyeda
"""
from shapely.geometry import Point, LineString, Polygon, MultiPoint
#Write your codes into a single read_attributes.py -file and upload the script 
#to your personal GitHub Exercise-1 repository.

#Create a function called getCentroid() that takes any kind of Shapely's 
#geometric -object as input and returns a centroid of that geometry. 
#Demonstrate the usage of the function.
def getCentroid(obj):
    obj_centroid = obj.centroid
    return obj_centroid

#Create a function called getArea() that takes a Shapely's Polygon -object as 
#input and returns the area of that geometry. Demonstrate the usage of the function.
def getArea(obj):
    obj_area = obj.area
    return obj_area


#Create a function called getLength() takes either a Shapely's LineString or 
#Polygon -object as input. Function should check the type of the input and 
#returns the length of the line if input is LineString and length of the exterior
# ring if input is Polygon. If something else is passed to the function, 
# it should tell the user --> "Error: LineString or Polygon geometries required!".
# Demonstrate the usage of the function.
def getLength(obj):
    if type(obj)== LineString:
        len_obj = obj.length
        return len_obj
    elif type(obj)== Polygon:
        len_obj = obj.exterior.length
        return len_obj
    else:
        print("Error: LineString or Polygon geometries required!")
 
        
        
        
#For testing     
point1 = Point(2.2, 4.2)

point2 = Point(7.2, -25.1)

point3 = Point(9.26, -2.456)
line = LineString([point1, point2, point3])
line
poly = Polygon([point1, point2, point3])
poly = Polygon([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])
poly

getLength(point1)







