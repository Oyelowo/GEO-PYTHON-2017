# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 20:01:29 2017

@author: oyeda
"""

import pandas as pd
data= pd.read_csv('C:/Users/oyeda/Desktop/AUTOGIS/ass6/1099875.txt' , 
                  sep= '\s+', skiprows=[1], na_values='-9999')


#Calculate the average temperature using columns TMAX and TMIN and insert those values
#into a new column called TAVG.

data['TAVG'] = (data['TMAX'] + data['TMIN'])/2

def fahrToCelsius(row, source, target):
     '''funtion to convert tempperature in fahrenheit to celsius in a column
    source: the colum with the temperature in fahrenheit
    target: created column with converted temperature in celsius
    '''
     row[target]=(row[source] - 32)/1.8
     return row


data = data.apply(fahrToCelsius, source='TAVG', target='TAVG_CELS', axis=1)

#Next, you should use the approaches learned during this week and the same approaches
#as in Problem 3 to answer / do:

#Calculate the temperature anomalies in Sodankyla, i.e. the difference between referenceTemps
#and the average temperature for each month (see Problem 3).
data.columns
data['DATE_str'] = data['DATE'].astype(str)

data['DATE_yrmo'] = data['DATE_str'].str.slice(start=0, stop=6)

data['Month'] = data['DATE_str'].str.slice(start=4, stop=6)

data['DATE_yrmo'] = data['DATE_yrmo'].astype(int)

data['Month'] = data['Month'].astype(int)


grouped_Month = data.groupby('DATE_yrmo')
len(grouped_Month)
dataMonths2 = pd.DataFrame()

#calculate the monthly average for the columns
for key, group in grouped_Month:
    Tmean_Month = group[['ELEVATION','LATITUDE', 'LONGITUDE', 'DATE', 'PRCP', 
    'TMAX', 'TMIN', 'TAVG', 'TAVG_CELS','Month']].mean()
    Tmean_Month['DATE_yrmo'] = key
    dataMonths2=dataMonths2.append(Tmean_Month, ignore_index=True)
    
    


dataMonths2.head()

monthlyData2= dataMonths2.copy()

#convert to integer. if the mean was derived earlier, wouldnt have to do this anymore.
monthlyData2['DATE_yrmo'] = monthlyData2['DATE_yrmo'].astype(int)

#select 28 years from 1959
data59_87= (monthlyData2.ix[(monthlyData2['DATE_yrmo'] >= 195901) & 
            (monthlyData2['DATE_yrmo'] <= 198712)]).reset_index(drop=True)



grouped_Month59_87 = data59_87.groupby('Month')

referenceTemps2 = pd.DataFrame()

#calculate the avergae monthly temperature for 28 years from the beginning of the data
for key, group in grouped_Month59_87:
    mean_month_59_87 = group[['TAVG_CELS']].mean()
    mean_month_59_87['Month'] = key
    referenceTemps2 = referenceTemps2.append(mean_month_59_87, ignore_index=True)
    
dict =  {'TAVG_CELS': 'TAVG_CELS_59_87'}
referenceTemps2=referenceTemps2.rename(columns=dict)

#merge the monthly data and the reference monthly temperatures
monthlyData2 = pd.merge(monthlyData2, referenceTemps2, on= 'Month', how='outer')

#sort the data chronologically according to the YEARMONTH
monthlyData2=monthlyData2.sort_values('DATE_yrmo', ascending=True)

monthlyData2['temp_anomalies'] = monthlyData2['TAVG_CELS'] - monthlyData2['TAVG_CELS_59_87']


#import the Helsinki monthly temperature data
helsinkiData = pd.read_csv('C:/Users/oyeda/Desktop/AUTOGIS/ass6/helsinki.csv'
                           ,sep=',') 

helsinkiData.columns

hData= helsinkiData[['DATE_yrmo','TAVG_CELS']]
diction= {'TAVG_CELS' :'H_TAVG_CELS'}
hData= hData.rename(columns=diction)

sData= monthlyData2[['DATE_yrmo','Month','TAVG_CELS']]
diction2= {'TAVG_CELS' :'S_TAVG_CELS'}
sData= sData.rename(columns=diction2)
HS_merged = pd.merge(hData, sData, on='DATE_yrmo')

#Calculate the monthly temperature differences between Sodankyla and Helsinki stations
HS_merged['temp_difference'] = HS_merged['S_TAVG_CELS'] - HS_merged['H_TAVG_CELS']

#How different the summer temperatures (June, July, August) have been between Helsinki 
#(used in Problems 1-3) and Sodankyla station?
HsummerTemp = HS_merged.ix[(HS_merged['Month']>=6) & (HS_merged['Month']<=8)]

HsummerTemp['DATE_yrmo_str'] = HsummerTemp['DATE_yrmo'].astype(str)
HsummerTemp['year'] = HsummerTemp['DATE_yrmo_str'].str.slice(start=0, stop=4)


#next thing is to aggregate the data
groupyear= HsummerTemp.groupby('year')
len(groupyear)
HsummerTemp.columns
HS_summer59_17= pd.DataFrame()

for key, group in groupyear:
    mean_year =group[['H_TAVG_CELS', 'S_TAVG_CELS', 'temp_difference']].mean()
    mean_year['year']=key
    HS_summer59_17=HS_summer59_17.append(mean_year, ignore_index=True)
    
   
#Calculate the monthly differences into a DataFrame and save it (as CSV file) into your own 
#Exercise repository for this week
output ='C:/Users/oyeda/Desktop/AUTOGIS/ass6/Helsinki_Sodankyla_Monthly_Temp.csv'
HS_merged.to_csv(output, sep=',', index=False, float_format="%.2f")



output2 ='C:/Users/oyeda/Desktop/AUTOGIS/ass6/sodankyla.csv'
monthlyData2.to_csv(output2, sep=',', index=False, float_format="%.2f")

#What were the summer mean temperatures for both of these stations?
H_Tmean= HS_summer59_17['H_TAVG_CELS'].mean()
print('The average summer temperature in Helsinki between 1959 and 2017 is', "%.2f"%H_Tmean)


S_Tmean= HS_summer59_17['S_TAVG_CELS'].mean()
print('The average summer temperature in Sodankyla between 1959 and 2017 is', "%.2f"%S_Tmean)


#What were the summer standard deviations for both of these stations?
H_Tstd= HS_summer59_17['H_TAVG_CELS'].std()
print('The Standard deviation of summer temperature in Helsinki between 1959 and 2017 is', "%.2f"%H_Tstd)


S_Tstd= HS_summer59_17['S_TAVG_CELS'].std()
print('The Standard deviation of summer temperature in Sodankyla between 1959 and 2017 is', "%.2f"%S_Tstd)


#Upload your script and data to GitHub.