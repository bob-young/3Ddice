from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import shoot

figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Load the STL files and add the vectors to the plot
your_mesh = mesh.Mesh.from_file('C:\\Users\\bob\\Desktop\\code\\python\\lz.stl')

print shoot.dice(your_mesh)
print "generate new model and store it\nits size:"

op = input("0:show the old model\n1:show the saved file's path\n2:show the new model:")

if(op==0):
	axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
	scale = your_mesh.points.flatten(-1)
	axes.auto_scale_xyz(scale, scale, scale)
	pyplot.show()
elif(op==1):
	print shoot.SAVE_PATH
elif(op==2):
	pass