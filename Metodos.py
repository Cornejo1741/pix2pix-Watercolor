import math
import cv2
import numpy as np
class operaciones:

    def __init__(self, I, f ,G):
        self.I=I
        self.f=f  
        self.G=G 
    def recortar(self, I,G):
        M,N = I.shape
        LadoMENOR = 0
        corrM = 0
        corrN = 0
        if (I.shape[0]<I.shape[1]):
            LadoMENOR = I.shape[0]
        else:
            LadoMENOR = I.shape[1]
        corrM = int((M/2)-(LadoMENOR/2))
        corrN = int((N/2)-(LadoMENOR/2))
        #print("M: "+str(M)+", N: "+str(N))
        #print("Lado menor: "+str(LadoMENOR))
        #print("prueva M<-: "+str(corrM))
        #print("prueva M->: "+str((int)(abs((M/2)-(LadoMENOR/2))+LadoMENOR)))        
        #print("prueva N<-: "+str(corrN))
        #print("prueva N->: "+str((int)(abs((N/2)-(LadoMENOR/2))+LadoMENOR)))        
        h = np.zeros((LadoMENOR,LadoMENOR), G.dtype)
        h = cv2.cvtColor(h,cv2.COLOR_GRAY2BGR)
        k=0
        l=0
        Vector = np.array([0,0,0])
        for m in range((int)(abs((M/2)-(LadoMENOR/2))),(int)(abs((M/2)-(LadoMENOR/2))+LadoMENOR)):
            for n in range((int)(abs((N/2)-(LadoMENOR/2))),(int)(abs((N/2)-(LadoMENOR/2))+LadoMENOR)):
                k=m-corrM
                l=n-corrN  
                Vector = G[m,n]
                h[k,l]= Vector

                      
        return h
    def erocion(self, I, f):
        M,N = I.shape
        #print("M: "+str(M)+", N: "+str(N))
        K,L = f.shape
        h = np.zeros((M,N), I.dtype)
    
        padding_size = int((K)/2)

        for m in range((int)((f.shape[0]-1)/2),(int)(I.shape[0]-(f.shape[0]-1)/2)):
            for n in range((int)((f.shape[1]-1)/2),(int)(I.shape[1]-(f.shape[1]-1)/2)):
                maximo = I[m,n]
                for k in range(0,K):
                    for l in range(0,L):
                        if(f[k][l]==1):
                           Tem =I[m+k-(int)((f.shape[0]-1)/2)][n+l-(int)((f.shape[1]-1)/2)]
                           if(maximo>Tem):
                                maximo = Tem
                    h[m,n]=maximo
        return h
    def umbralbin(self, I, U):
        M,N = I.shape
        #print("M: "+str(M)+", N: "+str(N))
 
        h = np.zeros((M,N), I.dtype)


        for m in range(0,I.shape[0]):
            for n in range(0,I.shape[1]):
                if(U<I[m][n]):
                    h[m,n]=255
                else:
                    h[m,n]=0
        return h
    def desumbralbin(self, I):
        M,N = I.shape
        #print("M: "+str(M)+", N: "+str(N))
 
        h = np.zeros((M,N), I.dtype)


        for m in range(0,I.shape[0]):
            for n in range(0,I.shape[1]):
                if(I[m][n]==1):
                    h[m,n]=255
                elif(I[m][n]==0):
                    h[m,n]=122                    
                else:
                    h[m,n]=0
        return h
    def interseccion(self, I,F):
        M,N = I.shape
        #print("M: "+str(M)+", N: "+str(N))
 
        h = np.zeros((M,N), I.dtype)


        for m in range(0,I.shape[0]):
            for n in range(0,I.shape[1]):
                if(I[m][n]==F[m][n]):
                    h[m,n]=I[m][n]
                else:
                    h[m,n]=-1
        return h   
    def complemento(self, I):
        M,N = I.shape
        #print("M: "+str(M)+", N: "+str(N))
 
        h = np.zeros((M,N), I.dtype)


        for m in range(0,I.shape[0]):
            for n in range(0,I.shape[1]):
                if(I[m][n]==1):
                    h[m,n]=0
                else:
                    h[m,n]=1
        return h      

