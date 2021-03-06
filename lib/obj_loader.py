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
from lib import util

random.seed(3)


def path_to_obj(obj_name):
	current_file_path = os.path.dirname(os.path.realpath(__file__))
	models_path = os.path.join(current_file_path,'../3DModels/{:s}/'.format(obj_name))

	sub_folders = os.listdir(models_path)
	idx = np.random.randint(0,len(sub_folders))

	idx_t = int(sub_folders[idx].split(obj_name)[1]) -1

	return os.path.join(models_path,sub_folders[idx])+'/model.obj' if \
			os.path.isfile(os.path.join(models_path,sub_folders[idx])+'/model.obj') else \
			os.path.join(models_path,sub_folders[idx])+'/model.dae', idx_t

def path_to_tex(tex_type):
	current_file_path = os.path.dirname(os.path.realpath(__file__))
	models_path = os.path.join(current_file_path,'../3DModels/{:s}/'.format(tex_type))

	sub_folders = os.listdir(models_path)
	idx = np.random.randint(0,len(sub_folders))

	return os.path.join(models_path,sub_folders[idx]) 

def coord_gen_obj():
	coords = []
	for i in range(cfg.area_div):
		th = np.random.randint(0,int(cfg.h_bound/cfg.h_div_unit)+1)
		tv = np.random.randint(0,int(cfg.v_bound/cfg.v_div_unit)+1)
		# print(th,tv)
		h = cfg.h_div_unit*th
		v = cfg.v_div_unit*tv
		if i == 0: coords.append((h,v))
		if i == 1: coords.append((-h,v))
		if i == 2: coords.append((-h,-v))
		if i == 3: coords.append((h,-v))
	return coords


def obj_importer(path,name,idx,coord=None):
	if  'obj' in path:
		result = bpy.ops.import_scene.obj(filepath=path)
	else: 
		result = bpy.ops.wm.collada_import(filepath=path)

	index = 0
	for obj in bpy.context.selected_objects:
		obj.name = name+str(idx)+'_{:d}'.format(index)
		for i in range(len(obj.material_slots)):
			obj.active_material_index = i
			obj.active_material.use_transparency = False
			obj.active_material.alpha = cfg.obj_alpha
		index +=1
		# if coord != None:
		# 	obj.location = (coord[0],coord[1],cfg.table_height)
			# print(obj.location)

def background_pos_gen():
	scale = np.random.randint(0,int((cfg.background_range[1] - cfg.background_range[0])/cfg.range_unit)+1)
	x = cfg.background_range[0] + scale*cfg.range_unit
	scale = np.random.randint(0,int((cfg.background_range[1] - cfg.background_range[0])/cfg.range_unit)+1)
	y = cfg.background_range[0] + scale*cfg.range_unit

	return x,y


def tex_importer(path,obj_name, idx=0):
	img = bpy.data.images.load(path, check_existing=False)
	tex = bpy.data.textures.new(name=obj_name,type='IMAGE')
	tex.image = img
	print(tex)
	print(obj_name)
	bpy.data.objects[obj_name].active_material_index = idx
	bpy.data.objects[obj_name].active_material.active_texture = tex

def load_setup_objs(load_obj,load_bg,load_table, plane_set, off_table_obj):
	selected_obj_list = []
	offtable_obj_list = []
	if load_table:
		file_path, idx = path_to_obj('table')  # change here to load particular table for testing
		# file_path = '/home/weizhang/Documents/blender_datasets/3DModels/cerealbox/cerealbox2/model.obj'
		print('-----------------------table-------------------------')
		print(file_path,idx)
		obj_importer(path=file_path,name='table', idx=idx)
		util.dim_setter_single('table',cfg.table_dim)

	if load_obj:
		global number_obj
		number_obj = np.random.randint(1, cfg.table_top_num_obj+1)  # might want to set up upper bound for table-top setup
		# number_obj = 1
		# num_obj = num_obj_i
		selected_obj_list = [cfg.dynamic_classes[i] for i in list(np.random.choice(len(cfg.dynamic_classes),number_obj,replace=False))]
		coord_idx = list(np.random.choice(cfg.table_top_num_obj,number_obj,replace=False))
		coords = coord_gen_obj()
		for key, each in enumerate(selected_obj_list):
			file_path, idx = path_to_obj(each)
			print('-----------------------Object-------------------------')
			print(file_path,idx)
			# file_path = '/home/weizhang/Documents/blender_datasets/3DModels/mug/mug11/model.obj'
			# print(file_path,idx)
			# idx = 10
			obj_importer(path=file_path,name=each, idx=idx)
			util.obj_locator(each,coords[coord_idx[key]][0],coords[coord_idx[key]][1],cfg.table_height)


	if off_table_obj:
		off_table_obj_idx = np.random.randint(0,len(cfg.off_table_classes))
		file_path,idx = path_to_obj(cfg.off_table_classes[off_table_obj_idx])
		offtable_obj_list.append(cfg.off_table_classes[off_table_obj_idx])
		print('-----------------------Off Table-------------------------')
		print(file_path, idx)
		# selected_obj_list.append(cfg.off_table_classes[off_table_obj_idx])
		obj_importer(path=file_path,name=cfg.off_table_classes[off_table_obj_idx], idx=idx)
		x,y = background_pos_gen()

		util.obj_locator(cfg.off_table_classes[off_table_obj_idx],x,y,0)

		
	if load_bg: 
		file_path,idx = path_to_obj('background')
		obj_importer(path=file_path,name='background', idx=idx)
		x,y = background_pos_gen()
		util.obj_locator('background',x,y,0)

	if plane_set:
		util.plane_setup()

	return selected_obj_list, offtable_obj_list