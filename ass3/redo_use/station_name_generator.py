# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 01:28:50 2017

@author: oyeda
"""

#Create a new variable basename that contains text "Station".
basename = "Station"

#Create a new variable filenames that is an empty list.
filenames=[]

#Iterate over the number range 0-20 and
for number in range(21):
    print number

#Create a variable station that contains the 1) text from basename variable, 
#2) the number, and 3) the file extension .txt
station = []
for x in range(21):
    station.append(basename +"_" + str(x) + ".txt")

#Add the content of station to filenames list which should have following content in the end:
filenames=station
print (filenames)
