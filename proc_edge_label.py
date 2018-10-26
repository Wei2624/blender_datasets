import os
import cv2
import numpy as np
import sys

step_size = 4

classes = ('__background__', 'table', 'book', 'laptop', 'kettle', 'pan') 
class_colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
im_width = 640
im_height = 480

def proc_edge(im):
	for i in xrange(0,im_height,step_size):
		for j in xrange(0,im_width,step_size):
			label_index = np.zeros((step_size, step_size))
			max_cls = -1
			max_votes = 0
			crop = im[i:i+step_size,j:j+step_size,:]
			index = im[i:i+step_size,j:j+step_size,2] + \
					256*im[i:i+step_size,j:j+step_size,1] + 256*256*im[i:i+step_size,j:j+step_size,0]
			print index.shape
			for k in xrange(len(class_colors)):
				color = class_colors[k]
				ind = color[0] + 256*color[1] + 256*256*color[2]
				I = np.where(index == ind)
				label_index[I[0], I[1]] = k+1
				if I[0].shape[0] > max_votes:
					max_votes = I[0].shape[0]
					max_cls = k
			I = np.where(label_index == 0)
			if I[0].shape[0] > 0:				
				if len(index.shape) == 2:index = np.expand_dims(index,axis=2)
				print I
				crop[I[0],I[1],0] = class_colors[max_cls][2]
				crop[I[0],I[1],1] = class_colors[max_cls][1]
				crop[I[0],I[1],2] = class_colors[max_cls][0]

				im[i:i+step_size,j:j+step_size,:] = crop
	return im




for i in range(0,1):
	print i
	rgbd_path = '/home/weizhang/Documents/ycb_blender/output/'  + '{:04d}/'.format(i)
	for j in xrange(0,1):
		filename = os.path.join(rgbd_path,'{:04d}_label.png'.format(j))
		im = cv2.imread(filename)

		im = proc_edge(im)

		cv2.imwrite(filename,im)


