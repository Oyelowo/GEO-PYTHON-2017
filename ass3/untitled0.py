# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 08:54:32 2017

@author: oyeda
"""

word = 'lowo'
print word[0]
print word[1]
print word[2]
print word[3]


word2 = "mayor"
for char in word2: print (char)

length = 10
for letter in 'geomatics': length = length + 1
print length

for letter in 'dayom': print (letter)
print (letter)

for value in range(8): print(value)

mylist =  [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
print (mylist)

for i in range(6): mylist[i]=mylist[i]+i
print(mylist)
for i in range(6): mylist[i]=mylist[i]+i
print(mylist)

mylist.append(19.0)
mylist.append(49)

for i in range(len(mylist)): mylist[i]= mylist[i]+i
    print(mylist)



for i in range(len(mylist)): mylist[i]=mylist[i]+i
print(mylist)
help(range)


for y in range(2, 9, 3): print(y)

words = 'ice pellets'
for i in range(len(words)): print(words[i])


yesterday = 14
today = 10
tomorrow = 13

if yesterday <= today:
    print('A')
elif today != tomorrow:
    print('B')
elif yesterday > tomorrow:
    print('C')
elif today == today:
    print('D')
    
    
if (1 > 0) and (-1 > 0): 
    print('Both parts are true')
else:
    print('One part is not true')
  

if (1 < 0) or (-1 < 0):
    print('At least one test is true')


In [11]: weather = 'Rain'

In [12]: wind = 'Windy'

In [13]: if (weather == 'Rain') and (wind == 'Windy'):
   ....:      print('Just stay home')
   ....: elif weather == 'Rain':
   ....:      print('Wear a raincoat')
   ....: else:
   ....:      print('No raincoat needed')
   
   
   
   
