from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
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
	
	sL = 1
	
	def __init__(self,dim):
		self.sL = dim
	
	#Turns list of voxels into properly placed voxels in a chunk
	def createChunk(self,posList):
		
		mpr = 1.0/self.sL
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
	
		voxGrid = [[[0]* (int(zRange*mpr)) for i in range(int(yRange*mpr))] for j in range(int(xRange*mpr))]
		for i in range(len(posList)):
			xLoc = posList[i].x - xMin
			yLoc = posList[i].y - yMin
			zLoc = posList[i].z - zMin
			voxGrid[int(xLoc*mpr)][int(yLoc*mpr)][int(zLoc*mpr)] = voxel(posList[i].x,posList[i].y,posList[i].z)
	
		newChunk.n = len(posList)
		newChunk.xOff = xMin
		newChunk.yOff = yMin
		newChunk.voxGrid = voxGrid
		#print("createChunk")
		#print(len(voxGrid))
		#print(len(voxGrid[0]))
		#print(len(voxGrid[0][0]))
		
		return newChunk

	def drawCubeLines(self,curChunk,ax):
		
		sL = self.sL
		chunkList = curChunk.voxGrid
		#print("drawCubeLines")
		#print(len(chunkList))
		#print(len(chunkList[0]))
		#print(len(chunkList[0][0]))
		for i in range(len(chunkList)):
			for j in range(len(chunkList[i])):
				for k in range(len(chunkList[i][j])):
			
					
					
					if chunkList[i][j][k] != 0:
						
						curCube = chunkList[i][j][k]
						
						x = curCube.x
						y = curCube.y
						z = curCube.z
	
						#Top
						if curCube.topBack == 1:
							ax.plot((x , x + sL), (y + sL, y + sL),(z + sL,z + sL),'b-')
						if curCube.topFront == 1:
							ax.plot((x , x + sL), (y , y ),(z + sL,z + sL),'b-')
						if curCube.topLeft == 1:
							ax.plot((x , x ), (y , y + sL),(z + sL,z + sL),'b-')
						if curCube.topRight == 1:
							ax.plot((x + sL, x + sL), (y , y + sL),(z + sL,z + sL),'b-')
						#Bottom
						if curCube.botBack == 1:
							ax.plot((x , x + sL), (y + sL, y + sL),(z ,z ),'b-')
						if curCube.botFront == 1:
							ax.plot((x , x + sL), (y , y ),(z ,z ),'b-')
						if curCube.botLeft == 1:
							ax.plot((x , x ), (y , y + sL),(z ,z ),'b-')
						if curCube.botRight == 1:
							ax.plot((x + sL, x + sL), (y , y + sL),(z ,z ),'b-')
						#Vertical
						if curCube.leftFront == 1:
							ax.plot((x , x ), (y , y ),(z ,z + sL),'b-')
						if curCube.leftBack == 1:
							ax.plot((x , x ), (y + sL, y + sL),(z ,z + sL),'b-')
						if curCube.rightFront == 1:
							ax.plot((x + sL, x + sL), (y , y ),(z ,z + sL),'b-')
						if curCube.rightBack == 1:
							ax.plot((x + sL, x + sL), (y + sL, y + sL),(z ,z + sL),'b-')

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
	def createOutline(self,chunkObj):
		
		chunk = chunkObj.voxGrid
		#print("createOutline")
		#print(len(chunk))
		#print(len(chunk[0]))
		#print(len(chunk[0][0]))
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

#Each dimension has to be twice as long to allow for half value edge lengths
	def custBox(self,x1,x2,y1,y2,z1,z2):
		
		sL = self.sL
		mpr = 1.0/sL
		
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
		
		
		for i in range(int(xRange*mpr)):
			for j in range(int(yRange*mpr)):
				for k in range(int(zRange*mpr)):
					
					posList.append(voxel(i/mpr + xOff,j/mpr + yOff,k/mpr + zOff))
		
		return posList


	def listAppend(self,cubePosList):
		
		cubeListFinal = []		
		for i in range(len(cubePosList)):
			for j in range(len(cubePosList[i])):
				cubeListFinal.append(cubePosList[i][j])
				
		return cubeListFinal

