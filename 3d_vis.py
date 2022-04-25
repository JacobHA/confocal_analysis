# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 14:06:45 2022

@author: jacob
"""


import scipy.io as spio
import vtk

phall = spio.loadmat('phall.mat')['PHALLOIDIN_IMG']

import vtk.util.numpy_support as numpy_support

# def numpyToVTK(data):
#     data_type = vtk.VTK_FLOAT
#     shape = data.shape

#     flat_data_array = data.flatten()
#     vtk_data = numpy_support.numpy_to_vtk(num_array=flat_data_array, deep=True, array_type=data_type)
    
#     img = vtk.vtkImageData()
#     img.GetPointData().SetScalars(vtk_data)
#     img.SetDimensions(shape[0], shape[1], shape[2])
#     return img

# from voxelfuse.voxel_model import VoxelModel
# from voxelfuse.mesh import Mesh

# list(np.array(phall, dtype=bool))

# mayavi.mlab.contour3d()

#%%

"""Create a Volume from a numpy array"""
import numpy as np

# data_matrix = np.zeros([75, 75, 75], dtype=np.uint8)
# # all voxels have value zero except:
# data_matrix[0:35,   0:35,  0:35] = 1
# data_matrix[35:55, 35:55, 35:55] = 2
# data_matrix[55:74, 55:74, 55:74] = 3

from vedo import Volume, show

#vol = Volume(data_matrix, c=['white','b','g','r'])
#vol.addScalarBar3D()

#show(vol, __doc__, axes=1).close()

#%%

"""Create a Volume from a numpy.mgrid"""
import numpy as np
from vedo import Volume, Text2D, show


import scipy.io as spio
import vtk

phall = spio.loadmat('phall.mat')['PHALLOIDIN_IMG']
dapi = spio.loadmat('dapi.mat')['DAPI_IMG']

phall[phall <= 4] = 0
# phall_max = np.where(phall <= 20)[0].max()
# phall[phall >= 20] = phall_max

dapi[dapi <= 15] = 0
# dapi_max = np.where(phall <= 200)[0].max()
# dapi[dapi >= 200] = dapi_max


import vtk.util.numpy_support as numpy_support


# Stretch out z axis:

X, Y, Z = np.mgrid[:512, :512, :10]
# Distance from the center at (15, 15, 15)
# scalar_field = ((X-15)**2 + (Y-15)**2 + (Z-15)**2) /225
scalar_field1 = phall[X,Y,Z]
scalar_field2 = dapi[X,Y,Z]

vol1 = Volume(scalar_field1, mapper='smart',spacing=(2.5,0.176,0.176))#, mapper='smart')#,mode=1)
vol2 = Volume(scalar_field2, mapper='smart',spacing=(2.5,0.176,0.176))#, mapper='smart')#,mode=1)

vol1.color('red')
vol2.color('blue')
#vol.addScalarBar3D()


# lego = vol.legosurface(vmin=1, vmax=2)
# lego.cmap('hot_r', vmin=1, vmax=2).addScalarBar3D()

# text1 = Text2D(__doc__, c='blue')
# text2 = Text2D('..and its lego isosurface representation\nvmin=1, vmax=2', c='dr')

# show(vol1, vol2, azimuth=10, interactive=0, offscreen=1)#, interactive=True)
# show([(vol,text1), (lego,text2)], N=2, azimuth=10).close()

# from vedo import exportWindow   

# exportWindow('panther.html')

# %%
import k3d
import numpy as np
# from vtkplotter import load, datadir
plot = k3d.plot()

cmap1 = k3d.colormaps.matplotlib_color_maps.winter
cmap2 = k3d.colormaps.matplotlib_color_maps.autumn

for vol,col,name,alpha in zip([vol1, vol2], [cmap1, cmap2], ['Phalloidin - Cytoskeleton','DAPI - Nuclei'], [30,5]):
    kx, ky, kz = vol.dimensions()
    arr = vol.getPointArray()
    kimage = arr.reshape(-1, ky, kx).astype(np.float32)

    kvol = k3d.volume(kimage, alpha_coef=alpha, bounds=vol.bounds(), name=name, color_map = col)
    plot += kvol

with open('page.html','w') as fp:
    fp.write(plot.get_snapshot())