# -*- coding: utf-8 -*-
"""
Created on Wed Oct 04 17:20:39 2017

@author: oyeda
"""

import pandas as pn
import os
#In this problem your task is to download and explore the data from 6153237444115dat.csv 
#by reading the data into Pandas and conduct following tasks / answer to following questions:

#Read the data into a variable called data.
#Important: When reading the data, it is important that you tell to Pandas that no-data values 
#are specified with varying number of * characters.
#You can do this by specifying a following parameter in the read_csv() -function:
#na_values=['*', '**', '***', '****', '*****', '******']
my_path = os.path.abspath(os.path.dirname(__file__))
myfile = os.path.join(my_path, './6153237444115dat.csv')
# myfile=('C:/Users/oyeda/Desktop/AUTOGIS/ass5/6153237444115dat.csv')
data = pn.read_csv(myfile, sep=',' , na_values=['*','**','***', '****', '*****', '******'])


#How many rows is there in the data?
print('There are',len(data), 'row in the data')
#or
len(data.index)
print('There are ' ,len(data.index), ' row in the data')
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

#calcuate mean fahrenheit temperature rounded to 3 dp
mean="%.3f"%(data['TEMP'].mean())

#or use this alternative method
mean2="%.3f"%(data['TEMP'].sum()/len(data['TEMP']))
print('mean =', mean)
print('mean =',mean2)

#What is the standard deviation of the Maximum temperature? (MAX column)
#calculate the standard deviation to 2 dp
standard_dev= "%.2f"%(data['MAX'].std())
print('standard deviation = ', standard_dev)

#How many unique stations exists in the data? (USAF column)
#unique stations in the data
unique_stations = data['USAF'].unique()
print('The unique stations are', list(unique_stations))
print('There are', len(unique_stations), 'unique stations in the data')

#You should write your codes into a data_exploration.py file and print the answers for 
#the questions above inside the script.

#Upload the script to your GitHub repository for Exercise 5
#Remember to comment well your code! (add docstring, and comments explaining what your code does)



#Problem 2 - Data manipulation (5 points)

#Similarly as in earlier exercises the temperatures in our data are represented
# in Fahrenheit, hence, you need to convert the temperatures into Celsius.

#create function to convert fahrenheit to celsius, just for fun
def fahrtoCels(t):
    '''This function converts fahrenheit to celsius
    t: is the temperature in fahrenheit'''
    a = (t - 32)/1.8
    return a
#check what fahrtoCels function does
help(fahrtoCels)

#Select from the data columns USAF, YR--MODAHRMN, TEMP, MAX, MIN and assign them
# into a new variable called selected
selected=data[['USAF', 'YR--MODAHRMN', 'TEMP', 'MAX', 'MIN']]

#Remove all rows from selected that has NoData in column TEMP using dropna() -function
#remove all the rows with no data in column 'TEMP'
selected_clean =selected.dropna(subset=['TEMP'])

#reset the index and drop the original
selected_clean=selected_clean.reset_index(drop=True)
#print the data with the removed nodata values in columnn 'TEMP'

print(selected_clean)

#Convert the Fahrenheit temperatures from TEMP into a new column Celsius using 
#the conversion formula:

#convert the temperature from fahrenheit to selsius and do this
#by updating the column and not create a new one
selected_clean['TEMP_CELS']= fahrtoCels(selected_clean['TEMP'])
print(selected_clean)   
 
#Round the values in Celsius to have 0 decimals (don't create a new column --> 
#update the current one)
selected_clean['TEMP_CELS']=selected_clean['TEMP_CELS'].round(0)
print(selected_clean)

#Convert the Celsius values into integers (don't create a new column --> 
#update the current one)
selected_clean['TEMP_CELS']=selected_clean['TEMP_CELS'].astype(int)
print(selected_clean)
#You can add your codes into a data_exploration.py file.

#Upload the script to your GitHub repository for Exercise-5
#Remember to comment well your code! (add docstring, and comments explaining 
#what your code does)


#Problem 3 - Data selection (5 points)

#In this problem you should divide the data into separate subsets for different stations 
#and save those DataFrames into disk.

#Divide the selection into two separate datasets:
#Select all rows from selected DataFrame into variable called kumpula where the 
#USAF code is 29980
kumpula = selected_clean.ix[selected_clean['USAF'] == 29980]

#Select all rows from selected DataFrame into variable called rovaniemi where the
#USAF code is 28450
rovianemi = selected_clean.ix[selected_clean['USAF'] == 28450]

#Save kumpula DataFrame into Kumpula_temps_May_Aug_2017.csv file (CSV format)
#separate the columns with ,
#use only 2 decimals in the floating point numbers
output1 = os.path.join(my_path, './Kumpula_temps_May_Aug_2017.csv')
# output1 ='C:/Users/oyeda/Desktop/AUTOGIS/ass5/Kumpula_temps_May_Aug_2017.csv'
kumpula.to_csv(output1, sep=',', index=False, float_format="%.2f")


#Save rovaniemi DataFrame into Rovaniemi_temps_May_Aug_2017.csv file (CSV format)
#separate the columns with ,
#use only 2 decimals in the floating point numbers
output2 = os.path.join(my_path, './Rovaniemi_temps_May_Aug_2017.csv')
# output2 ='C:/Users/oyeda/Desktop/AUTOGIS/ass5/Rovaniemi_temps_May_Aug_2017.csv'
kumpula.to_csv(output2, sep=',', index=False, float_format="%.2f")

#Upload your csv files into your GitHub repository for Exercise 5
#You can add your codes into a data_exploration.py file.

#Upload the script to your GitHub repository for Exercise-5
#Remember to comment well your code! (add docstring, and comments explaining what
# your code does)




#Problem 4 - Data analysis (5 points)

#In this problem the aim is to understand how different the summer temperatures 
#has been in Helsinki Kumpula and Rovaniemi. Using the data from Problem 3 in 
#kumpula and rovaniemi DataFrames answer to following questions:

#Part 1

#What was the median temperature in:
#Helsinki Kumpula?
print('the median temperature in kumpula was', (kumpula['TEMP'].median()))

#Rovaniemi?
print('the median temperature in Rovianemi was', rovianemi['TEMP'].median())

#Part 2

#Part 1 considers data from quite long period of time (May-Aug), 
#hence the differences might not be so clear. Let's find out what were 
#the mean temperatures in May and June in Kumpula and Rovaniemi:

#for fun, check the first 68 rows in kumpula data
kumpula[:68]

#Select from rovaniemi and kumpula DataFrames such rows from the DataFrames where 
#YR--MODAHRMN values are from May 2017 (see hints for help) and assign them 
#into variables rovaniemi_may and kumpula_may
kumpula_may = (kumpula.ix[(kumpula['YR--MODAHRMN'] >= 201705010000) & 
              (kumpula['YR--MODAHRMN'] < 201706010000)]).reset_index(drop=True)

print(kumpula_may)

rovianemi_may = (rovianemi.ix[(rovianemi['YR--MODAHRMN'] >= 201705010000) & 
              (rovianemi['YR--MODAHRMN'] < 201706010000)]).reset_index(drop=True)

print(rovianemi_may)
#Do similar procedure for June and assign those values into variables rovaniemi_june 
#and kumpula_june
#Using those new subsets print the mean, min and max temperatures for both places in May and June.
kumpula_june = (kumpula.ix[(kumpula['YR--MODAHRMN'] >= 201706010000) & 
              (kumpula['YR--MODAHRMN'] < 201707010000)]).reset_index(drop=True)

print(kumpula_june)

rovianemi_june = (rovianemi.ix[(rovianemi['YR--MODAHRMN'] >= 201706010000) & 
              (rovianemi['YR--MODAHRMN'] < 201707010000)]).reset_index(drop=True)

print(rovianemi_june)


print('mean temperature in kumpula in May was',"%.1f" % kumpula_may['TEMP_CELS'].mean())
print('mean temperature in Rovianemi in May was', "%.1f" % rovianemi_may['TEMP_CELS'].mean())

print('minimum temperature in kumpula in May was',kumpula_may['TEMP_CELS'].min())
print('minimum temperature in  Rovianemi in May was', rovianemi_may['TEMP_CELS'].min())

print('maximum temperature in kumpula in May was',kumpula_may['TEMP_CELS'].max())
print('maximum temperature in Rovianemi in May was', rovianemi_may['TEMP_CELS'].max())


print('mean temperature in kumpula in June was', "%.1f" % kumpula_june['TEMP_CELS'].mean())
print('mean temperature in Rovianemi in June was', "%.1f" % rovianemi_june['TEMP_CELS'].mean())

print('minimum temperature in kumpula in June was', kumpula_june['TEMP_CELS'].min())
print('minimum temperature in Rovianemi in June was',rovianemi_june['TEMP_CELS'].min())


print('maximum temperature in kumpula in June was',kumpula_june['TEMP_CELS'].max())
print('maximum temperature in Rovianemi in june was', rovianemi_june['TEMP_CELS'].max())

#You can add your codes into a data_exploration.py file.



#Interpreting the results after the data analysis is one of the most important
# steps in a process called knowledge discovery. Hence, use the information above 
#to discuss shortly about following questions (justify your answers with the data 
#analysis results):

#Does there seem to be large difference in temperatures between the months?
#The differences in temperatures between the two months were quite high
#For instance, the mean temperature in kumpula was about 4 degrees more in June that in 
#May. The difference was even higher in Rovianemi with about 8 degrees higher mean temperature in 
#June that in May. Also the minimum and the maximum temperatures were higher in June
#which appears to be the summer and is overall, expected to be warmer than May

#Is Rovaniemi much colder place than Kumpula?
#Write your answers below here:
#Generally, Rovianemi is much colder as it can be seen in the analysis. It was cooler 
#in both months in Rovianemi and even had minimum temperatures below in June. Although, 
#Kumpula also had a minimum temperature of -2degrees  in May, Rovianemi was even quite colder
#with minimum temperature of -7 degrees. Also the maximum temperatures were lower in :
#Rovianemi in both months
    




