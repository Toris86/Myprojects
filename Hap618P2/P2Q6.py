# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 20:35:14 2020

@author: torio
"""
limit= int(input("Enter the limit for the fibonacci series: ")) 
#I set limit to 6 when I ran the code

a= 1
b=1
series= [a,b]  # series= [1,1, 2, 3, 5]
for i in range(2, limit):
    c= a+b # c= 5
    a= b # a=3
    b= c # b= 5
    series.append(b)

number=  int(input("Enter the number you want to check: "))
if  number in series:
    print("The number is part of the fibonacci")
else:
    print("The number is not part of the fibonacci")
