import matplotlib
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from itertools import product, combinations
import networkx as nx

def viewComponentGeo(G):
	plt.close()
		
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	xs = []
	ys = []
	zs = []

	for node in G.nodes():
		if 'Type' in G.node[node]:
			if G.node[node]['Type'] == 'Component':
				xs.append(G.node[node]['x'])
				ys.append(G.node[node]['y'])
				zs.append(G.node[node]['z'])

	ax.scatter(xs, ys, zs, c='r', marker='o')
	ax.set_xlabel('X Label')
	ax.set_ylabel('Y Label')
	ax.set_zlabel('Z Label')

	plt.show()

def viewCompartmentGeo(G):
	plt.close()

	fig = plt.figure()
	ax = fig.gca(projection='3d')
	ax.set_aspect("equal")

	for node in G.nodes():
		if 'Type' in G.node[node]:
			if G.node[node]['Type'] == 'Compartment':
				a = G.node[node]['EdgeLength']
				x = G.node[node]['x']
				y = G.node[node]['y']
				z = G.node[node]['z']
				hSL = float(a/2)
				r = [-hSL, hSL]
				rX = [-hSL + x, hSL + x]
				rY = [-hSL + y, hSL + y]
				rZ = [-hSL + z, hSL + z]
				for s, e in combinations(np.array(list(product(rX,rY,rZ))), 2):
					if not np.sum(np.abs(s-e)) > a+0.0000001:
						ax.plot3D(*zip(s,e), color="b")

	scaling = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
	ax.auto_scale_xyz(*[[np.min(scaling), np.max(scaling)]]*3)
	plt.show()