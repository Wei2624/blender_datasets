import os
import cv2
import numpy as np
import sys

import matplotlib.pyplot as plt

for i in range(0,100):
	print i
	rgbd_path = '/home/weizhang/Documents/blender_datasets/output/dataset1/'  + '{:04d}/'.format(i)
	for j in xrange(0,100):
		filename_depth = os.path.join(rgbd_path,'{:04d}_depth.png'.format(j))
		# os.rename(old_filename,new_filename)
		im = cv2.imread(filename_depth)

		# filename = os.path.join(rgbd_path,'{:04d}_label_plane.png'.format(j))

		# im_label = cv2.imread(filename)


		# index = im_label[:,:,2] + 256*im_label[:,:,1] + 256*256*im_label[:,:,0]

		# ind = 0 + 256*0 + 256*256*0

		# I = np.where(index == ind)

		# im[I[0],I[1],0] = 0
		# im[I[0],I[1],1] = 0
		# im[I[0],I[1],2] = 0


		im = cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
		im = im.astype(np.uint16)
		im = im/255.0*65535.0
		im = im.astype(np.uint16)
		cv2.imwrite(filename_depth,im)
