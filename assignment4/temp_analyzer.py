# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 12:21:34 2017

@author: oyedayo

Description:
    
    This file contains FMI temperature data from Helsinki Malmi Airport for one week that are used 
    in Exercise 4 at Geo-Python 2017 course: https://geo-python.github.io
This script analyses the temperature data which is in fahrenheit. The list was converted to celsius using
the functions developed earlier. it was also grouped into different conditions which were counted.
Data source:
    https://www.ncdc.noaa.gov
Note:
    The data values in temp list are half-hourly values (1 obs / 30 minutes) represented in Fahrenheits. 
   

"""
#import the funtions created earlier
from functions import fahrToCelsius, tempClassifier
# List of half-hourly temperature values (in degrees Fahrenheit) for one week
tempData =  [19, 21, 21, 21, 23, 23, 23, 21, 19, 21, 19, 21, 23, 27, 27, 28, 30, 30, 32, 32, 32, 32, 34, 34,
             34, 36, 36, 36, 36, 36, 36, 34, 34, 34, 34, 34, 34, 32, 30, 30, 30, 28, 28, 27, 27, 27, 23, 23,
             21, 21, 21, 19, 19, 19, 18, 18, 21, 27, 28, 30, 32, 34, 36, 37, 37, 37, 39, 39, 39, 39, 39, 39,
             41, 41, 41, 41, 41, 39, 39, 37, 37, 36, 36, 34, 34, 32, 30, 30, 28, 27, 27, 25, 23, 23, 21, 21,
             19, 19, 19, 18, 18, 18, 21, 25, 27, 28, 34, 34, 41, 37, 37, 39, 39, 39, 39, 41, 41, 39, 39, 39,
             39, 39, 41, 39, 39, 39, 37, 36, 34, 32, 28, 28, 27, 25, 25, 25, 23, 23, 23, 23, 21, 21, 21, 21,
             19, 21, 19, 21, 21, 19, 21, 27, 28, 32, 36, 36, 37, 39, 39, 39, 39, 39, 41, 41, 41, 41, 41, 41,
             41, 41, 41, 39, 37, 36, 36, 34, 32, 30, 28, 28, 27, 27, 25, 25, 23, 23, 23, 21, 21, 21, 19, 19,
             19, 19, 19, 19, 21, 23, 23, 23, 25, 27, 30, 36, 37, 37, 39, 39, 41, 41, 41, 39, 39, 41, 43, 43,
             43, 43, 43, 43, 43, 43, 43, 39, 37, 37, 37, 36, 36, 36, 36, 34, 32, 32, 32, 32, 30, 30, 28, 28,
             28, 27, 27, 27, 27, 25, 27, 27, 27, 28, 28, 28, 30, 32, 32, 32, 34, 34, 36, 36, 36, 37, 37, 37,
             37, 37, 37, 37, 37, 37, 36, 34, 30, 30, 27, 27, 25, 25, 23, 21, 21, 21, 21, 19, 19, 19, 19, 19,
             18, 18, 18, 18, 18, 19, 23, 27, 30, 32, 32, 32, 32, 32, 32, 34, 34, 34, 34, 34, 36, 36, 36, 36,
             36, 32, 32, 32, 32, 32, 32, 32, 32, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 28, 28]


#Iterate over the Fahrenheit temperature values in the tempData list (one by one) and:
#Create a new variable called tempCelsius in which you should assign the temperature in 
#Celsius using the fahrToCelsius function to convert the Fahrenheit temperature into Celsius.
#Create a new variable called tempClass in which you should assign the temperature class number 
#(0, 1, 2, or 3) using the tempClassifier function
#Add the tempClass value to the temp_classes list

#create an empty list for tempCelsius
tempCelsius=[] 

#iterate over the data and convert to celsius, also round off to 2 decimal places.
for t in tempData:
    a=round(fahrToCelsius(t),2) 
    tempCelsius.append(a)
   
print (tempCelsius)
len(tempCelsius)

tempClasses=[]
for tempClass in tempCelsius:
    tempClasses.append(tempClassifier(tempClass))
    
print (tempClasses)

#How many temperatures are there within each temperature class?
#Count the number of zeros, ones, twos, and threes in the tempClasses list and 
#print out the results at the end of your script
#Tip: You might want to consider using a count() function OR a for loop to handle this
#Add comments in your code and a docstring at the beginning of your script that explains 
#what the temp_analyzer script does and how it is used.
#Commit your temp_analyzer.py script to your own GitHub repository for Exercise 4

#count the number of times each condition values occured
tempClasses.count(0)
tempClasses.count(1)
tempClasses.count(2)
tempClasses.count(3)
tempClasses.count(0) + tempClasses.count(1) + tempClasses.count(2) + tempClasses.count(3)

#Alternative. it can also be done by:
count0=[]
for freq in tempClasses:
    if freq == 0: count0.append(freq)
len(count0)

count1=[]
for freq in tempClasses:
    if freq == 1: count1.append(freq)
len(count1)

count2=[]
for freq in tempClasses:
    if freq == 2: count2.append(freq)
len(count2)

count3=[]
for freq in tempClasses:
    if freq == 3: count3.append(freq)
len(count3)

