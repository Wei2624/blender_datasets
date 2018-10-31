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
from lib import obj_loader

random.seed(3)


def obj_selector(cate_name):
	for obj in bpy.data.objects:
		if cate_name in obj.name:obj.select = True
		else: obj.select = False

def obj_remover(obj_list):
	for obj in bpy.data.objects:
		for name in obj_list:
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
		if 'Lamp' in obj.name:
			if index in lights_idx:
				obj.hide_render = False
				if cfg.randomize_xyz:
					# random all three coordinates
					plane_scaler = random.randint(0,cfg.plane_scale)
					abs_dist = plane_scale*cfg.range_unit
					if cfg.lamp_xy[index][0] != 0 and cfg.lamp_xy[index][1] != 0:
						obj.location[0] = cfg.lamp_xy[index][0] + np.sign(cfg.lamp_xy[index][0])*abs_dist
						obj.location[1] = cfg.lamp_xy[index][1] + np.sign(cfg.lamp_xy[index][1])*abs_dist*abs(cfg.lamp_xy[index][1]/cfg.lamp_xy[index][0])
					else:
						if cfg.lamp_xy[index][0] == 0: 
							obj.location[1] = cfg.lamp_xy[index][1] + np.sign(cfg.lamp_xy[index][1])*abs_dist
						if cfg.lamp_xy[index][1] == 0: 
							obj.location[0] = cfg.lamp_xy[index][0] + np.sign(cfg.lamp_xy[index][0])*abs_dist
				scale = random.randint(0,int((cfg.light_z_range[1] - cfg.light_z_range[0])/cfg.range_unit))
				obj.location[2] = cfg.light_z_range[0] + scale*cfg.range_unit
			else:
				obj.hide_render = True
			index +=1

def plane_setup():
	for obj in bpy.data.objects:
		if 'Plane' in obj.name:
			if obj.name == 'Plane':
				file_path = obj_loader.path_to_tex('floor_tex')
			else:
				file_path = obj_loader.path_to_tex('wall_tex')
			obj_loader.tex_importer(file_path,obj.name)




