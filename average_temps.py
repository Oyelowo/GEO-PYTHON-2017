# -*- coding: utf-8 -*-
"""
Prints information about monthly average temperatures recorded at the Helsinki
Malmi airport.
Created on Thu Sep 14 21:37:28 2017

@author: oyedayo oyelowo
"""



#Create a script called average_temps.py that allows users to select a 
#month and have the monthly average temperature printed to the screen. 
#For example, if the user sets month to "March", the script will display
#The average temperature in Helsinki in March is -1.0"""


#create list for the 12 months of the year
month = ['January', 'February', 'March', 'April', 'May', 'June', 'July',\
             'August', 'September', 'October' ,'November', 'December']

#create list for average temperature of each month
temp = [-3.5, -4.5, -1.0, 4.0, 10.0, 15.0, 18.0, 16.0, 11.5, 6.0, 2.0, -1.5]

#set the selected month
selectedMonth = 'August'

#find the location of the selected month
indexMonth = month.index(selectedMonth)

#get the average temperature of the selected month
monthTemp = temp[indexMonth]

#print the month and the average temperature of that month
print 'The average temperature in Helsinki in', selectedMonth , 'is', monthTemp 