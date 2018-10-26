import os
import cv2
import numpy as np
import sys
import scipy.io


for i in range(100,110):
	print i
	rgbd_path = '/home/weizhang/Documents/ycb_blender/output/'  + '{:04d}/'.format(i)
	for j in xrange(0,100):
		filename_meta = os.path.join(rgbd_path,'{:04d}_meta.mat'.format(j))

		meta = scipy.io.loadmat(filename_meta)

		meta['factor_depth'] = np.array([[15000]])

		scipy.io.savemat(filename_meta,meta)

