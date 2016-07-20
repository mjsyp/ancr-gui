'''
Created on Jul 18, 2016

@author: Alice
'''

import voxelGridTest as vox
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import time



fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")


voxelHandler = vox.voxelHandler()

cubePos = voxelHandler.custBox( -5, 5, -5, 5, -5, 5)
cubePos2 = voxelHandler.custBox(8, 20 , 2, -2, 2, -2)
#cubPos3 = voxelHandler.custBox()



for i in range(len(cubePos2)):
		cubePos.append(cubePos2[i])
curChunk = voxelHandler.createChunk(cubePos)

voxelHandler.createOutline(curChunk)


voxelHandler.drawCubeLines(curChunk)

scaling = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
ax.auto_scale_xyz(*[[np.min(scaling), np.max(scaling)]]*3)
plt.show()