# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 15:37:55 2017

@author: oyeda
"""
#The numerical values for rainfall and temperature read in as numbers
#The second row of the datafile should be skipped, but the text labels for the columns should be from the first row
#The no-data values should properly be converted to NaN
import pandas as pd
import os

my_path = os.path.abspath(os.path.dirname(__file__))
myfile = os.path.join(my_path, './1091402.txt')

data= pd.read_csv(myfile, sep= '\s+', skiprows=[1], na_values='-9999')
data.head(2)
data.tail()
#How many non-NaN values are there for TAVG?
print(data['TAVG'].isnull().sum() )

#What about for TMIN?
print(data['TMIN'].isnull().sum() )

#How many days total are covered by this data file?
print(len(data['DATE'].index))

#When is the first observation?
print(data.loc[0, 'DATE'])
#or use this altermative way
print(data['DATE'].iloc[0])

#When is the last?
print(data['DATE'].iloc[(len(data['DATE']))-1])
#or use this alternative way
print(data.loc[(len(data['DATE']))-1, 'DATE'])


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
data1= data.copy()

#drop the nodata in column TAVG
#data1=data1.dropna(subset=['TAVG'])

#reset the index and drop the original
data1= data1.reset_index(drop=True)

#apply the function created ealier to create a new column which converts
#the fahrenheit temperature to celsius
data1= data1.apply(fahrToCels, source_col = 'TAVG', target_col='TAVG_CELS', axis=1)
data1.head(7)



#convert to float, to be able to calculate the mean temperature
data1['TAVG_CELS']=data1['TAVG_CELS'].astype(float)

#What was the average temperature of the whole data file (all years)?

#calculate mean temperature in celsius for the entire data, to 2 decimal places
meanTempCels= '%.2f'%(data1['TAVG_CELS'].mean())
print('The mean temperature in celsius is',meanTempCels)

meanTempFahr= '%.2f'%(data1['TAVG'].mean())
print('The mean temperature in fahrenheit is', meanTempFahr)

#What was the TMAX temperature of the Summer 69 (i.e. including months 
#May, June, July, August of the year 1969)?

summer69= (data1.ix[(data1['DATE']>=19690501) & 
                (data1['DATE']<19690901)]).reset_index(drop=True)
TMaxSummer69F=summer69['TMAX'].max()

#also possible to do the above directly, as in
#TMaxSummer69F=(dataCopy.ix[(dataCopy['DATE']>=19690501) & 
#    (dataCopy['DATE']<19690901)]).reset_index(drop=True)['TMAX'].max()

#convert to celsius and round off to 2dp
TMaxSummer69C= '%.2f'%(ftc(TMaxSummer69F))

print('The maximum temperature in summer in 1969 was' , TMaxSummer69F, 
'degree fahrenheit')

print('The maximum temperature in summer in 1969 was' , TMaxSummer69C, 
'degree celsius')



#For this problem our goal is to calculate monthly average temperature values in
#degrees Celsius from the daily values we have in the data file. You can use the
#approaches taught during the Lesson 6 to solve this . You can again consult the 
#hints for Exercise 6 if you are stuck.

#For this problem modify your temperature_anomalies.py script to

#1.Calculate the monthly average temperatures for the entire data file using the 
#approaches taught during the lecture
#2.Save the output to a new Pandas Series called dataMonths


data1['DATE_str'] = (data1['DATE'].astype(str))
data1['DATE_yrmo'] = data1['DATE_str'].str.slice(start=0, stop=6)


data1['Month'] = data1['DATE_str'].str.slice(start=4,stop=6)
data1['Month'] = data1['Month'].astype(int)


grouped= data1.groupby('DATE_yrmo')
type(grouped)
len(grouped)
#group1= grouped.get_group(195201)
#group1['TAVG'].mean()

mean_cols= ['STATION', 'ELEVATION', 'LATITUDE', 'LONGITUDE', 'DATE', 'PRCP', 'TAVG',
       'TMAX', 'TMIN', 'DATE_str', 'DATE_yrmo', 'Month']
dataMonths = pd.DataFrame()

for key, group in grouped:
    
    # Aggregate the data
    mean_val= group[mean_cols].mean()
    
    # Add the ´key´ (i.e. the date+time information) into the aggregated values
    mean_val['DATE_yrmo'] = key

    # Append the aggregated values into the DataFrame
    dataMonths=dataMonths.append(mean_val, ignore_index=True)
   
dataMonths.head()
    
    
    
    

#Create a second Series called dataMonthsC that has the monthly temperatures in Celsius.
#dataMonths['TAVG_CELS'] = ftc(dataMonths.['TAVG'])
dataMonthsC = dataMonths.apply(fahrToCels, source_col='TAVG', target_col='TAVG_CELS', axis=1)
help(fahrToCels)
dataMonthsC.head()

#Merge the two data Series into a single Pandas DataFrame called monthlyData 
#using the pd.concat() function (see the documentation of Pandas or hints if needed).

#NOTE!!!!!!!!!!!!!!!! There is no need for me to merge the above 
monthlyData = dataMonthsC.copy()




#Upload the updated script to your repository for this week's exercise.




#Problem 3 - Calculating temperature anomalies (5 points)

#Our goal in this problem is to calculate monthly temperature anomalies in order
# to see how temperatures have changed over time, relative to the observation 
#period between 1952-1980. We will again do this by modifying your 
#temperature_anomalies.py script. In order to complete the problem, you must do 
#two things:

#You need to calculate a mean temperature for each month for the period 1952-1980 
#using the data in the data file. Note that the monthly mean here is slightly 
#different than the monthly mean temperatures calculated earlier. 
#Here, we are looking to find the mean temperature for January in the period 1952-1980,
# February for the same period, etc. You should end up with 12 values, 
#1 mean temperature for each month in that period, and store them in a Pandas 
#Series called referenceTemps. Remember, these temperatures should be in degrees 
#Celsius.

#Once you have the monthly mean values for each of the 12 months, you can then 
#calculate a temperature anomaly for every month in the monthlyData DataFrame. 
#The temperature anomaly we want to calculate is simply the temperature for one month
# in monthlyData minus the corresponding monthly average temperature from the
# referenceTemps data Series. You should thus end up with a new column in the 
#monthlyData DataFrame showing the temperature anomaly, the difference in temperature
# for a given month (e.g., February 1960) compared to the average (e.g., for February
# 1952-1980).

#Upload the updated script to your repository for this week's exercise.
#converts the dataMonths from string into integer to be able to order it
monthlyData['DATE_yrmo'] = monthlyData['DATE_yrmo'].astype(int)
monthlyData['Month'] = monthlyData['Month'].astype(int)


data28yrs = (monthlyData.ix[(monthlyData['DATE_yrmo'] >= 195201) & 
                      (monthlyData['DATE_yrmo'] <= 198012)]).reset_index(drop=True)

data52_80 = data28yrs.copy()
data52_80.dtypes



grouped_Month= data52_80.groupby('Month')

type(grouped_Month)
len(grouped_Month)
#group1= grouped_Month.get_group(1)
#group1['TAVG'].mean()

#convert the celsius temperature from object to float to allow the loop
data52_80['TAVG_CELS'] = data52_80['TAVG_CELS'].astype(float)
pd
#create empty dataframe
referenceTemps = pd.DataFrame()

for key, group in grouped_Month:
    
    # Aggregate the data.  NB: the bracket has to be two for this. i.e "[[]]" and
    # one "[]". For the second method below which uses series, however, the reverse is the case.
   # mean_month= group[['ELEVATION', 'LATITUDE', 'LONGITUDE', 'DATE', 'PRCP', 'TAVG',
    #   'TMAX', 'TMIN', 'DATE_Month', 'Month', 'TAVG_CELS']].mean()
    mean_month= group[['TAVG_CELS']].mean()
    
    # Add the ´key´ (i.e. the date+time information) into the aggregated values
    mean_month['Month'] = key

    # Append the aggregated values into the DataFrame
    referenceTemps=referenceTemps.append(mean_month, ignore_index=True)


#rename column 'TAVG_CELS' before joining
dict = {'TAVG_CELS':'TAVG_CELS_28yrs'}
referenceTemps=referenceTemps.rename(columns=dict)   

#Another method to do it is below, but  the above seems to be better for me, as it includes the 
#original names of the columns. The second was only able to perform the operation on one
#column successfully. I'm just keeping for reference purpose.

#referenceTemps1 = pd.DataFrame()
#for key, group in grouped_Month:
    
    # Aggregate the data
#    mean_month= group['TAVG_CELS'].mean()
    
#    aggre= pd.Series([key, mean_month])
    # Add the ´key´ (i.e. the date+time information) into the aggregated values
   

    # Append the aggregated values into the DataFrame
#    referenceTemps1=referenceTemps1.append(aggre, ignore_index=True)


monthlyData = (pd.merge(monthlyData, referenceTemps, on= 'Month', how= 'outer'))
#sort the data according to the DATE_Month column.
monthlyData=monthlyData.sort_values(by='DATE_yrmo')

#alternative way to do the sorting
#monthlyData = monthlyData.sort('DATE_yrmo', ascending='True').reset_index()
monthlyData.columns

#convert 'TAVG_CELS' from object to float too, to allow the subtraction operation
monthlyData['TAVG_CELS'] = monthlyData['TAVG_CELS'].astype(float)
monthlyData['temp_anomalies'] = monthlyData['TAVG_CELS'] - monthlyData['TAVG_CELS_28yrs']
monthlyData.reset_index()

output1 = os.path.join(my_path, './helsinki.csv')
monthlyData.to_csv(output1, sep=',', index=False, float_format="%.2f")




