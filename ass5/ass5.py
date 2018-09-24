# -*- coding: utf-8 -*-
"""
Created on Wed Oct 04 17:20:39 2017

@author: oyeda
"""

import pandas as pn
#In this problem your task is to download and explore the data from 6153237444115dat.csv 
#by reading the data into Pandas and conduct following tasks / answer to following questions:

#Read the data into a variable called data.
#Important: When reading the data, it is important that you tell to Pandas that no-data values 
#are specified with varying number of * characters.
#You can do this by specifying a following parameter in the read_csv() -function:
#na_values=['*', '**', '***', '****', '*****', '******']
myfile=('C:/Users/oyeda/Desktop/AUTOGIS/ass5/6153237444115dat.csv')
data = pn.read_csv(myfile, sep=',' , na_values=['*','**','***', '****', '*****', '******'])


#How many rows is there in the data?
len(data)
#or
len(data.index)

#There are 11, 694 rows


#What are the column names?
print(data.columns)
#Index(['USAF', 'WBAN', 'YR--MODAHRMN', 'DIR', 'SPD', 'GUS', 'CLG', 'SKC', 'L',
 #      'M', 'H', 'VSB', 'MW', 'MW.1', 'MW.2', 'MW.3', 'AW', 'AW.1', 'AW.2',
  #     'AW.3', 'W', 'TEMP', 'DEWP', 'SLP', 'ALT', 'STP', 'MAX', 'MIN', 'PCP01',
   #    'PCP06', 'PCP24', 'PCPXX', 'SD'],
    #  dtype='object')



#What are the datatypes of the columns?
print(data.dtypes)


#What is the mean Fahrenheit temperature in the data? (TEMP column)
mean= data['TEMP'].mean()
#or
#data['TEMP'].sum()/len(data['TEMP'])
print(mean)
#What is the standard deviation of the Maximum temperature? (MAX column)
standard_dev= data['MAX'].std()
print(standard_dev)

#How many unique stations exists in the data? (USAF column)
unique_stations = data['USAF'].unique()
print(list(unique_stations))

#You should write your codes into a data_exploration.py file and print the answers for 
#the questions above inside the script.

#Upload the script to your GitHub repository for Exercise 5
#Remember to comment well your code! (add docstring, and comments explaining what your code does)