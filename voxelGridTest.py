'''
Created on Jul 14, 2016

@author: Alice
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import time



#Stores all info about a cube
#maybe initialize to 0
class voxel():
	
	topFront = 1
	topBack = 1
	topLeft = 1
	topRight = 1
	botFront = 1
	botBack = 1
	botLeft = 1
	botRight = 1
	leftFront = 1
	leftBack = 1
	rightFront = 1
	rightBack = 1
	
	x = 0
	y = 0
	z = 0

	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z

class chunkData():
	n = 0
	xOff = 0
	yOff = 0
	zOff = 0
	voxGrid = []
	
	def __init__(self):
		self.n = 0
		self.xOff = 0
		self.yOff = 0
		self.zOff = 0
		self.voxGrid = []

class voxelHandler():
	
	def __init__(self):
		pass
	
	#Turns list of voxels into properly placed voxels in a chunk
	def createChunk(self,posList):
	
		newChunk = chunkData()
		
		for i in range(len(posList)):
			if i == 0:
				xMin = posList[i].x
				xMax = posList[i].x
				yMin = posList[i].y
				yMax = posList[i].y
				zMin = posList[i].z
				zMax = posList[i].z
				continue
			if posList[i].x > xMax:
				xMax = posList[i].x
			if posList[i].x < xMin:
				xMin = posList[i].x
			if posList[i].y > yMax:
				yMax = posList[i].y
			if posList[i].y < yMin:
				yMin = posList[i].y
			if posList[i].z > zMax:
				zMax = posList[i].z
			if posList[i].z < zMin:
				zMin = posList[i].z
	
		xRange = xMax - xMin + 1
		yRange = yMax - yMin + 1
		zRange = zMax - zMin + 1
	
		voxGrid = [[[0]* zRange for i in range(yRange)] for j in range(xRange)]
		for i in range(len(posList)):
			xLoc = posList[i].x - xMin
			yLoc = posList[i].y - yMin
			zLoc = posList[i].z - zMin
			voxGrid[xLoc][yLoc][zLoc] = voxel(posList[i].x,posList[i].y,posList[i].z)
	
		newChunk.n = len(posList)
		newChunk.xOff = xMin
		newChunk.yOff = yMin
		newChunk.voxGrid = voxGrid
	
		return newChunk

	def drawCubeLines(self,curCube):
	
		x = curCube.x
		y = curCube.y
		z = curCube.z
	
		#Top
		if curCube.topBack == 1:
			plt.plot((x , x + 1), (y + 1, y + 1),(z + 1,z + 1))
		if curCube.topFront == 1:
			plt.plot((x , x + 1), (y , y ),(z + 1,z + 1))
		if curCube.topLeft == 1:
			plt.plot((x , x ), (y , y + 1),(z + 1,z + 1))
		if curCube.topRight == 1:
			plt.plot((x + 1, x + 1), (y , y + 1),(z + 1,z + 1))
		#Bottom
		if curCube.botBack == 1:
			plt.plot((x , x + 1), (y + 1, y + 1),(z ,z ))
		if curCube.botFront == 1:
			plt.plot((x , x + 1), (y , y ),(z ,z ))
		if curCube.botLeft == 1:
			plt.plot((x , x ), (y , y + 1),(z ,z ))
		if curCube.botRight == 1:
			plt.plot((x + 1, x + 1), (y , y + 1),(z ,z ))
		#Vertical
		if curCube.leftFront == 1:
			plt.plot((x , x ), (y , y ),(z ,z + 1))
		if curCube.leftBack == 1:
			plt.plot((x , x ), (y + 1, y + 1),(z ,z + 1))
		if curCube.rightFront == 1:
			plt.plot((x + 1, x + 1), (y , y ),(z ,z + 1))
		if curCube.rightBack == 1:
			plt.plot((x + 1, x + 1), (y + 1, y + 1),(z ,z + 1))

	def cubeAdjChk(self,pos,chunk):
		i = pos[0]
		j = pos[1]
		k = pos[2]
	
		if i < 0 or j < 0 or k < 0 or i >= len(chunk) or j >= len(chunk[0]) or k >= len(chunk[0][0]):
			return False
		elif chunk[i][j][k] != 0:
			return True
		else:
			return False

	#determines what sides of cubes to show
	def createOutline(self,chunk):	
		for i in range(len(chunk)):
			for j in range(len(chunk[i])):
				for k in range(len(chunk[i][j])):
				
					if chunk[i][j][k] == 0:
						continue
		
					#topFront
					if (self.cubeAdjChk([i,j - 1,k],chunk)) ^ (self.cubeAdjChk([i,j,k + 1],chunk))^ (self.cubeAdjChk([i,j - 1,k + 1],chunk)):
						chunk[i][j][k].topFront = 0
					#topBack
					if (self.cubeAdjChk([i,j + 1,k],chunk)) ^ (self.cubeAdjChk([i,j,k + 1],chunk))^ (self.cubeAdjChk([i,j + 1,k + 1],chunk)):
						chunk[i][j][k].topBack = 0
					#topLeft
					if (self.cubeAdjChk([i - 1,j,k],chunk)) ^ (self.cubeAdjChk([i,j,k + 1],chunk))^ (self.cubeAdjChk([i - 1,j,k + 1],chunk)):
						chunk[i][j][k].topLeft = 0
					#topRight
					if (self.cubeAdjChk([i + 1,j,k],chunk)) ^ (self.cubeAdjChk([i,j,k + 1],chunk))^ (self.cubeAdjChk([i + 1,j,k + 1],chunk)):
						chunk[i][j][k].topRight = 0

					#botFront
					if (self.cubeAdjChk([i,j - 1,k],chunk)) ^ (self.cubeAdjChk([i,j,k - 1],chunk))^ (self.cubeAdjChk([i,j - 1,k - 1],chunk)):
						chunk[i][j][k].botFront = 0
					#botBack
					if (self.cubeAdjChk([i,j + 1,k],chunk)) ^ (self.cubeAdjChk([i,j,k - 1],chunk))^ (self.cubeAdjChk([i,j + 1,k - 1],chunk)):
						chunk[i][j][k].botBack = 0
					#botLeft
					if (self.cubeAdjChk([i - 1,j,k],chunk)) ^ (self.cubeAdjChk([i,j,k - 1],chunk))^ (self.cubeAdjChk([i - 1,j,k - 1],chunk)):
						chunk[i][j][k].botLeft = 0
					#botRight
					if (self.cubeAdjChk([i + 1,j,k],chunk)) ^ (self.cubeAdjChk([i,j,k - 1],chunk))^ (self.cubeAdjChk([i + 1,j,k - 1],chunk)):
						chunk[i][j][k].botRight = 0
					
					#leftFront
					if (self.cubeAdjChk([i,j - 1,k],chunk)) ^ (self.cubeAdjChk([i - 1,j,k],chunk))^ (self.cubeAdjChk([i - 1,j - 1,k],chunk)):
						chunk[i][j][k].leftFront = 0
					#leftBack
					if (self.cubeAdjChk([i,j + 1,k],chunk)) ^ (self.cubeAdjChk([i - 1,j,k],chunk))^ (self.cubeAdjChk([i - 1,j + 1,k],chunk)):
						chunk[i][j][k].leftBack = 0
					#rightFront
					if (self.cubeAdjChk([i,j - 1,k],chunk)) ^ (self.cubeAdjChk([i + 1,j,k],chunk))^ (self.cubeAdjChk([i + 1,j - 1,k],chunk)):
						chunk[i][j][k].rightFront = 0
					#rightBack
					if (self.cubeAdjChk([i,j + 1,k],chunk)) ^ (self.cubeAdjChk([i + 1,j,k],chunk))^ (self.cubeAdjChk([i + 1,j + 1,k],chunk)):
						chunk[i][j][k].rightBack = 0


	def custBox(self,x1,x2,y1,y2,z1,z2):
		
		posList = []
		
		xRange = abs(x2-x1)
		yRange = abs(y2-y1)
		zRange = abs(z2-z1)
		if x1 < x2:
			xOff = x1
		else:
			xOff = x2
		if y1 < y2:
			yOff = y1
		else:
			yOff = y2
		if z1 < z2:
			zOff = z1
		else:
			zOff = z2
		
		
		for i in range(xRange):
			for j in range(yRange):
				for k in range(zRange):
					
					posList.append(voxel(i + xOff,j + yOff,k + zOff))
		
		return posList




