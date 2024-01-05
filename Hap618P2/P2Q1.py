# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 20:13:23 2020

@author: torio
"""

num1= int(input("Enter first number: "))# num1= 6
num2= int(input("Enter second number: "))# num2= 2
num3= int(input("Enter third number: "))#num3=4
num4= int(input("Enter fourth number: "))# num4= 9
num5= int(input("Enter fifth number: "))# num5= 10

numbers= [num1, num2, num3, num4, num5] # numbers= [6,2,4,9,10]

maxValue= num1 # maxValue= 10
for num in numbers: # num= 10
    if num> maxValue:
        maxValue= num

print("The maximum value is:"+ str(maxValue))

