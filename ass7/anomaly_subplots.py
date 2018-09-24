# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 22:30:26 2017

@author: oyeda
"""
import pandas as pd
import matplotlib.pyplot as plt


#The goal for this problem is to make this plot.

#For Problem 2, the goal is to recreate the plot above, a 4-panel plot showing seasonal 
#temperature anomalies from 1953-2016. To do this, you should:

#Start by creating a new Python script called anomaly_subplots.py and performing steps 
#1-3 from Problem 1 to prepare the data for plotting.
#Create a yearly Pandas datetime index from 1953-2016 using the pd.date_range() function.
#Create an empty Pandas DataFrame called seasonalData using the index you just created
#and column titles 'Winter', 'Spring', 'Summer', and 'Fall'.
#Fill the data frame with mean temperatures for each season in each year.
#Assume that Winter is December-February, Spring is March-May, Summer is June-
#August, and Fall is September-November.
#Create a figure with 4 subplots in the arrangement shown above, labeling axes as needed, 
#with gridlines on, and with a line legend for each panel.
#You can find tips about these different plot features in the Matplotlib documentation 
#and the hints for this week's exercise.
#Save your Python script in GitHub and include a copy of the plot it produces in
#your answer to Problem 2 below.


data_h = pd.read_csv('C:/Users/oyeda/Desktop/AUTOGIS/ass7/helsinki.csv', sep=',', parse_dates=['DATE_yrmo'])

data_h['DATE_yrmo'] = pd.to_datetime(data_h['DATE_yrmo'], format = '%Y%m')
data_h = data_h.set_index('DATE_yrmo')


#create the time index for 1953 till 2016
timeindex = pd.date_range('1953', '2016', freq='AS')


seasonalData = pd.DataFrame(index=timeindex, columns=['Winter', 'Spring', 'Summer', 'Fall'])

for i in range(1953,2017):
     current =i
     previous = i-1
     meanValue = data_h[str(previous)+'-12':str(current)+'-2']['temp_anomalies'].mean()
     seasonalData.loc[str(i), 'Winter'] = meanValue
 
     meanValue1 = data_h[str(current)+'-3':str(current)+'-5']['temp_anomalies'].mean()
     seasonalData.loc[str(i), 'Spring'] = meanValue1

     meanValue2 = data_h[str(current)+'-6':str(current)+'-8']['temp_anomalies'].mean()
     seasonalData.loc[str(i), 'Summer'] = meanValue2
     meanValue3 = data_h[str(current)+'-9':str(current)+'-11']['temp_anomalies'].mean()
     seasonalData.loc[str(i), 'Fall'] = meanValue3

#or simply doing it more directly
#for i in range(1953,2017):
     
     #meanValue = data_h[str(i-1)+'-12':str(i)+'-2']['temp_anomalies'].mean()
     #season_Temp.loc[str(i), 'Winter'] = meanValue
     
     #NB: this can also be done by using the string formating but the first solution is more concise
     #current =i
     #previous = i-1
     #meanValue = data_h[('{previous}-12').format(previous=i-1):('{current}-2').format(current=i)]['temp_anomalies'].mean()
     #seasonalData.loc[str(i), 'Winter'] = meanValue


 
     #meanValue1 = data_h[str(i)+'-3':str(i)+'-5']['temp_anomalies'].mean()
     #season_Temp.loc[str(i), 'Spring'] = meanValue1

     #meanValue2 = data_h[str(i)+'-6':str(i)+'-8']['temp_anomalies'].mean()
     #season_Temp.loc[str(i), 'Summer'] = meanValue2
     #meanValue3 = data_h[str(i)+'-9':str(i)+'-11']['temp_anomalies'].mean()
     #season_Temp.loc[str(i), 'Fall'] = meanValue3
     

#creating the subplots
winter= seasonalData['Winter']
spring= seasonalData['Spring']
summer= seasonalData['Summer']
fall= seasonalData['Fall']

#create a panel 2 X 2 with  subplots
#fig, axes=plt.subplots(ncols=2, nrows=2,, figsize=(12,8))

#instead of giving same x and ylabels to individual plot, I decided to use one for all
#since they share thesame xlabel and ylabel. to do it individually, I could just use
#ylabel='Temperature(°celsius)', xlabel='date, in individual subplots, but I choose
#this because I think it is more elegant.

fig, axes = plt.subplots(nrows=2, ncols=2,figsize=(12, 8))

#the below is if I want them to share thesame axes and the numbers don't have to be
#repeated on all subplots
#fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True, figsize=(12, 8))
fig.text(0.5, 0.04, 'Date', ha='center')
fig.text(0.04, 0.5, 'Temperature(°celsius)', va='center', rotation='vertical')

#create main title for all plots
plt.suptitle('Seasonal variation in Temperature Anomalies in Helsinki 1953-2016', size=20)
plt.style.use('seaborn-whitegrid')

#parse the axes from the axarray
ax11 =  axes[0][0]
ax12 =  axes[0][1]
ax21 =  axes[1][0]
ax22 =  axes[1][1]



#create the subplots
#winter.plot(x= winter.index, y = 'TAVG_CELS', legend='winter', ylim=(y.max()+5,y.min()-5), ax=ax11, lw=2, c='blue')
winter.plot(x= winter.index, y = 'temp_anomalies', legend='winter', ylim=(-10,10), ax=ax11, lw=2, c='blue')
spring.plot(x= spring.index, y = 'temp_anomalies', legend='spring', ylim=(-10, 10),  ax=ax12, lw=2, c='orange')
summer.plot(x= summer.index, y = 'temp_anomalies', legend='summer', ylim=(-10, 10),  ax=ax21, lw=2, c='red')
fall.plot(x= fall.index, y = 'temp_anomalies', legend='fall', ylim=(-10, 10),  ax=ax22, lw=2, c='purple')
plt.show()

import os
myfolder = r"C:\Users\oyeda\Desktop\AUTOGIS\ass7\other_plots"
filename = "anomally_subplots.png"
filepath = os.path.join(myfolder, filename)
plt.savefig(filepath)
