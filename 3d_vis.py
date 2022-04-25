# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 14:06:45 2022

@author: jacob
"""


import vtk.util.numpy_support as numpy_support
import numpy as np
from vedo import Volume, show
import k3d

MIN_PHALL_THRESHOLD = 4
MIN_DAPI_THRESHOLD = 15
XY_SCALE = 0.176 # um/pixel
Z_SCALE = 2.5 # um/pixel

phall = spio.loadmat('phall.mat')['PHALLOIDIN_IMG']
dapi = spio.loadmat('dapi.mat')['DAPI_IMG']

# Use this to flush out small values below a threshold:
# (could alternatively use Otsu's method, etc.)
phall[phall <= MIN_PHALL_THRESHOLD] = 0
dapi[dapi <= MIN_DAPI_THRESHOLD] = 0

# File in 3D data from matlab:
X, Y, Z = np.mgrid[:512, :512, :10]
phall_field = phall[X,Y,Z]
dapi_field = dapi[X,Y,Z]

# Create the volumes
phall_vol = Volume(phall_field, mapper = 'smart', spacing = (Z_SCALE, XY_SCALE, XY_SCALE))
dapi_vol = Volume(dapi_field, mapper = 'smart', spacing = (Z_SCALE, XY_SCALE, XY_SCALE))
phall_vol.color('red')
dapi_vol.color('blue')

plot = k3d.plot()

# Use some colormaps
cmap1 = k3d.colormaps.matplotlib_color_maps.winter
cmap2 = k3d.colormaps.matplotlib_color_maps.autumn

# Plot both datasets, with labels
for vol,col,name,alpha in zip([vol1, vol2], [cmap1, cmap2], ['Phalloidin - Cytoskeleton','DAPI - Nuclei'], [30,5]):
    kx, ky, kz = vol.dimensions()
    arr = vol.getPointArray()
    kimage = arr.reshape(-1, ky, kx).astype(np.float32)

    kvol = k3d.volume(kimage, alpha_coef=alpha, bounds=vol.bounds(), name=name, color_map = col)
    plot += kvol

# Saving the html file for later viewing or sharing
with open('page.html','w') as fp:
    fp.write(plot.get_snapshot())
