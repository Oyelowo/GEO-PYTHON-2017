# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 15:52:42 2017

@author: oyeda
"""
import pandas as pd
import matplotlib.pyplot as plt
#Problem 1 - Doing time, plotting temperatures (6 points)

#in this first problem we'll work with using the datetime format for Pandas data,
#and creating a line plot of data from a file. You should:

#Load the Helsinki temperature data file produced above (helsinki.csv) into Pandas
#Convert the DATE_m column to the Pandas datetime format.
#Set the DATE_m column as the DataFrame index
#Make a line plot of temperatures in Celsius from 2010-2017.
#The line should be a dashed black line with circles for the data points, and include
#a descriptive title and axis labels.
#Save your Python script file as temperature_plot.py in GitHub and include a copy of the 
#plot it produces in your answer to Problem 1 below. More guidance on this problem can'
#be found in the hints for this week's exercise.

data_h = pd.read_csv('C:/Users/oyeda/Desktop/AUTOGIS/ass7/helsinki.csv', sep=',', parse_dates=['DATE_yrmo'])

data_h['DATE_yrmo'] =  pd.to_datetime(data_h['DATE_yrmo'], format='%Y%m')
data_h = data_h.set_index('DATE_yrmo')


data10_17 = data_h['2010-01':'2017-12']

x=data10_17.index
#y=data10_17['PRCP']
y=data10_17['TAVG_CELS']

#I don't have to aggregate to month anymore since the data had already been agg into months
#monthly = data10_17.resample(rule='M').mean()
#x=monthly.index

plt.plot(x, y, 'ko--')
plt.title('Temperatures in Helsinki 2010-2017')
plt.xlabel('Time')
plt.ylabel('Temperature(°celsius)')
plt.show()

import os
myfolder = r"C:\Users\oyeda\Desktop\AUTOGIS\ass7\other_plots"
filename = "temperature_subplots.png"
filepath = os.path.join(myfolder, filename)
plt.savefig(filepath)
help(plt.plot)



