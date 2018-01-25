#usr/bin/python
#coding = utf-8
#
from stl import mesh
import math
import numpy
import shoot
import pickle
import itertools


f2=file(shoot.SAVE_PATH,'rb')
a2=pickle.load(f2)
print '*'*100
print len(a2)
print '*'*100

data = numpy.zeros(len(a2), dtype=mesh.Mesh.dtype)

for i in range(len(a2)):
  data['vectors'][i]=numpy.array(a2[i])


meshs=mesh.Mesh(data.copy())

print meshs.vectors
print "shoot:"

from matplotlib import pyplot
from mpl_toolkits import mplot3d

# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Render the cube faces

axes.add_collection3d(mplot3d.art3d.Poly3DCollection(meshs.vectors))


scale = numpy.concatenate([meshs.points])
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
pyplot.show()