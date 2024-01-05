# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 20:40:51 2020

@author: torio
"""
primeCount=0
for i in range(2, 20000):
    isPrime= True
    for j in range(2, i): 
        if i%j==0: 
            isPrime= False

    if isPrime==True:
        print(i)
        primeCount= primeCount+1

print("The total number of primes is: "+ str(primeCount))
