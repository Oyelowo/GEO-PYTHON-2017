# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 09:54:27 2017

@author: oyeda
"""

import pandas as pd

import matplotlib.pyplot as plt

dataframe = pd.read_csv('C:/Users/oyeda/Desktop/AUTOGIS/ass7/Kumpula-June-2016-w-metadata.txt', skiprows= 8)

dataframe.columns

x = dataframe['YEARMODA']
y = dataframe['TEMP']

plt.plot(x,y)


#'r is the colour, o is the circle point, -- is the line connecting the points
plt.plot(x,y, 'ro--')
plt.title('Kumpula Temperature in June 2016')
plt.xlabel('Date')
plt.ylabel('Temperatue [F]')
plt.text(20160604, 68, 'High temp in early june')
plt.axis([20160615, 20160630, 55.0, 70.0])


plt.bar(x,y)
plt.axis([20160615, 20160630, 55.0, 70.0])


