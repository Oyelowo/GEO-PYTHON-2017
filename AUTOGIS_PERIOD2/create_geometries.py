# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 15:10:55 2017

@author: oyeda
"""
from shapely.geometry import Point, LineString, Polygon
#Problem 1: Creating basic geometries

#Write your codes into a single create_geometries.py -file and upload the script
#to your personal GitHub Exercise-1 repository.

#Create a function called createPointGeom() that has two parameters (x_coord, y_coord). 
#Function should create a shapely Point geometry object and return that. Demonstrate 
#the usage of the function by creating Point -objects with the function.

def createPointGeom(x_coord, y_coord):
    """
    function to create a shapely point geometry object
    """
    point1 = Point(x_coord, y_coord)
    return point1

#Create a function called createLineGeom() that takes a list of Shapely Point 
#objects as parameter and returns a LineString object of those input points. 
#Function should first check that the input list really contains Shapely Point(s).
#Demonstrate the usage of the function by creating LineString -objects with the function.
def createLineGeom(point_lists):
    """
    function to create a shapely Line geometry object
    """
    for i in  point_lists:
        if type(i)!= Point:
            return
    
    LS = LineString(point_lists)  
    return LS

#Create a function called createPolyGeom() that takes a list of coordinate tuples
#OR a list of Shapely Point objects and creates/returns a Polygon object of the 
#input data. Both ways of passing the data to the function should be working. 
#Demonstrate the usage of the function by passing data first with coordinate-tuples 
#and then with Point -objects.

def createPolyGeom(point_lists):
    
        if len(point_lists)<3:
            return
        elif len(point_lists)>=3:
            poly=Polygon([[p.x, p.y] if type(p)==Point else [p[0],p[1]] for p in point_lists])
            return poly
        

