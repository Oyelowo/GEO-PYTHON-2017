# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 11:49:38 2017

@author: oyeda
"""

#Create a new variable basename that contains text "Station".
basename = 'Station'


#Create a new variable filenames that is an empty list.
#filenames = []
filenames = list()
filenames
#Iterate over the number range 0-20 and
number = list(range(21))
number


#for number in range(21): 

 station =( basename + "_" + ".txt") * 20
 station
#Create a variable station that contains the 1) text from basename variable, 
#2) the number, and 3) the file extension .txt
for i in range(6): number[i]=number[i]+i
print(number)

lenn = 0
for letter in number:
     lenn = lenn + 1
     station = basename + "_" + ".txt"
station
In [15]: print('There are', length, 'letters')
There are 8 letters

station = basename + "_" + ".txt"
my(numer)

station

#Add the content of station to filenames list which should have following 
#content in the end:
filenames.append(station+number)
filenames
#['Station_0.txt', 'Station_1.txt', 'Station_2.txt', 'Station_3.txt',
 #'Station_4.txt', 'Station_5.txt', 'Station_6.txt', 'Station_7.txt',
 #'Station_8.txt', 'Station_9.txt', 'Station_10.txt', 'Station_11.txt',
 #'Station_12.txt', 'Station_13.txt', 'Station_14.txt', 'Station_15.txt',
 #'Station_16.txt', 'Station_17.txt', 'Station_18.txt', 'Station_19.txt',
 #'Station_20.txt']

