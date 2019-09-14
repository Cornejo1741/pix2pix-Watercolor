# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 13:28:25 2019

@author: Rene
"""



import numpy as np
import cv2
from Metodos import operaciones
from Metodoscolor import RGBSeparar
MB=np.array([[0,0,1,0,0],
             [0,1,1,1,0],
             [1,1,1,1,1],
             [0,1,1,1,0],
             [0,0,1,0,0]])
tamaño =286
dim = (tamaño, tamaño)
U = 180
nombre  = 'Pintura-'
nombre3 = '.jpg'
inicial = 1
final = 400
Fac = 0.4
Fac2 = 0.7
for Num in range(inicial,final+1):
    
    nombre2 = (str)(Num)
    print(nombre+nombre2+nombre3)
    img = cv2.imread(nombre+nombre2+nombre3)
    imgcont = img
    imgcont2 = img    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    MOD   = operaciones(gray,MB,img)
    color = RGBSeparar(gray,img)  
    MOD2   = operaciones(gray,MB,imgcont)
    color2 = RGBSeparar(gray,imgcont)      
    Original = MOD.recortar(gray,img)
    Original  = cv2.resize(Original,  dim, interpolation = cv2.INTER_AREA)
    
    #######################EROSION##########################################
    R  = color.MRed(gray,img)
    G  = color.MGreen(gray,img)  
    B  = color.MBlue(gray,img)  
    R2 = R
    G2 = G
    B2 = B
    R2 = MOD2.umbralbin(R2,U)
    G2 = MOD2.umbralbin(G2,U)  
    B2 = MOD2.umbralbin(B2,U)     
    
    #cv2.imshow('Rojo',R)
    #cv2.imshow('Verde',G)
    #cv2.imshow('Azul',B)

    
    R = MOD.erocion(R,MB)
    G = MOD.erocion(G,MB)
    B = MOD.erocion(B,MB)
    R3 = cv2.addWeighted(R,Fac,R2,(1-Fac),0)
    G3 = cv2.addWeighted(G,Fac,G2,(1-Fac),0)
    B3 = cv2.addWeighted(B,Fac,B2,(1-Fac),0)
    
    img = color2.Msumacolor(imgcont,R3,G3,B3, gray)
    ########################EROCION#########################################
    img = cv2.addWeighted(img,Fac2,imgcont2,(1-Fac2),0)
    
    img = MOD.recortar(gray,img)
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
     
    cv2.imwrite('M-'+nombre+nombre2+nombre3,img)
    cv2.imwrite(nombre+nombre2+nombre3,Original)

