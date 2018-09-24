# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 12:36:10 2017

@author: oyeda
"""

##########################################################################
#GEOCODING
import pandas as pd
import geopandas as gpd
from geopandas.tools import geocode
import matplotlib.pyplot as plt
#from geopy.geocoders import Nominatim

fp=r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment3\addresses.txt"
data= pd.read_csv(fp, sep=";")

#Geocode the addresses
geo = geocode(data['addr'], provider='nominatim')

#Join the DataFrames together
geo = geo.join(data)
# exporting to shapefile works without the above join operation

#geo.plot()

#Save to disk
outfp= r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment3\addresses.shp"
geo.to_file(outfp)


#################################################################
#QUERIES
from shapely.geometry import Point, LineString, Polygon, MultiLineString
#to speedup the creation of points and shapes
import shapely.speedups
#enable it
shapely.speedups.enable()
#Create points
p1 = Point(24.952242, 60.1696017)
p2 = Point(24.976567, 60.1612500)

#Create a polygon
coords = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
poly = Polygon(coords)

#
p1.within(poly)
p2.within(poly)

poly.contains(p1)
poly.contains(p2)


#INTERSECT
line_a = LineString([(0, 0), (1, 1)])
line_b = LineString([(1, 1), (0, 2)])

#check if they intersect eachother
line_a.intersects(line_b)

#touch?
line_a.touches(line_b)

#Create a multiline string
multiline = MultiLineString([line_a, line_b])

#Reading KML-files in Geopandas
addresses_fp =r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment3\addresses.shp"
poly_fp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment3\PKS_suuralue.kml"

#read files
data1 = gpd.read_file(addresses_fp)

#to make it read kml fil
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

polys = gpd.read_file(poly_fp, driver ='KML')

#select the sourthern district
southern = polys.ix[polys['Name']=='Eteläinen ']
southern.reset_index(drop=True, inplace=True)

#Figure, axes
fig, ax = plt.subplots()
polys.plot(ax=ax, facecolor='gray')
southern.plot(ax=ax, facecolor='red')
data.plot(ax=ax, color='blue', markersize=5)


#select the point inside the red polygons(southern district polygon)
points_in_polygon_mask = data1.within(southern.loc[0, 'geometry'])

#use mask array to select those points that are true
pip_data = data.loc([points_in_polygon_mask])



fpa = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment3\Vaestotietoruudukko_2015.shp"

#read the data
pop = gpd.read_file(fpa)

#rename the columns
pop= pop.rename(columns={'ASUKKAITA':'pop15'})
pop.columns

#remove some columns
drop_cols=['ASVALJYYS', 'IKA0_9', 'IKA10_19', 'IKA20_29',
       'IKA30_39', 'IKA40_49', 'IKA50_59', 'IKA60_69', 'IKA70_79', 'IKA_YLI80']
      
pop=pop.drop(labels=drop_cols, axis=1)

addresses = gpd.read_file(addresses_fp)

pop.crs

#reproect the addresses to thesame projection as population dataframe.
from fiona.crs import from_epsg
addresses.crs = from_epsg(4326)
addresses=addresses.to_crs(crs=pop.crs)

#check
pop.head()
addresses.head()

#spatial join
join = gpd.sjoin(addresses, pop, how='inner', op='within')

join.plot(column='pop15', cmaps='Reds', markersize=7, scheme ='natural_breaks', legend=True)

import pysal


######################################################3
#Nearest Neighbour Analysis
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points

#create origin point
orig = (1, 1.67)

#create a few destination points 
dest1, dest2, dest3 = Point(0, 1.45), Point(2,2), Point(0,2.5)
dest1
dest2
dest3


#find which is closest to the origin.

#first combine the points one feature as multipooints

#crearte a multpoint object
destinations= MultiPoint([dest1, dest2, dest3])
destinations


#find out the narest eo,etru
nearest_geoms = nearest_points(orig, destinations)

print(nearest_geoms[0])
print(nearest_geoms[1])


def nearest(row, geom_union, df1, df2, geom1_col='geometry', geom2_col='geometry', src_column=None):
    """Find the nearest point and return the corresponding value from specified column."""
    # Find the geometry that is closest
    nearest = df2[geom2_col] == nearest_points(row[geom1_col], geom_union)[1]
    # Get the corresponding value from df2 (matching is based on the geometry)
    value = df2[nearest][src_column].get_values()[0]
    return value
    
    

addresses_fp =r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment3\addresses.shp"
polys = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment3\PKS_suuralue.kml"




#read files
data = gpd.read_file(addresses_fp)

gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
polys = gpd.read_file(polys, driver = 'KML')

#MultiPoint
unary_union =data.unary_union

#calculate centroid
polys['centroid'] = polys.centroid

polys['nearest_id'] = polys.apply(nearest, geom_union=unary_union, df1=polys, df2=data, geom1='centroid'
                    , src_column='id', axis=1)

#Rename polygon geometry
polys = polys.rename(columns={'geometry': 'poly_geom'})

#Table join
polys = polys.merge(data, left_on='nearest_id', right_on='id')

#Create a LineString from the centroids and the address points
polys['line']=None

polys['line'] = polys.apply(lambda row: LineString([row['geometry'], row['centroid']]),axis=1)

lines=polys[['line', 'id']]
lines.columns=['geometry', 'id']

lines = gpd.GeoDataFrame(lines, geometry='geometry', crs=polys.crs)
lines.plot(column='id')