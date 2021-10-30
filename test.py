import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *

# creating a dummy dataset
x = np.random.randint(low=100, high=500, size=(1000,))
y = np.random.randint(low=300, high=500, size=(1000,))
z = np.random.randint(low=200, high=500, size=(1000,))
'''
x = []
y = []
z = []
for i in range(180):
	for j in range(180):
		for k in range(3):
			x.append(i)
			y.append(j)
			z.append(k)
'''
colo = [x + y + z]

# creating figures
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# setting color bar
color_map = cm.ScalarMappable(cmap=cm.Greys)
color_map.set_array(colo)

# creating the heatmap
img = ax.scatter(x, y, z, marker='s',
                s=20, color='grey')
plt.colorbar(color_map)

# adding title and labels
ax.set_title("3D Heatmap")
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

# displaying plot
plt.show()
