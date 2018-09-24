# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 15:37:55 2017

@author: oyeda
"""
#The numerical values for rainfall and temperature read in as numbers
#The second row of the datafile should be skipped, but the text labels for the columns should be from the first row
#The no-data values should properly be converted to NaN
import pandas as pd
data= pd.read_csv('C:/Users/oyeda/Desktop/AUTOGIS/ass6/1091402.txt' , 
                  sep= '\s+', skiprows=[1], na_values='-9999')
data.head(2)
data.tail()
#How many non-NaN values are there for TAVG?
data['TAVG'].isnull().sum() 

#What about for TMIN?
data['TMIN'].isnull().sum() 

#How many days total are covered by this data file?
len(data['DATE'].index)

#When is the first observation?
data['DATE'].iloc[0]

#When is the last?
data['DATE'].iloc[(len(data['DATE']))-1]


def ftc(fahrenheit):
    '''This function converts temperature from fahrenheit to celsius
    fahrnheit:  the temperature in fahrenheit to be converted'''
    result = (fahrenheit - 32)/1.8
    return result
    





#What was the average temperature of the whole data file (all years)?
def fahrToCels(row, source_col, target_col):
    '''funtion to convert tempperature in fahrenheit to celsius in a column
    source_col: the colum with the temperature in fahrenheit
    target col: created column with converted temperature in celsius
    '''
    row[target_col]="%.2f"%((row[source_col] - 32) /1.8)
    return row
help(fahrToCels)


#create a copy of the data
dataCopy= data.copy()

#drop the nodata in column TAVG
data1=dataCopy.dropna(subset=['TAVG'])

#reset the index and drop the original
data1= data1.reset_index(drop=True)

#apply the function created ealier to create a new colum which converts
#the fahrenheit temperature to celsius
data1= data1.apply(fahrToCels, source_col = 'TAVG', target_col='TAVG_CELS', axis=1)
data1.head(7)


#convert to float, to be able to calculate the mean temperature
data1['TAVG_CELS']=data1['TAVG_CELS'].astype(float)

#calculate mean temperature in celsius for the entire data, to 2 decimal places
meanTempCels= '%.2f'%(data1['TAVG_CELS'].mean())
print('The mean temperature in celsius is: ', meanTempCels)

meanTempFahr= '%.2f'%(data1['TAVG'].mean())
print('The mean temperature in fahrenheit is: ', meanTempFahr)

#What was the TMAX temperature of the Summer 69 (i.e. including months 
#May, June, July, August of the year 1969)?

summer69= (dataCopy.ix[(dataCopy['DATE']>=19690501) & 
                (dataCopy['DATE']<19690901)]).reset_index(drop=True)
TMaxSummer69F=summer69['TMAX'].max()

#also possible to do the above directly, as in
#TMaxSummer69F=(dataCopy.ix[(dataCopy['DATE']>=19690501) & 
#    (dataCopy['DATE']<19690901)]).reset_index(drop=True)['TMAX'].max()

#convert to celsius and round off to 2dp
TMaxSummer69C= '%.2f'%(ftc(TMaxSummer69F))

print('The maximum temperature in summer in 1969 was: ' , TMaxSummer69F, 
'degree fahrenheit')

print('The maximum temperature in summer in 1969 was: ' , TMaxSummer69C, 
'degree celsius')


                          