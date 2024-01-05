# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 20:33:01 2020

@author: torio
"""
list1=[1,2,5,6,3,77,9,0,3,23,0.4,-12.4,-3.12]

for i in range(1, len(list1)): # index=3
    a= list1[i] 
    b= list1[i-1]
    print(a-b)
