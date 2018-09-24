# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 14:07:43 2017

@author: oyeda
"""

#Exercise 4
#
#This week we will practice how to do data classification and aggregation in Geopandas. 
#We continue from the last week's exerise with rather similar idea. The overall 
#aim this week is to define dominance areas [0] for 8 shopping centers in Helsinki
# with different travel modes (Public tranport, private car). The last step 
#(optional) is to find out how many people live within the dominance areas of 
#those big shopping centers in Helsinki Region.
#
#The exercise might be a rather demanding one, so don't panic, the assistants will 
#help you and we will go through the exercise in the following week.
#
#[0]: Here, we define the dominance area of a service as the geographical area 
#from where the given service (shopping center) is the closest one to reach in 
#terms of travel time.
#
#Exercise 4 is due by the start of lecture on 27.11.
#
#Don't forget to check out the hints for this week's exercise if you're having trouble.
#
#Scores on this exercise are out of 20 points.
#
#Problem 1: Join accessibility datasets into a grid and visualize them by using 
#a classifier (6 points)
#
#Steps:
#
#Download a dataset from here that includes 7 text files containing data about 
#accessibility in Helsinki Region and a Shapefile that contains a Polygon grid 
#that can be used to visualize and analyze the data spatially. The datasets are:
#
#travel_times_to_[XXXXXXX]_[NAME-OF-THE-CENTER].txt including travel times and 
#road network distances to specific shopping center
#MetropAccess_YKR_grid_EurefFIN.shp including the Polygon grid with YKR_ID 
#column that can be used to join the grid with the accessibility data
#Read those travel_time data files (one by one) with Pandas and select only 
#following columns from them:
#
#pt_r_tt
#car_r_t
#from_id
#to_id
#Visualize the classified travel times (Public transport AND Car) of at least 
#one of the shopping centers using the classification methods that we went through 
#in the lesson materials. You need to classify the data into a new column in 
#your GeoDataFrame. For classification, you can either:
#
#Use the common classifiers from pysal
#
#Or create your own custom classifier. If you create your own, remember to 
#document it well how it works! Write a general description of it and comment 
#your code as well.
#
#Upload the map(s) you have visualized into your own Exercise 4 repository 
#(they don't need to be pretty). If visualizing takes for ever (as computer 
#instance can be a bit slow), it is enough that you visualize only one map using
# plotting in Geopandas. If it is really slow, you can do the visualization also 
# using the QuantumGIS in the computer instance or even ArcGIS in the GIS-lab.


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import glob

files =  glob.glob(r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment4\solution\dataE4\*")
#files =  glob.glob("C:/Users/oyeda/Desktop/AUTOGIS/AUTOGIS_PERIOD2/assignment4/solution/dataE4/*")

print(files)
#csv_files = glob.glob('/home/geo/data/small*.csv')

#tt_jum=pd.read_csv(fp + "\TravelTimes_to_5878070_Jumbo.txt", sep=";")
#tt_dix=pd.read_csv(fp + "\TravelTimes_to_5878087_Dixi.txt", sep=";")
#tt_myyr =pd.read_csv(fp +"\TravelTimes_to_5902043_Myyrmanni.txt", sep=";")
#tt_iti= pd.read_csv(fp +"\TravelTimes_to_5944003_Itis.txt", sep=";")
#tt_for= pd.read_csv(fp +"\TravelTimes_to_5975373_Forum.txt", sep=";")
#tt_iso =pd.read_csv(fp + "\TravelTimes_to_5978593_Iso_omena.txt", sep=";")
#tt_ruo = pd.read_csv(fp +"\TravelTimes_to_5980260_Ruoholahti.txt", sep=";")



fp=r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment4\solution\dataE4"
tt_jum=pd.read_csv(fp + "\TravelTimes_to_5878070_Jumbo.txt", sep=";")
tt_dix=pd.read_csv(fp + "\TravelTimes_to_5878087_Dixi.txt", sep=";")
tt_myyr =pd.read_csv(fp +"\TravelTimes_to_5902043_Myyrmanni.txt", sep=";")
tt_iti= pd.read_csv(fp +"\TravelTimes_to_5944003_Itis.txt", sep=";")
tt_for= pd.read_csv(fp +"\TravelTimes_to_5975373_Forum.txt", sep=";")
tt_iso =pd.read_csv(fp + "\TravelTimes_to_5978593_Iso_omena.txt", sep=";")
tt_ruo = pd.read_csv(fp +"\TravelTimes_to_5980260_Ruoholahti.txt", sep=";")


#select the below columns from all the above
tt_jum = tt_jum[["pt_r_tt", "car_r_t", "from_id", "to_id"]] 
tt_dix = tt_dix[["pt_r_tt", "car_r_t", "from_id", "to_id"]] 
tt_myyr = tt_myyr[["pt_r_tt", "car_r_t", "from_id", "to_id"]] 
tt_iti = tt_iti[["pt_r_tt", "car_r_t", "from_id", "to_id"]] 
tt_for = tt_for[["pt_r_tt", "car_r_t", "from_id", "to_id"]] 
tt_iso = tt_iso[["pt_r_tt", "car_r_t", "from_id", "to_id"]] 
tt_ruo = tt_ruo[["pt_r_tt", "car_r_t", "from_id", "to_id"]] 

grid_shp = gpd.read_file(fp + "\MetropAccess_YKR_grid_EurefFIN.shp")
grid_shp.plot()

grid_shp.crs
tt_iti.crs
tt_iti.head(5)

import pysal as ps

# Define the number of classes
n_classes = 5
#The classifier needs to be initialized first with make() function that takes the
#number of desired classes as input parameter.

#Trying put these two classifiers
classifier = ps.Quantiles.make(k=n_classes)
# Create a Natural Breaks classifier
classifier = ps.Natural_Breaks.make(k=n_classes)
#Now we can apply that classifier into our data quite similarly as in our previous examples.

# Classify the data
classifications = tt_iti[['pt_r_tt']].apply(classifier)

# Let's see what we have
classifications.head()

#create a new column to include the classification
tt_iti["quant_pt_r_tt"] = classifications
tt_iti.head(5)
grid_shp.head(2)
tt_iti.head(2)

tt_iti_merg_shp = grid_shp.merge(tt_iti, left_on="YKR_ID", right_on="from_id" )
tt_iti_merg_shp.head(2)

tt_iti_merg_shp.plot(column="quant_pt_r_tt", linewidth= 0 ,legend=True)
plt.tight_layout()

tt_iti["quant_car_r_t"] = classifications
tt_iti_merg_shp.plot(column="quant_car_r_t", linewidth= 0 ,legend=True)
plt.tight_layout()

#==============================================================================
# Problem 2:
# Calculate and visualize the dominance areas of shopping centers (9 points)
# 
# In this problem, the aim is to define the dominance area for each of those shopping 
# centers based on travel time.
# 
# How you could proceed with the given problem is:
# 
# iterate over the accessibility files one by one
# rename the travel time columns so that they can be identified
# you can include e.g. the to_id number as part of the column name 
# (then the column name could be e.g. "pt_r_tt_5987221")
# Join those columns into MetropAccess_YKR_grid_EurefFIN.shp where YKR_ID in the 
# grid corresponds to from_id in the travel time data file. At the end you should 
# have a GeoDataFrame with different columns show the travel times to different 
# shopping centers.
# 
# For each row find out the minimum value of all pt_r_tt_XXXXXX columns and insert 
# that value into a new column called min_time_pt. You can now also parse the to_id 
# value from the column name (i.e. parse the last number-series from the column text) 
# that had the minimum travel time value and insert that value as a number into 
# a column called dominant_service. In this, way are able to determine the "closest" 
# shopping center for each grid cell and visualize it either by travel times or 
# by using the YKR_ID number of the shopping center (i.e. that number series that 
# was used in column name).
#                                                    
# Visualize the travel times of our min_time_pt column using a common classifier 
# from pysal (you can choose which one).
# Visualize also the values in dominant_service column (no need to use any specific 
# classifier). Notice that the value should be a number. If it is still as text, 
# you need to convert it first.
# Upload the map(s) you have visualized into your own Exercise 4 repository 
# (they don't need to be pretty).
#==============================================================================

files =  glob.glob(r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment4\solution\dataE4\*")
txt_files = glob.glob(r"C:\Users\oyeda\Desktop\AUTOGIS\AUTOGIS_PERIOD2\assignment4\solution\dataE4\*.txt")
tt_iti.head(3)
tt_jum.head(3)


gg=gpd.GeoDataFrame()
gg["min_time_pt"]=None

nn=[]
grid_shp = gpd.read_file(fp + "\MetropAccess_YKR_grid_EurefFIN.shp")
for file in txt_files:
    aa= pd.read_csv(file, sep=";", usecols=["pt_r_tt", "from_id", "to_id"])
    
    #I used the max function below because there are nodata rows marked with -1
    #hence, unique() might not work as wanted because there would be -1 and the to_id number of the dataframa"
    destination = str(aa["to_id"].max())
    
    #rename travel time columns tohave unique id
    aa.rename(columns = {"pt_r_tt": ("pt_r_tt_" + destination)}, inplace = True)
    #The above can also be done by following the next two steps below:
#    tt_col_id = dict({"pt_r_tt": ("pt_r_tt_" + destination) })
#    aa.rename(columns = tt_col_id, inplace=True)

    #merge the grid with the  travel time matrices
    grid_shp = grid_shp.merge(aa,  left_on="YKR_ID", right_on="from_id")
    
    for idx, rows in grid_shp.iterrows():
        #select columns
        val= ["pt_r_tt_5878070","pt_r_tt_5878087","pt_r_tt_5902043","pt_r_tt_5944003","pt_r_tt_5975373","pt_r_tt_5978593","pt_r_tt_5980260"]
        #find the minimum travel time of each row
        min_tt=rows[val].min() 
        #place them in a new column
        grid_shp.loc[idx, "min_time_pt"]=min_tt
        #select the column with minimum time by locating the columns with the minimum time and selecting the second
        #because the first is the minimum time. then, slice the names by taking of pt_r_tt and leaving the number which
        #starts at index 8 and is also the to_id
        cb= (grid_shp.columns[(grid_shp==min_tt).iloc[idx]][1])[8:]
        grid_shp.loc[idx, "dominant_service"] = cb

grid_shp.plot(column="min_time_pt", linewidth= 0 ,legend=True)
        
mmm= grid_shp.head(10)
df.columns[(df == 38.15).iloc[0]]
grid_shp['min_time_pt'].where(grid_shp['min_time_pt'] == 121)
grid_shp.columns[8]

(grid_shp.columns[(grid_shp==121).iloc[0]][1])[8:]


      ccc.slice(9,15)  

        #rows.loc[idx, rows["pt_r_tt_5878070","pt_r_tt_5878087","pt_r_tt_5902043","pt_r_tt_5944003","pt_r_tt_5975373","pt_r_tt_5978593","pt_r_tt_5980260"]]
      