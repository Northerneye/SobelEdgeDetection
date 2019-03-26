import os 
import numpy as np
from PIL import Image
import math
filename = input("filename: ")
openThis = filename+".jpg"

kernelSize = int(input("kernel size(3,5): "))

def nonlin(x,deriv=False):
	if(deriv==True):
		return x*(1-x)
	return 1/(1+np.exp(-x))

accuracy = float(input("Limit(0-1): ")) #number 0-1, .1 works well

amplify = int(input("amplification: "))#3 works well

def xKernel3(imageArray, xpos, ypos):
    value = [0,0,0]
    for x in range(3):
        value[x] += imageArray[xpos-1][ypos][x]*-2/4
        value[x] += imageArray[xpos+1][ypos][x]*2/4
        value[x] += imageArray[xpos-1][ypos-1][x]*-1/4
        value[x] += imageArray[xpos-1][ypos+1][x]*-1/4
        value[x] += imageArray[xpos+1][ypos-1][x]*1/4
        value[x] += imageArray[xpos+1][ypos+1][x]*1/4
    return value
def yKernel3(imageArray, xpos, ypos):
    value = [0,0,0]
    for x in range(3):
        value[x] += imageArray[xpos][ypos-1][x]*-2/4
        value[x] += imageArray[xpos][ypos+1][x]*2/4
        value[x] += imageArray[xpos-1][ypos-1][x]*-1/4
        value[x] += imageArray[xpos+1][ypos-1][x]*-1/4
        value[x] += imageArray[xpos-1][ypos+1][x]*1/4
        value[x] += imageArray[xpos+1][ypos+1][x]*1/4
    return value
def xKernel5(imageArray, xpos, ypos):
    value = [0,0,0]
    for x in range(3):
        value[x] += imageArray[xpos-1][ypos][x]*-6/27
        value[x] += imageArray[xpos+1][ypos][x]*6/27
        value[x] += imageArray[xpos-1][ypos-1][x]*-4/27
        value[x] += imageArray[xpos-1][ypos+1][x]*-4/27
        value[x] += imageArray[xpos+1][ypos-1][x]*4/27
        value[x] += imageArray[xpos+1][ypos+1][x]*4/27
        value[x] += imageArray[xpos-1][ypos-2][x]*-2/27
        value[x] += imageArray[xpos-1][ypos+2][x]*-2/27
        value[x] += imageArray[xpos+1][ypos-2][x]*2/27
        value[x] += imageArray[xpos+1][ypos+2][x]*2/27
        value[x] += imageArray[xpos-2][ypos][x]*-3/27
        value[x] += imageArray[xpos+2][ypos][x]*3/27
        value[x] += imageArray[xpos-2][ypos-1][x]*-2/27
        value[x] += imageArray[xpos-2][ypos+1][x]*-2/27
        value[x] += imageArray[xpos+2][ypos-1][x]*2/27
        value[x] += imageArray[xpos+2][ypos+1][x]*2/27
        value[x] += imageArray[xpos-2][ypos-2][x]*-1/27
        value[x] += imageArray[xpos-2][ypos+2][x]*-1/27
        value[x] += imageArray[xpos+2][ypos-2][x]*1/27
        value[x] += imageArray[xpos+2][ypos+2][x]*1/27
    return value
def yKernel5(imageArray, xpos, ypos):
    value = [0,0,0]
    for x in range(3):
        value[x] += imageArray[xpos][ypos-1][x]*-6/27
        value[x] += imageArray[xpos][ypos+1][x]*6/27
        value[x] += imageArray[xpos-1][ypos-1][x]*-4/27
        value[x] += imageArray[xpos+1][ypos-1][x]*-4/27
        value[x] += imageArray[xpos-1][ypos+1][x]*4/27
        value[x] += imageArray[xpos+1][ypos+1][x]*4/27
        value[x] += imageArray[xpos-2][ypos-1][x]*-2/27
        value[x] += imageArray[xpos+2][ypos-1][x]*-2/27
        value[x] += imageArray[xpos-2][ypos+1][x]*2/27
        value[x] += imageArray[xpos+2][ypos+1][x]*2/27
        value[x] += imageArray[xpos][ypos-2][x]*-3/27
        value[x] += imageArray[xpos][ypos+2][x]*3/27
        value[x] += imageArray[xpos-1][ypos-2][x]*-2/27
        value[x] += imageArray[xpos+1][ypos-2][x]*-2/27
        value[x] += imageArray[xpos-1][ypos+2][x]*2/27
        value[x] += imageArray[xpos+1][ypos+2][x]*2/27
        value[x] += imageArray[xpos-2][ypos-2][x]*-1/27
        value[x] += imageArray[xpos+2][ypos-2][x]*-1/27
        value[x] += imageArray[xpos-2][ypos+2][x]*1/27
        value[x] += imageArray[xpos+2][ypos+2][x]*1/27
    return value
im = Image.open(openThis)
pix = im.load()
imageSize = im.size
imageData = np.array([[[0.00000 for z in range(3)] for x in range(imageSize[1])] for y in range(imageSize[0])])
for height in range(imageSize[1]):
    for length in range(imageSize[0]):
        imageData[length][height] = [abs(pix[length, height][0])/255,abs(pix[length, height][1])/255,abs(pix[length, height][2])/255]
if(kernelSize == 3):
    kernOut = [[[0.00000,0.00000,0.00000] for x in range(imageSize[1]-2)] for y in range(imageSize[0]-2)]
    for x in range(imageSize[0]-2):
        for y in range(imageSize[1]-2):
            kernOut[x][y] = xKernel3(imageData, x+1, y+1) + yKernel3(imageData, x+1, y+1)
elif(kernelSize == 5):
    kernOut = [[[0.00000,0.00000,0.00000] for x in range(imageSize[1]-4)] for y in range(imageSize[0]-4)]
    for x in range(imageSize[0]-4):
        for y in range(imageSize[1]-4):
            kernOut[x][y] = xKernel5(imageData, x+1, y+1) + yKernel5(imageData, x+1, y+1)
im2 = Image.new("RGB", [len(kernOut),len(kernOut[0])])
kernPros = im2.load()
for x in range(len(kernOut)):
    for y in range(len(kernOut[0])):
        R = 0
        G = 0
        B = 0
        if(kernOut[x][y][0] >= accuracy):
            R = int(kernOut[x][y][0]*255*amplify)
        if(kernOut[x][y][1] >= accuracy):
            G = int(kernOut[x][y][1]*255*amplify)
        if(kernOut[x][y][2] >= accuracy):
            B = int(kernOut[x][y][2]*255*amplify)
        kernPros[x, y] = tuple([R, G, B])
        
im2.save(filename+"out.png", "PNG")