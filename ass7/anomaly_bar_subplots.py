# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 21:15:42 2017

@author: oyeda
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 22:04:03 2017

@author: oyeda
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 10:17:01 2017

@author: oyeda
"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
#The goal for this problem is to make this kind of animation.

#For Problem 3, the goal is to recreate 65 individual bar plots that can be animated 
#like the animation above that shows the variation in seasonal temperature anomalies 
#from 1953-2016.

#To do this, you should:

#Start by creating a new Python script called anomaly_barplots.py. You should use the same 
#data as in Problem 2.
data_h = pd.read_csv('C:/Users/oyeda/Desktop/AUTOGIS/ass7/helsinki.csv', sep=',', parse_dates=['DATE_yrmo'])

data_s = pd.read_csv('C:/Users/oyeda/Desktop/AUTOGIS/ass7/sodankyla.csv', sep=',', parse_dates=['DATE_yrmo'])


#You should select data for each season of each year between 1953-2017 using the techniques 
#that you have learned during the Lesson 7.
#Assume that Winter is December-February, Spring is March-May, Summer is June-August, 
#and Fall is September-November.
#You should calculate the mean temperature of the weather anomalies (outcome from Problem 3
#in Exercise 6 last week) based on the selected data for each season of the year. 
#You should end up having altogether four values for each year (i.e. one for winter, 
#spring, summer, and fall).

data_h['DATE_yrmo'] = pd.to_datetime(data_h['DATE_yrmo'], format = '%Y%m')
data_h = data_h.set_index('DATE_yrmo')

data_s['DATE_yrmo'] = pd.to_datetime(data_s['DATE_yrmo'], format = '%Y%m')
data_s = data_s.set_index('DATE_yrmo')

#create the time index for 1953 till 2016
timeindex_h = pd.date_range('1953', '2016', freq='AS')

timeindex_s = pd.date_range('1959', '2016', freq='AS')


seasonalData_h = pd.DataFrame(index=timeindex_h, columns=['Winter', 'Spring', 'Summer', 'Fall'])

seasonalData_s = pd.DataFrame(index=timeindex_s, columns=['Winter', 'Spring', 'Summer', 'Fall'])

for i in range(1960,2017):
     current =i
     previous = i-1
     meanValue = data_h[str(previous)+'-12':str(current)+'-2']['temp_anomalies'].mean()
     seasonalData_h.loc[str(i), 'Winter'] = meanValue
 #    plt.plot(seasonalData.index[0], seasonalData.iloc[:,[0,1,2,3],], kind='bar')
 
     meanValue1 = data_h[str(current)+'-3':str(current)+'-5']['temp_anomalies'].mean()
     seasonalData_h.loc[str(i), 'Spring'] = meanValue1

     meanValue2 = data_h[str(current)+'-6':str(current)+'-8']['temp_anomalies'].mean()
     seasonalData_h.loc[str(i), 'Summer'] = meanValue2

     meanValue3 = data_h[str(current)+'-9':str(current)+'-11']['temp_anomalies'].mean()
     seasonalData_h.loc[str(i), 'Fall'] = meanValue3


for i in range(1960,2017):
     current =i
     previous = i-1
     meanValue = data_s[str(previous)+'-12':str(current)+'-2']['temp_anomalies'].mean()
     seasonalData_s.loc[str(i), 'Winter'] = meanValue
 #    plt.plot(seasonalData.index[0], seasonalData.iloc[:,[0,1,2,3],], kind='bar')
 
     meanValue1 = data_s[str(current)+'-3':str(current)+'-5']['temp_anomalies'].mean()
     seasonalData_s.loc[str(i), 'Spring'] = meanValue1

     meanValue2 = data_s[str(current)+'-6':str(current)+'-8']['temp_anomalies'].mean()
     seasonalData_s.loc[str(i), 'Summer'] = meanValue2

     meanValue3 = data_s[str(current)+'-9':str(current)+'-11']['temp_anomalies'].mean()
     seasonalData_s.loc[str(i), 'Fall'] = meanValue3


import os
myfolder = r"C:\Users\oyeda\Desktop\AUTOGIS\ass7\plots2"

#extra note for me: I can use the above instead of having to change the 
#backslash to forward slash juse use r before the filepath
#myfolder = "C:/Users/oyeda/Desktop/AUTOGIS/ass7/plots"
plt.ioff()
#until plt.show()
for i in range(1960, 2017):
    #seasonalData[str(i)].plot(kind='bar', title ="Seasonal anomalies", ylim=(-5,5), figsize=(15, 10), legend=True, fontsize=12)
    
    


    #fig, axes = plt.subplots(nrows=2, ncols=1,figsize=(12, 8))

#the below is if I want them to share thesame axes and the numbers don't have to be
#repeated on all subplots
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True, figsize=(12, 8))
    fig.text(0.5, 0.04, str(i), ha='left')
    fig.text(0.04, 0.5, 'Temperature anomalies(°celsius)' , fontsize=23 , va='center', rotation='vertical')

#create main title for all plots
    plt.suptitle('Seasonal variation in Temperature Anomalies in Helsinki  ' + str(i) , size=20)
    plt.style.use('seaborn-whitegrid')

#parse the axes from the axarray
    ax11 =  axes[0]
    ax12 =  axes[1]




#create the subplots
#winter.plot(x= winter.index, y = 'TAVG_CELS', legend='winter', ylim=(y.max()+5,y.min()-5), ax=ax11, lw=2, c='blue')
    seasonalData_h[str(i)].plot(kind='bar', ylim=(-6,6),ax=ax11, figsize=(15, 10), legend=True, fontsize=12)
    #plt.title('Helsinki'+ str(i), fontsize=23)
    
    seasonalData_s[str(i)].plot(kind='bar', ylim=(-6,6),ax=ax12, figsize=(15, 10), title="Sodankyla", legend=False, fontsize=12)
    plt.title('Seasonal variation in Temperature Anomalies in Sodankyla  '+ str(i), fontsize=23)
    #plt.ylabel('Temperature anomalies(°celsius)', fontsize=17)
    #plt.xlabel(str(i), fontsize=13)
    
    plt.style.use('seaborn-whitegrid')
    filename = "My_File_" + str(i) + ".png"
    filepath = os.path.join(myfolder, filename)
    plt.savefig(filepath)
    
    
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 21:15:42 2017

@author: oyeda
"""

import glob
import imageio

# Find all files from given folder that has .png file-format
search_criteria = r"C:\Users\oyeda\Desktop\AUTOGIS\ass7\plots2\*.png"

# Execute the glob function that returns a list of filepaths
figure_paths = glob.glob(search_criteria)

# Save the animation to disk with 48 ms durations
output_gif_path = r"C:\Users\oyeda\Desktop\AUTOGIS\ass7\animated_plot\Animated_helsinki_sodankyla.gif"
imageio.mimsave(output_gif_path, [imageio.imread(fp) for fp in figure_paths], duration=0.51, subrectangles=True)
