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
