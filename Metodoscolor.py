# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 13:55:19 2019

@author: Rene
"""
import math
import cv2
import numpy as np
class RGBSeparar:
    def __init__(self, I,C):
        self.I=I
        self.C=C     
    def MRed(self, I,C):
        M,N = I.shape
        #print("M: "+str(M)+", N: "+str(N))
        h = np.zeros((M,N), I.dtype) 
        V = np.array([0,0,0])
        for m in range(0,M):
            for n in range(0,N):
                V = C[m,n]
                h[m,n] = V[0]

        return h    
    def MGreen(self, I,C):
        M,N = I.shape
        #print("M: "+str(M)+", N: "+str(N))
        h = np.zeros((M,N), C.dtype) 
        V = np.array([0,0,0])
        for m in range(0,M):
            for n in range(0,N):
                V = C[m,n]
                h[m,n] = V[1]

        return h    
    def MBlue(self, I,C):
        M,N = I.shape
        #print("M: "+str(M)+", N: "+str(N))
        h = np.zeros((M,N), C.dtype) 
        V = np.array([0,0,0])
        for m in range(0,M):
            for n in range(0,N):
                V = C[m,n]
                h[m,n] = V[2]

        return h  
    def Mcolor(self, I,C,F):
        M,N = I.shape
        #print("M: "+str(M)+", N: "+str(N))
        
        V = np.array([0,0,0])
        for m in range(0,M):
            for n in range(0,N):
                V = C[m,n]
                
                V = [(V[0]*F[0]),(V[1]*F[1]),(V[2]*F[2])]
                C[m,n] = V

        return C      
    def Msumacolor(self,C,R,G,B,I):
        M,N = I.shape
        #print("M: "+str(M)+", N: "+str(N))
          
        for m in range(0,M):
            for n in range(0,N):
                VR = R[m,n]
                VG = G[m,n]
                VB = B[m,n]                
                V = [(VR),(VG),(VB)]
                C[m,n] = V

        return C    
