# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 09:39:38 2017

@author: oyeda
"""

import pandas as pd

data = pd.read_csv("C:/Users/oyeda/Desktop/AUTOGIS/ass6/6591337447542dat_August.txt",
                   na_values=["*", "**","***","****","*****"], sep ='\s+')

data.head()
data.columns

#select_cols = ['YR--MODAHRMN', 'DIR', 'SPD', 'GUS','TEMP', 'MAX', 'MIN']
#data = data[select_cols]

data = data[['YR--MODAHRMN', 'DIR', 'SPD', 'GUS','TEMP', 'MAX', 'MIN']]

data.tail()
data.columns
data.dtypes


name_conversion_dict = {'YR--MODAHRMN': 'TIME', 'SPD': 'SPEED', 'GUS': 'GUST'}
print(name_conversion_dict)
type(name_conversion_dict)

data = data.rename(columns=name_conversion_dict)

data.columns
data.describe()

data.head(30)


def fahrToCelsius(temp_fahrenheit):
    """
    Function to convert Fahrenheit temperature into Celsius.

    Parameters
    ----------

    temp_fahrenheit: int | float
        Input temperature in Fahrenheit (should be a number)
    """

    # Convert the Fahrenheit into Celsius and return it
    converted_temp = (temp_fahrenheit - 32) / 1.8
    return converted_temp
    
    
    
for idx, row in data.iterrows():
    print('Index:', idx)
    print('row: ', row)
    break
    
type(row)


# Create an empty column for the data
col_name = 'Celsius'
data[col_name] = None
#data['Celsius'] = None

# Iterate ove rows
for idx, row in data.iterrows():
  # Convert the Fahrenheit temperature of the row into Celsius
  celsius = fahrToCelsius(row['TEMP'])
  # Add that value into 'Celsius' column using the index of the row
  data.loc[idx, col_name] = celsius

data.head()

#conert speed m/s = mph x 0.44704
data['SPEED'] = data['SPEED']*0.44704

data['GUST'] = data['GUST']*0.44704

data.head(30)

data['TIME_str'] = data['TIME'].astype(str)

data.head()


data['TIME_str'].dtypes


type(data.loc[0, 'TIME_str'])


data['TIME_dh'] = data['TIME_str'].str.slice(start=0, stop=10)
data.head()


data['TIME_h'] = data['TIME_str'].str.slice(start=8, stop=10)

data['TIME_h'] = data['TIME_h'].astype(int)

data.head()



aggr_data = pd.DataFrame()
grouped = data.groupby('TIME_dh')
type(grouped)
len(grouped)


time1 = '2017080400'

group1 = grouped.get_group(time1)
group1

mean_cols = ['DIR', 'SPEED', 'GUST', 'TEMP', 'Celsius', 'TIME_h']

mean_values = group1[mean_cols].mean()

mean_values['TIME_dh'] = time1

aggr_data = aggr_data.append(mean_values, ignore_index=True)
aggr_data



for key, group in grouped:
       print(key)
       print(group)
       break
   
   
# Create an empty DataFrame for the aggregated values
aggr_data = pd.DataFrame()

# The columns that we want to aggregate
mean_cols = ['DIR', 'SPEED', 'GUST', 'TEMP', 'Celsius', 'TIME_h']

# Iterate over the groups
for key, group in grouped:
    # Aggregate the data
    mean_values = group[mean_cols].mean()

    # Add the ´key´ (i.e. the date+time information) into the aggregated values
    mean_values['TIME_dh'] = key

    # Append the aggregated values into the DataFrame
    aggr_data = aggr_data.append(mean_values, ignore_index=True)
    
aggr_data


#Finding outliers from the data
#Finally, we are ready to see and find out if there are any outliers in our data 
#suggesting to have a storm (meaning strong winds in this case). We define an outlier 
#if the wind speed is 2 times the standard deviation higher than the average wind speed 
#(column SPEED).

#Let’s first find out what is the standard deviation and the mean of the Wind speed.

std_wind = aggr_data['SPEED'].std()

avg_wind = aggr_data['SPEED'].mean()

print('Std:', std_wind)


print('Mean:', avg_wind)
#Mean: 5.153377777777777
#Okey, so the variance in the windspeed tend to be approximately 1.6 meters per second, and the wind speed is approximately 5.2 m/s. Hence, the threshold for a wind speed to be an outlier with our criteria is:

upper_threshold = avg_wind + (std_wind*2)

print('Upper threshold for outlier:', upper_threshold)

#Let’s finally create a column called Outlier which we update with True value if 
#the windspeed is an outlier and False if it is not. We do this again by iterating 
#over the rows.


# Create an empty column for outlier info
aggr_data['Outlier'] = None

# Iterate over rows
for idx, row in aggr_data.iterrows():
    # Update the 'Outlier' column with True if the wind speed is higher than our threshold value
    if row['SPEED'] > upper_threshold :
        aggr_data.loc[idx, 'Outlier'] = True
    else:
        aggr_data.loc[idx, 'Outlier'] = False
print(aggr_data)

storm = aggr_data.ix[aggr_data['Outlier'] == True]

print(storm)
print(storm['TIME_h'].value_counts())


gust_sort = storm.sort_values(by='GUST', ascending=False)






def fahrToCelsius(row, src_col, target_col):
    """
    A generic function to convert Fahrenheit temperature into Celsius.

    Parameters
    ----------

    row: pd.Series
        Input row containing the data for specific index in the DataFrame

    src_col : str
        Name of the source column for the calculation. I.e. the name of the column where Fahrenheits are stored.

    target_col : str
        Name of the target column where Celsius will be stored.
    """
    # Convert the Fahrenheit into Celsius and update the target column value
    row[target_col] = (row[src_col]- 32) / 1.8
    return row
    
    
    
    
    
data2 = data.copy()
data2 = data2.apply(fahrToCelsius, src_col='TEMP', target_col='Celsius2', axis=1)
data2.head()


data2 = data2.apply(fahrToCelsius, src_col='TEMP', target_col='Celsius3', axis=1)
data2.head()
