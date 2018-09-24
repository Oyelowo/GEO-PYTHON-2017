# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 14:16:31 2017

@author: oyeda
"""

# A list of night-time (00-08), day-time (08-16) and evening (16-24) temperatures for April 2013 
# measured in Helsinki Malmi Airport
temperatures = [-5.4, 1.0, -1.3, -4.8, 3.9, 0.1, -4.4, 4.0, -2.2, -3.9, 4.4,
                -2.5, -4.6, 5.1, 2.1, -2.4, 1.9, -3.3, -4.8, 1.0, -0.8, -2.8,
                -0.1, -4.7, -5.6, 2.6, -2.7, -4.6, 3.4, -0.4, -0.9, 3.1, 2.4,
                1.6, 4.2, 3.5, 2.6, 3.1, 2.2, 1.8, 3.3, 1.6, 1.5, 4.7, 4.0,
                3.6, 4.9, 4.8, 5.3, 5.6, 4.1, 3.7, 7.6, 6.9, 5.1, 6.4, 3.8,
                4.0, 8.6, 4.1, 1.4, 8.9, 3.0, 1.6, 8.5, 4.7, 6.6, 8.1, 4.5,
                4.8, 11.3, 4.7, 5.2, 11.5, 6.2, 2.9, 4.3, 2.8, 2.8, 6.3, 2.6,
                -0.0, 7.3, 3.4, 4.7, 9.3, 6.4, 5.4, 7.6, 5.2]

# Task 1 - Create empty lists for different temperature classes
# i.e. cold, slippery, comfortable, warm
# -------------------------------------------------------------

# Add your code here.

cold = []           #create an empty list for cold
slippery = []       #create an empty list for slippery
comfortable = []    #create an empty list for comfortable
warm = []           #create an empty list for warm

# Task 2 - Iterate over temperatures and add temperatures to different temperature classes
# as defined below:
#  1. Cold --> temperatures below -2 degrees (Celsius)
#  2. Slippery --> temperatures between -2 and +2 degrees (Celsius)
#  3. Comfortable --> temperatures between +2 and +15 degrees (Celsius)
#  4. Warm --> temperatures above +15 degrees (Celsius)
# ------------------------------------------------------------------------------------------

# Add your code here.
#iterate over temperature and assign various temperature ranges to the
#appropriate physiological feelings  by appending into the empty lists
#created earlier.
for temp in temperatures:
    if temp < -2:   cold.append('cold')
    elif temp >-2 and temp < 2 : slippery.append('slippery')
    elif temp > 2 and temp < 15:comfortable.append('comfortable')
    else: warm.append('warm')

# Task 3 - Questions - Print the answers
# --------------------------------------

# 1. How many times was it slippery during the study period?

# Edit these variable (i.e. replace XXX) by finding out how many values are withing different lists
#count how many times slippery occurs in the list where it has been appended
slippery_times = slippery.count('slippery')
#print this number of occurences as part of the sentence
print ("In April 2013 it was slippery", slippery_times, "times.")

# 2. How many times was it warm?
#count how many times warm condition occurs in the list where it has been appended
warm_times = warm.count('warm')
#print this number of occurences as part of the sentence
print ("In April 2013 it was warm ", warm_times, "times.")

#count how many times cold condition occurs in the list where it has been appended
# 3. How many times was it cold?
cold_times = cold.count('cold')
#print this number of occurences as part of the sentence
print ("In April 2013 it was cold ", cold_times, "times.")

#I also tried it for comfortable
#count how many times comfortable condition occurs in the list where it has been appended
comfortable_times = comfortable.count('comfortable')
#print this number of occurences as part of the sentence
print ("In April 2013 it was comfortable ", comfortable_times, "times.")




# Task 4 - EXTRA (optional)
# --------------------------

# Data values in the 'temperatures' list are grouped in a way that three values always comprise
# a single day. I.e. 
# The first value in the list is temperature for night-time (00-08) at day 1, 
# the second for day-time (08-16) at day 1, 
# and the third for evening (16-24) temperatures at day 1,
# whereas the fourth value is temperature for night-time (00-08) on the next day (day 2), etc.

# 1. Create empty lists for night, day, and evening temperatures


# Add your code here
night = []
day= []
evening=[]

# 2. Iterate over the temperature values and add the temperatures to corresponding lists

# Add your code here

# 3. What was the mean day-time temperature in April 2013?

# Add your code here that answers to the question
day.extend(temperatures[1::3])
print day
mean_temperature = sum(day)/len(day)
print("Mean day-time temperature was", mean_temperature)
