# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 12:33:42 2017

@author: oyeda
"""

#import necessary modules
from shapely.geometry import Point, Polygon
from fiona.crs import from_epsg
import geopandas as gpd
filepath=r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment2\Data\DAMSELFISH_distributions.shp"
data =  gpd.read_file(filepath)

#print the head
data.head


data.plot()

output_fp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment2\Data\DAMSELFISH_selection.shp"

#select data
selection = data[0:50]

#another way
#selection = data.head(50)

#or tail
#selection = data.tail(50)

#write data to disk
selection.to_file(output_fp)


#in pandas and geopandas, you need to use this iterrows instead of doing it directly

for idx, row in selection.iterrows():
    poly_area=row['geometry'].area
#:.3f is for the decimal place
    print("Polygon area at index{0} is: {1:.3f}".format(idx, poly_area))
    
    
selection['area'] =  selection.area

#get centroid
selection.centroid
    

#maximum or minimunm or mean area of the selected area
max_area = selection['area'].max()
minimum_area=selection['area'].min()
mean_area=selection['area'].mean()
#create an empty GeoDataframe

data2= gpd.GeoDataFrame()

data2['geometry']= None


coordinates = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]

poly= Polygon(coordinates)


#insert the polygon intp GeoDataframe
data2.loc[0, 'geometry'] = poly

type(data2)

data2.loc[0, 'Location'] = 'Senaantintori'

data2
data2.plot()

#wont print anything cos we havent specified anythig for the datafrme
data2.crs

#check for the previous which was defined
data.crs

#we need to specify the orojection information and the easiest wsay
#is to use the epsg

#check this: from_epsg(4326)
#now specify the coordinate reference system for data2
#from_epsg(4326): this is for the wgsb4 use for representing the longitude and latitude
data2.crs =  from_epsg(4326)


#export te data

outfp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment2\Data\Senaantintori"
data2.to_file = output_fp




#export fishes
grouped = data.groupby('binomial')
grouped


#
for key, rows in grouped:
    print(rows)
    break
key
type(key)    


#you can use replace command to replace the space beteeen the name
#key.replace

#
outdir =r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment2\Data\fishes"

#for passing the full path

import os


for key, rows in grouped:
    output_name = "{0}.shp".format(key.replace(' ', '_'))
    output_path = os.path.join(outdir, output_name)
    
    #incase i run into problem
    geo=gpd.GeoDataFrame(rows, crs =from_epsg(4326))
    rows.to_file(output_path)
    
