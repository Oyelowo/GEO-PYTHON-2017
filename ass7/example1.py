# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 11:09:15 2017

@author: oyeda
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 10:45:28 2017

@author: oyeda
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as mp

fp = 'C:/Users/oyeda/Desktop/AUTOGIS/ass7/1924927457196dat.txt'

#read the data with time inoformationa nd parse that
data = pd.read_csv(fp, sep = '\s+', parse_dates=['YR--MODAHRMN'], na_values=['*','**','***', '****', '*****', '******'])

data.dtypes


data =data[['YR--MODAHRMN', 'TEMP', 'SPD']]
data

# Rename columns
name_conversion = {'YR--MODAHRMN': 'TIME', 'SPD': 'SPEED'}
data = data.rename(columns=name_conversion)

data.columns

# Convert Fahrenheit temperature into Celsius
data['Celsius'] = (data['TEMP'] - 32) / 1.8

data.head()

data.plot(x='TIME', y='Celsius');


#Selecting data based on time in Pandas
#What is obvious from the figure above, is that the hourly level data is actually slightly too accurate for plotting data covering two full years. Let’s see a trick, how we can really easily aggregate the data using Pandas.

#First we need to set the TIME as the index of our DataFrame. We can do this by using set_index() parameter.

#change the index
data = data.set_index('TIME')

data.head()

data.index

#select data 
first_jan = data['2013-01-01': '2013-01-01']

first_jan_12h = data['2013-01-01 00:00': '2013-01-01 12:00']

#aggregate data from hourly obsaervations into daily observations
daily = data.resample(rule='D').mean()
daily.head()


#Let’s now plot our daily temperatures in a similar manner as earlier. Note, 
#that now our time is the index of our DataFrame, so we can pass that into our 
#plotting function. Let’s also change the width and the color of our line to red).
#The kind parameter can be used to specify what kind of plot you want to visualize.
#There many different ones available in Pandas, however, we will now only use
#basic line plots in this tutorial. See many different kind of plots from official 
#Pandas documentation about visualization.

#plot temperatures
daily.plot(x=daily.index, y='Celsius', kind='line', lw=0.75, 'ro--', c='r');
 
#you can use the below, if you try it in console with the dot at the end, and tab key, it brings out
#many options for you to do many things
#data.index

#save the figure with 300 resolution
plt.savefig("C:/Users/oyeda/Desktop/AUTOGIS/ass7/temp_plot1.png", dpi=300)

#select data for different seasons
winter = daily['2012-12-01': '2013-02-28']
spring = daily['2013-03-01': '2013-05-31']
summer = daily['2013-06-01': '2013-08-31']
fall = daily['2013-09-01': '2013-11-30']

#create a panel 2 X 2 with  subplots
flg, axes = plt.subplots(nrows= 2, ncols = 2, figsize=(12, 8))

#parse the axes from the axarray
ax11 =  axes[0][0]
ax12 =  axes[0][1]
ax21 =  axes[1][0]
ax22 =  axes[1][1]

#create the subplots
winter.plot(x= winter.index, y = 'Celsius',ylim=(-25, 25), ax=ax11, lw=2, c='blue')
spring.plot(x= spring.index, y = 'Celsius',ylim=(-25, 25),  ax=ax12, lw=2, c='orange')
summer.plot(x= summer.index, y = 'Celsius',ylim=(-25, 25),  ax=ax21, lw=2, c='purple')
fall.plot(x= fall.index, y = 'Celsius',ylim=(-25, 25),  ax=ax22, lw=2, c='red')
