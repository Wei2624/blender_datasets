import sys
import bpy
import os
from mathutils import *
from math import *
import numpy as np
import random

scipy_path = '/home/weizhang/anaconda2/envs/blender/lib/python3.5/site-packages/'
sys.path.insert(0, scipy_path)
import scipy.io
from cfgs import test_config as cfg

random.seed(3)


def obj_selector(cate_name):
	for obj in bpy.data.objects:
		if cate_name in obj.name:obj.select = True
		else: obj.select = False

def obj_remover(*args):
	for obj in bpy.data.objects:
		for name in args:
			if name in obj.name:
				bpy.data.objects.remove(obj,True)
				break

def dim_setter_single(obj_name, dim):
	for obj in bpy.data.objects:
			if obj_name in obj.name:
				obj.dimensions = dim
				break

def obj_rotator(cate_name,angle):
	for obj in bpy.data.objects:
		if cate_name in obj.name:
			obj.rotation_euler = (obj.rotation_euler[0],obj.rotation_euler[1], obj.rotation_euler[2] + radians(angle))

def obj_locator(cate_name, tx,ty,tz):
	for obj in bpy.data.objects:
		if cate_name in obj.name:
			obj.location = (tx,ty,tz)
			# obj.location[0] += (tx - obj.location[0])
			# obj.location[1] += (ty - obj.location[1])
			# obj.location[2] += (tz - obj.location[2])
			# print(obj.location)

def obj_resizer(cate_name,scale_ratio):
	index = 0
	for obj in bpy.data.objects:
		if cate_name in obj.name:
			# obj.dimensions= (1,1,1) #obj.dimensions*1
			# obj.rotation_euler = (obj.rotation_euler[0],obj.rotation_euler[1], obj.rotation_euler[2] + radians(30))
			# obj.location[2] = 1.0 
			obj.scale *= scale_ratio
			# print(obj.dimensions)
			# print(obj.scale)
	# obj_selector(cate_name)
	# bpy.ops.transform.resize(value=target_size)


def lights_setup():
	num_of_lights_on = random.randint(1,cfg.num_of_lights)
	lights_idx = list(np.random.choice(cfg.num_of_lights,num_of_lights_on,replace=False))

	index = 0
	for obj in bpy.data.objects:
		if 'Lamp' in obj.name and index in lights_idx:
			if cfg.randomize_xyz:
				# random all three coordinates
			else:
				# only random z direction
				
			index +=1




