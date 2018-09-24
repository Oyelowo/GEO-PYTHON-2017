# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 14:04:27 2017

@author: oyeda
"""

import geopandas as gpd


#read the data
fp = r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment2\euro_borders\Europe_borders.shp"

data = gpd.read_file(fp)


#create a copy of the geodataframe
data_proj =  data.copy()

#REproject
data_proj =data_proj.to_crs(epsg=3035)

#another way. sometimes, the above might nt be posible. eg when dealing with ESRI projectionm
proj_txt ="+proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000 +ellps=GRS80 +units=m +no_defs"
data2_proj2 = data.to_crs(proj_txt)

#now they ave different projections. check below:
data.head()
data_proj.head()

data.plot()

#the shape looks better now
data_proj.plot()

#if you have to calculate distance to this point, ypou can do this. here ou have to inout the specific
#position of the placeyou are dealing with e.g Helsinki below. 0,0 location are from helsinki and they vary from
#there
hki_lon = 24.9417

hki_lat = 60.1666

proj4_txt_LAEA_hki = proj4_txt = '+proj=eqc +lat_ts=60 +lat_0={0} +lon_0={1} +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs'.format(hki_lon, hki_lat)

data_wec= data.to_crs(proj4_txt_LAEA_hki)


#calculate the centroids of the countries i europe
data_wec['country_centroid'] = data_wec.centroid

#now, calculate the distances to helsinki

from shapely.geometry import Point

#Create a point for Helsinki
hki_point = Point(hki_lon, hki_lat)
print(hki_point)


def calculateDistance(row, dest_geom, src_col='geometry', target_col='distance'):
    """
    Calculates the distance between a single Shapely Point geometry and a GeoDataFrame with Point geometries.

    Parameters
    ----------
    dest_geom : shapely.Point
        A single Shapely Point geometry to which the distances will be calculated to.
    src_col : str
        A name of the column that has the Shapely Point objects from where the distances will be calculated from.
    target_col : str
        A name of the target column where the result will be stored.
    """
    # Calculate the distances
    dist = row[src_col].distance(dest_geom)
    # Tranform into kilometers
    dist_km = dist/1000
    # Assign the distance to the original data
    row[target_col] = dist_km
    return row
    
    
from fiona.crs import from_epsg
#create a geoseries of the helsinki point
hki_series = gpd.GeoSeries([hki_point], crs=from_epsg(4326))
hki_series=hki_series.to_crs(proj4_txt_LAEA_hki)


hki_Series

hki_geo= hki_series.get(0)


#apply function to geodataframe
data_wec= data_wec.apply(calculateDistance, dest_geom=hki_geo, src_col='country_centroid', target_Col = 'dist_to_hki', axis=1)


#another way
data_wec.distance(hki_geo)