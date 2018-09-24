# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 09:05:48 2017

@author: oyeda
"""

#==============================================================================
# In the first problem the aim is to find out the addresses of shopping centers 
# and geocoding them as a single Shapefile called shopping_centers.shp.
# 
# Steps
# 
# From the internet find out the addresses for following shopping centers and 
# write the addresses into a text file called shopping_centers.txt:
# 
# Itis
# 
# Forum
# 
# Iso-omena
# 
# Sello
# 
# Jumbo
# 
# REDI (i.e. use the metro station of Kalasatama)
# 
# Use same kind of formatting for the text file as in the lesson materials, 
# thus use semicolon ; as a separator and add a unique integer number as id 
# (doesn't matter what) for each center.
# 
# Geocode the addresses in Geopandas in a similar manner as was done in the lesson materials
# 
# Reproject the geometries into a EPSG projection 3879 similarly as in lesson materials
# 
# Notice: you need to pass the coordinate information as a proj 4 dictionary in a 
# similar manner as in the lesson materials (see the second last bullet point in the lesson materials
# Make a Table join to retrieve the id column from original shopping centers 
# DataFrame similarly as in lesson materials
# 
# Save the GeoDataFrame as a Shapefile called shopping_centers.shp
#==============================================================================

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

fpath=r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment3\shopping_centres.txt"
data = pd.read_csv(fpath, sep=";", encoding='latin-1')

data.head(5)
from geopandas.tools import geocode
geoc= geocode(data['addre'], provider='nominatim')
geoc

from fiona.crs import from_epsg
geoc=geoc.to_crs(from_epsg(3879))
#it can also be done as below:
#geoc['geometry']= geoc['geometry'].to_crs(epsg=3879)
geoc.crs
geoc_join= geoc.join(data)
type(geoc)

fp=r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment3\shopping_centres.shp"
geoc_join.to_file(fp)
#geoc_join.plot()


#==============================================================================
# 
# Problem 2: Create buffers around shopping centers (5 points)
# 
# Let's continue with our case study and calculate a 5 km buffer around the points.
# 
# Steps
# 
# Create a new column called buffer to your shopping-centers GeoDataFrame (or whatever you call it)
# 
# Iterate over the rows in your GeoDataFrame and update the buffer column with a 5 km buffer Polygon.
# 
# Use Shapely's buffer function to create it (see the link for details how to use it)
# You only need to use the distance -parameter, don't care about the other parameters.
# Replace the values in geometry column with the values of buffer column
#==============================================================================

#copy the  geocoded data into shops

shops= geoc_join.copy()
shops['buffer']= ''

#from shapely.geometry import CAP_STYLE, JOIN_STYLE

for idx, rows in shops.iterrows():
    poly= rows['geometry'].buffer(5000)
    shops.loc[idx, 'buffer'] = poly


#This is a more straightforward way of updating the buffer column    
shops['buffer']= shops['geometry'].buffer(5000)
    
#==============================================================================
#Aalternative way. but here you would ave to add the list into the new buffer column
# xx=[]
# for idx, rows in shops.iterrows():
#     poly= rows['geometry'].buffer(5000)
#     xx.append(poly)
#==============================================================================
#==============================================================================
#The geometry colum can be updated straighytup, it is safer to fisrst create the buffer columnm
# for idx, rows in shops.iterrows():
#     poly= rows['geometry'].buffer(5000)
#     shops.loc[idx, 'geometry'] = poly
#==============================================================================
    
#update the geometry column using the buffers
shops['geometry']=shops['buffer']

#delete the buffer column
del shops['buffer']
type(shops)



#==============================================================================
# Problem 3: How many people live within 5 km from shopping centers? (5 points)
# 
# Last step in our analysis is to make a spatial join between our point-buffer layer and the same population grid that was used in the lesson materials.
# 
# Steps
# 
# Read and prepare the population grid into a GeoDataFrame similarly as in the lesson materials
# 
# Make a spatial join between your buffered point layer and population grid layer
# 
# Note: Join the information now from buffer layer into the population grid layer
# Group the joined layer by shopping center index
# 
# Calculate the sum of population living within 5 km for each shopping center.
# 
# Write the answers down here into the Answers section
#==============================================================================

#import the population grid
fpa=r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment3\pop_grid\Vaestotietoruudukko_2015.shp"

#read the population grid shapefile
pop_grid= gpd.read_file(fpa)
#pop_grid.plot()

#change the name of the column 'ASUKKAITA' to population
pop_grid=pop_grid.rename(columns={'ASUKKAITA':'population'})

#select theopulation and geometry columns from the populatin grid dataframe

pop_grid2=pop_grid[['population', 'geometry']]

#reproject the pop_grid2 to have thesame crs as the shops dataframe
pop_grid2=pop_grid2.to_crs(shops.crs)

#confirm the reprojection
pop_grid2.crs



#make a spatial join between the pop_grid2 and the shops with geometry as its buffer
pop_shops_buf= gpd.sjoin(pop_grid2, shops, how='inner', op='within')

pop_shops_buf.plot()

pop_shops_group= pop_shops_buf.groupby('addre')

pop_total=gpd.GeoDataFrame()
pop_total['pop_sum']=''


for key, group in pop_shops_group:
     t=sum(group['population'])
     pop_total.loc[key, 'pop_sum']=t
     pop_total.loc[key,'shops']=key
     pop_total.loc[key, 'shops_name']=(group['shops']).unique()
     pop_total=pop_total.reset_index(drop=True)
     
#     for idx, rows in group.iterrows():
#         xx=rows['shops']
#         print(xx)
#         pop_total.loc[key, 'shops_name']=xx

   

#==============================================================================
# Problem 4: What is the closest shopping center from your home / work? (5 points)
# 
# In the last problem you should find out the closest shopping center from 
# a) your home and b) work locations.
# 
# Steps:
# 
# Create a txt-file called activity_locations.txt 
# (use same formatting as in Problem 1) with two columns:
# 
# id --> unique number (e.g. 0 and 1)
# addr --> address of your work and home (you don't need to reveal your home / 
# work if you don't want to, these can be whatever two addresses from Helsinki!)
# Read those addresses into Pandas and convert the addresses to Point objects 
# using the geocoding functionalities of Geopandas
# 
# Find out the nearest shopping center to these points using the techniques shown
# during the lesson. You can use the shopping center addresses you geocoded in Problem 1.
#==============================================================================

fpa=r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment3\activity_locations.txt"
my_places= pd.read_csv(fpa, sep=';',encoding='latin')

my_places_geoc=geocode(my_places['addre'], provider='nominatim')

my_places_geoc=my_places_geoc.join(my_places)

#the data for the shopping centres
shops_c = geoc_join.copy()

#reproject the data into second dataframe
my_places_geoc = my_places_geoc.to_crs(shops_c.crs)

from shapely.geometry import MultiPoint
from shapely.ops import nearest_points


#hh=pd.DataFrame()
#hh['geometry']=''
#hh['geometry']= my_places_geoc['geometry']
#hhh=my_places_geoc.ix[my_places_geoc['place']=='home']
#hhh=hhh['geometry'].iloc[0]

#the first part selects the dataframe based on column place with rows called 'names',
home = my_places_geoc.loc[my_places_geoc['place']=='home']
#home = my_places_geoc.ix[my_places_geoc['place']=='home']['geometry']

#this selects the point from the above
home_geom=home['geometry'].iloc[0]

dest_geom=MultiPoint(shops_c['geometry'])

#find the nearest points
nearest_home_shops = nearest_points(home_geom, dest_geom)

home_closest=shops_c.loc[shops_c['geometry']==nearest_home_shops[1]]['shops'].iloc[0]
print('{0} is the closest shopping centre to my home.'.format(home_closest.upper()))

#This is to confirm that I used my home as the origin
home_address=my_places_geoc.loc[my_places_geoc['geometry']==nearest_home_shops[0]]['address'].iloc[0]
print('The full address of my home is: {0}'.format(home_address.upper()))


#select the geometry of my work
work_geom= my_places_geoc.loc[my_places_geoc['place']=='work']['geometry'].iloc[0]
print('{0} is the coordinate of my work'.format(work_geom))

#find the nearest shopping centre to my work
nearest_work_shops = nearest_points(work_geom, dest_geom)
work=nearest_work_shops[0]
nearest_shop=nearest_home_shops[1]
#check the closest shop based on the index of the closest shop at [1]. 
#i.e nearest_work_Shops[1]
shop_to_work=shops_c.loc[shops_c['geometry']== nearest_shop]['shops'].iloc[0]
#shop_to_work=shops_c.loc[shops_c['geometry']== nearest_work_shops[1]]['shops'].iloc[0]
print('{0} is the closest shopping centre to my work'.format(shop_to_work))


#Check if the index 0 of the nearest_work_shops is my work(school)
work_address= my_places_geoc.loc[my_places_geoc['geometry']==work][['place', 'address']].iloc[0,1]
#work_address= my_places_geoc.loc[my_places_geoc['geometry']==nearest_work_shops[0]][['place', 'address']].iloc[0,1]
print('The full address of my work is {0}'.format(work_address.upper()))

my_work=my_places_geoc.loc[my_places_geoc['geometry']==nearest_work_shops[0]][['place', 'address']].iloc[0,0]
print('This is my {0}'.format(my_work))



