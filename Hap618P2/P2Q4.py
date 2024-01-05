# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 20:30:20 2020

@author: torio
"""

list1=[1,2,5,6,3,77,9,0,3,23,0.4,-12.4,-3.12]
sum= 0
length= 0
for num in list1: 
    sum= sum+num
    #sum+=num # sum =8
    length= length+1

print("The mean value is: "+ str(sum/length))
