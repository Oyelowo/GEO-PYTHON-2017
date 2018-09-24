# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 13:27:55 2017

@author: oyeda
"""

# -*- coding: utf-8 -*-
"""
Prints the names of FMI weather stations separated into four geographical zones in Finland (NW, NE, SW, SE) based on
the coordinates of the stations. Additionally, prints the information about the how equally distributed the station
network is in Finland. 

Description:
    This script is only a test for a planned version that would read in all operative station data 
    from a file and allow users to analyze also analyze weather observations from those stations. 

Note:
    The data only includes stations that were operative 70 years ago (started before 1948).   

Limitations:
    The script will produce and error before step 3 has been solved. 

Usage:
    ./allocate_locations.py

Author:
    Henrikki Tenkanen - 19.9.2017

Modified by:
    None
"""

# Data for the exercise
# =====================

# Station names
stations = ['Hanko Russarö', 'Heinola Asemantaus', 'Helsinki Kaisaniemi', 
            'Helsinki Malmi airfield', 'Hyvinkää Hyvinkäänkylä', 'Joutsa Savenaho', 
            'Juuka Niemelä', 'Jyväskylä airport', 'Kaarina Yltöinen', 'Kauhava airfield', 
            'Kemi Kemi-Tornio airport', 'Kotka Rankki', 'Kouvola Anjala', 
            'Kouvola Utti airport', 'Kuopio Maaninka', 'Kuusamo airport', 
            'Lieksa Lampela', 'Mustasaari Valassaaret', 'Parainen Utö', 'Pori airport', 
            'Rovaniemi Apukka', 'Salo Kärkkä', 'Savonlinna Punkaharju Laukansaari', 
            'Seinäjoki Pelmaa', 'Siikajoki Ruukki', 'Siilinjärvi Kuopio airport', 
            'Tohmajärvi Kemie', 'Utsjoki Nuorgam', 'Vaala Pelso', 'Vaasa airport', 
            'Vesanto Sonkari', 'Vieremä Kaarakkala', 'Vihti Maasoja', 'Ylitornio Meltosjärvi']

# Latitude coordinates of Weather stations  
lat = [59.77, 61.2, 60.18, 60.25, 60.6, 61.88, 63.23, 62.4,
       60.39, 63.12, 65.78, 60.38, 60.7, 60.9, 63.14, 65.99,
       63.32, 63.44, 59.78, 61.47, 66.58, 60.37, 61.8, 62.94,
       64.68, 63.01, 62.24, 70.08, 64.5, 63.06, 62.92, 63.84,
       60.42, 66.53]

# Longitude coordinates of Weather stations 
lon = [22.95, 26.05, 24.94, 25.05, 24.8, 26.09, 29.23, 25.67, 
       22.55, 23.04, 24.58, 26.96, 26.81, 26.95, 27.31, 29.23, 
       30.05, 21.07, 21.37, 21.79, 26.01, 23.11, 29.32, 22.49, 
       25.09, 27.8, 30.35, 27.9, 26.42, 21.75, 26.42, 27.22, 
       24.4, 24.65]

# Cutoff values that correspond to the centroid of Finnish mainland
# North - South
NScutoff = 64.5
# East-West
EWcutoff = 26.3

# Step 1. Create lists for geographical zones (North-West, North-East, South-West, South-East)
# ---------------------------------------------------------------------------------------------
# Add your code here
ne = []
nw = []
sw = []
se = []

# Step 2. Make a loop that iterates N number of times. 
# N should be based on the number of stations that we have here. 
# --------------------------------------------------------------
# Add your code here
n = len(stations)
for i in range(n): print(i)
# Step 2.1 - Find out the latitude, longitude and the name of the station

    # Add your code here
station_pos = stations.index('Kouvola Anjala')

long_st = lon[station_pos]
long_st

lat_st = lat[station_pos]
lat_st

    # Steps 2.2-2.3 - Make conditional statements to add the station to correct zone -list
    # You should determine if 
    # a) the lat coordinate is North or South of the center latitude (stored in NScutoff variable)
    # AND 
    # b) if the lon coordinate is East or West of the center longitude (stored in EWcutoff variable)
    # c) Based on the criteria you should add the NAME of the station (from stations -list) to correct list (done in step 1)
    


for x in lat:
    if x> NScutoff:
        if lon[lat.index(x)] > EWcutoff: 
            ne.append(stations[lat.index(x)])
        else: 
            nw.append(stations[lat.index(x)])
    else:
        if lon[lat.index(x)] > EWcutoff: 
            se.append(stations[lat.index(x)])
        else: 
            sw.append(stations[lat.index(x)])
        

        




ne
 nw
se    
sw
len(stations)
len(ne)
len(nw)
len(se)
len(sw)
# Step 3 - Print the station names at each geographical zone
# ----------------------------------------------------------

# Replace the XXX with your list names
print("The names of the North-West stations are:\n", nw)
print("The names of the North-East stations are:\n", ne)
print("The names of the South-West stations are:\n", sw)
print("The names of the South-East stations are:\n", se)

# Step 4 (optional) - Print the share of stations at each geographical zone (in percentages)
# ------------------------------------------------------------------------------------------

# Step 4.1 - Calculate the share for different zones
# Fix the code (replace 0.0 with the result of the calculation)

#the below is used to convert integer to float. I could use float() too
from __future__ import division
nw_share = len(nw)/len(stations) * 100
ne_share = len(ne)/len(stations) * 100
sw_share = len(sw)/len(stations) * 100
se_share = len(sw)/len(stations) * 100

# Print the information (you don't need to modify this)
print("North-West contains", nw_share, "% of all stations.")
print("North-East contains", ne_share, "% of all stations.")
print("South-West contains", sw_share, "% of all stations.")
print("South-East contains", se_share, "% of all stations.")        



