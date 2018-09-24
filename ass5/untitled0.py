# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 05:19:12 2017

@author: oyeda
"""
import pandas as pn
import os
#Problem 5 (optional) - Parse daily temperatures

#This optional task is for more advanced students (minimal guidance given). 
#Our current dataset contains hourly temperatures (actually 3 measurements per hour).

#Your task here is to:

#create a new DataFrame where you have calculated mean, max and min temperatures 
#for each day separately using the hourly values from Rovaniemi and Helsinki Kumpula.
#this problem is a classical data aggregation problem
#Find help from Pandas Official documentation and using Google to find information 
#about solving this issue. If you think you can handle this but don't know how to 
#proceed, ask in Slack for tips.

my_path = os.path.abspath(os.path.dirname(__file__))
input1 = os.path.join(my_path, './Kumpula_temps_May_Aug_2017.csv')
input2 = os.path.join(my_path, './Rovaniemi_temps_May_Aug_2017.csv')

# input1 = 'C:/Users/oyeda/Desktop/AUTOGIS/ass5/Kumpula_temps_May_Aug_2017.csv'
# input2 = 'C:/Users/oyeda/Desktop/AUTOGIS/ass5/Rovaniemi_temps_May_Aug_2017.csv'


data1 = pn.read_csv(input1, sep=',', )
print(data1)
data2 = pn.read_csv(input2, sep=',', )

temps = data1['TEMP_CELS']
print(temps)
# for day in range(1, 32):
#     mask = data1['Day']==day
#     max_temp = temps[mask].max()
#     date = data1[mask]['Date/Time'][temps[mask].argmax()][:11]
#     hour = data1[mask]['Time'][temps[mask].argmax()]    
#     print ('max temperature on',date, 'was', max_temp, 'at', hour)
#Write your codes into a data_aggregation.py file.

#Upload the script to your GitHub repository for Exercise-5
#Remember to comment well your code! (add docstring, and comments 
#explaining what your code does)