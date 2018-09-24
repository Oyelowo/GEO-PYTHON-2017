# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 11:15:48 2017

@author: oyeda
"""

##You should do following (also criteria for grading):

#Create a function called fahrToCelsius in functions.py
#The function should have one input parameter called tempFahrenheit
#Inside the function, create a variable called convertedTemp to which you should
#assign the conversion result (i.e., the input Fahrenheit temperature converted to Celsius)
#The conversion formula from Fahrenheit to Celsius is:

#Return the converted value from the function back to the user
#Comment your code and add a docstring that explains how to use your fahrToCelsius function 
#(i.e., you should write the purpose of the function, parameters, and returned values)


def fahrToCelsius(tempFahrenheit):   #define function to convert parameter(tempFahrenheit)
    """
    Function for converting temperature in Fahrenheit to Celsius.

    Parameters
    ----------
    tempFahrenheit: <numerical>
        Temperature in Fahrenheit
    convertedTemp: <numerical>
        Target temperature in Celsius

    Returns
    -------
    <float>
        Converted temperature.
        """
    convertedTemp = (tempFahrenheit - 32)/1.8   #assign the conversion to convertedTemp variable
    return convertedTemp                         #return the converted temperature variable


#What is 48° Fahrenheit in Celsius? ==> Add your answer here:
fahrToCelsius(48)

#What about 71° Fahrenheit in Celsius? ==> Add your answer here:
fahrToCelsius(71)

print ("32 degrees Fahrenheit in Celsius is:", fahrToCelsius(32))

#check what the function does by using help function which returns the docstring comments
help(fahrToCelsius)

#0	temperatures below -2 degrees (Celsius)
#1	temperatures from -2 up to +2 degrees (Celsius) [1]
#2	temperatures from +2 up to +15 degrees (Celsius) [2]
#3	temperatures above +15 degrees (Celsius)

def tempClassifier(tempCelsius):   #define the function of the parameter(tempCelsius)
    """
    Function for classifying temperature in celsius.

    Parameters
    ----------
    tempCelsius: <numerical>
        Temperature in Celsius

    Returns
    -------
    <integer>
        Classified temperature.
        """
        
#conditional statements to assign temperatues to  different values/classes
    if tempCelsius < -2: return 0
    elif tempCelsius >= -2 and tempCelsius<=2: return 1
    elif tempCelsius >= 2 and tempCelsius<=15: return 2
    else: return 3
    
#What is class value for 16.5 degrees (Celsius)? ==> Add your answer here:
tempClassifier(16.5)

#What is the class value for +2 degrees (Celsius)? ==> Add your answer here:
tempClassifier(2)
tempClassifier(15)
