# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 01:39:07 2019

@author: umesh
"""

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

x = [0.26,0.36,0.49,0.5,0.55,0.58,0.59,0.61,0.62,0.65,0.72,0.74,0.77,0.94,0.95,1.02,1.06,1.27,1.31]
y = [17,52,74,29,128,15,50,78,71,119,63,99,98,149,141,92,156,102,163]
z = [2,109,26,6,136,0,7,41,17,35,10,31,50,78,46,20,67,31,93]


dataset = pd.read_csv('A:\\CC\\Final\\only_not_falls.csv')

data = dataset.iloc[:, 0:3].values

print(data.shape)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_trisurf(data[0], data[1], data[2], cmap=cm.jet, linewidth=0.2)
plt.show()