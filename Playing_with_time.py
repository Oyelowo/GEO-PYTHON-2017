# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 11:05:32 2018

@author: oyeda
"""

k=[]
for s in range(0,(24*60*60)):
        m=s/60
        h=m/60
        if h<12:
            a=('{0}:{1}:{2}am'.format("%.2d"%(h%12),"%.2d"%(m%60), "%.2d"%(s%60)))
            k.append(a)
        elif h<24:
            a=('{0}:{1}:{2}pm'.format("%.2d"%(h%12),"%.2d"%(m%60), "%.2d"%(s%60)))
            k.append(a) 
k
    