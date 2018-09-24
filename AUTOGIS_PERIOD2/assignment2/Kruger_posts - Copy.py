# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 08:51:43 2017

@author: oyeda
"""
#==============================================================================
# 
# Problem 2: Points to map (6 points)
# 
# The problem 2 this week continues the process that we started last week, i.e. 
# creating geometric point -objects and putting them into a map. Here our aim is 
# to plot a set of x and y coordinates that we should read from a some_posts.csv 
# comma separated file that contains following kind of data:
# 
# lat,lon,timestamp,userid
# -24.980792492,31.484633302,2015-07-07 03:02,66487960
# -25.499224667,31.508905612,2015-07-07 03:18,65281761
# -24.342578456,30.930866066,2015-03-07 03:38,90916112
# -24.85461393,31.519718439,2015-10-07 05:04,37959089
# The data has 81379 rows and consists of locations and times of social media 
# posts inside Kruger national park in South Africa:
# 
# Column	Description
# lat	y-coordinate of the post
# lon	x-coordinate of the post
# timestamp	Time when the post was uploaded
# userid	userid
# Note: although the data is based on real social media data, it is heavily 
# anonymized. Userids and timestamps have been randomized, i.e. they do not not 
# match with real ones, also spatial accuracy of the data have been lowered.
# 
# Download the data (Click on the link ==> CNTRL + S)
# Read the data into memory using Pandas
# Create an empty column called geometry where you will store shapely Point objects
# Iterate over the rows of the DataFrame and insert Point objects into column geometry 
# (you need to use .loc indexer to update the row, see materials
# Convert that DataFrame into a GeoDataFrame, see hints
# Update the CRS for coordinate system as WGS84 (i.e. epsg code: 4326)
# Save the data into a Shapefile called Kruger_posts.shp
# Create a simple map of those points using a GIS software or using .plot() -funtion 
# in Python. Save it to GitHub as png file.
#==============================================================================

import pandas as pd
from shapely.geometry import Point, Polygon, LineString
import geopandas as gpd
file = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment2\some_posts.txt"
data_k = pd.read_csv(file, sep=',', parse_dates=['timestamp'])

data_k['geometry']= None
data_k.head(n=6)

#n=[]
#for i, row in data_k.iterrows():
#    m=Point(row['lon'], row['lat'])
#    n.append(m)
#    

for i in range(len(data_k)):
    xy=Point(data_k.iloc[i,data_k.columns.get_loc('lon')],data_k.iloc[i,data_k.columns.get_loc('lat')])
    #or simply as below. i only use the above, incase the column number changes
    #xy=Point(data_k.iloc[i,1],data_k.iloc[i,0])
    data_k.loc[i,'geometry']=xy

from fiona.crs import from_epsg

#convert the dataframe into geoDataframe
geodata_k = gpd.GeoDataFrame(data_k, geometry='geometry', crs=from_epsg(4326))

#==============================================================================
# This is not necessary, just saving for reference purpose
# import os
# filepath=r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment2\kruger_posts\kruger_posts"
# if not os.path.exists(filepath):
#     os.makedirs(filepath)
# filename='kruger_posts.shp'
# a=os.path.join(filepath, filename)
#==============================================================================

filepath=r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment2\kruger_posts\kruger_posts.shp"
geodata_k.to_file(filepath)

geodata_k.plot()



#==============================================================================
# Problem 3: How long distance individuals have travelled? (8 points)
# 
# In this problem the aim is to calculate the distance in meters that the individuals
#  have travelled according the social media posts (Euclidian distances between points).
# 
# Write your codes into the same file as in previous Problem (2).
# 
# In your code you should:
# 
# Reproject the data from WGS84 projection into EPSG:32735 -projection which stands
# for UTM Zone 35S (UTM zone for South Africa) to transform the data into metric system.
# Group the data by userid
# Create an empty GeoDataFrame called movements
# For each user:
# sort the rows by timestamp
# create LineString objects based on the points
# add the geometry and the userid into the GeoDataFrame you created in the last step
# Determine the CRS of the movements GeoDataFrame to EPSG:32735 (epsg code: 32735)
# Calculate the lenghts of the lines into a new column called distance in movements GeoDataFrame.
# Save the movements of into a Shapefile called Some_movements.shp
# 
#==============================================================================

#reproject data
geodata_k2 = geodata_k.to_crs(epsg=32735)

geodata_k2.tail(5)
data_k2 = data_k.copy()

#group the data by userid

grouped=geodata_k2.groupby('userid')
grouped
#create an emoty geodataframe called movements


#==============================================================================
# zz=pd.DataFrame(columns=['lat', 'lon', 'timestamp', 'userid', 'geometry'])
# geo
# for key, group in grouped:
#     zx=zz.loc(group.sort_values(by='timestamp'))
#     zz.append(group.sort_values(by='timestamp'))
#     
#     LineString(zz.iloc[:, zz.columns.get_loc('geometry')])
# 
#     
#==============================================================================
    
    
#grouped.count() 
    


#group =grouped.get_group(50136) 

movements =  gpd.GeoDataFrame()
movements['geometry']=''

userid=[]
#pointlist=[]
for key, group in grouped:
    pointlist=[] 
    userid.append(key)
    group = group.sort_values(by='timestamp')
    if len(group['geometry'])>1:
        for idx, row in group.iterrows():
            pointlist.append(row['geometry'])
        lines=LineString(pointlist)
        movements.loc[key, 'geometry']=lines
        #movements['userid']=userid
        































   

movements =  gpd.GeoDataFrame()
movements['geometry']=''
for key, group in grouped:
    cv=[] 
    group = group.sort_values(by='timestamp')
    if len(group)>1:
        for idx, row in group.iterrows():
            points= (row['geometry'])
            cv.append(points)
        zz=LineString(cv)
        movements.loc[key, 'geometry']=zz


movements = gpd.GeoDataFrame(movements, geometry='geometry', crs=from_epsg(32735))
movements['distance']=movements['geometry'].length

movements.plot()

        

#LineString(geodata_k2.iloc[:, geodata_k2.columns.get_loc('geometry')])    
    

#getting a a number in the data frame
#geodata_k2.iloc[3, geodata_k2.columns.get_loc('userid')]


