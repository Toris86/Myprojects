# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 20:21:44 2020

@author: torio
"""
list1=[1,2,5,6,3,77,9,0,3,23,0.4,-12.4,-3.12]

smallest= list1[0] 
for num in list1:
    if num<smallest:
        smallest= num

print("The smallest number in the list is: "+ str(smallest))
