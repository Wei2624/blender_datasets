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
from cfgs import test_config


def path_to_obj(obj_name):
	current_file_path = os.path.dirname(os.path.realpath(__file__))
	models_path = os.path.join(current_file_path,'../3DModels/{:s}/'.format(obj_name))

	sub_folders = os.listdir(models_path)
	idx = random.randint(0,len(sub_folders)-1)

	return os.path.join(models_path,sub_folders[idx])+'/model.obj' if \
			os.path.isfile(os.path.join(models_path,sub_folders[idx])+'/model.obj') else \
			os.path.join(models_path,sub_folders[idx])+'/model.dae'

def path_to_tex(tex_type):
	current_file_path = os.path.dirname(os.path.realpath(__file__))
	models_path = os.path.join(current_file_path,'../3DModels/{:s}/'.format(tex_type))

	sub_folders = os.listdir(models_path)
	idx = random.randint(0,len(sub_folders)-1)

	return os.path.join(models_path,sub_folders[idx]) 

def obj_importer(path,name):
	if  'obj' in path:
		result = bpy.ops.import_scene.obj(filepath=path)
	else: 
		result = bpy.ops.wm.collada_import(filepath=path)

	for o in bpy.context.selected_objects:
		o.name = name

def tex_importer(path,obj_name):
	img = bpy.data.images.load(path, check_existing=False)
	tex = bpy.data.textures.new(name=obj_name,type='IMAGE')
	tex.image = img
	bpy.data.objects[obj_name].active_material.active_texture = tex



def load_objs(cate_list,load_bg,load_table, plane_set):
	if load_table:
		file_path = path_to_obj('table')  # change here to load particular table for testing
		obj_importer(file_path,'table')

	# number_obj = random.randint(1, len(cate_list))  # might want to set up upper bound for table-top setup
	# selected_obj_list = [cate_list[i] for i in list(np.random.choice(len(cate_list),number_obj))]
	# for each in selected_obj_list:
	# 	file_path = path_to_obj(each)
	# 	obj_importer(file_path,each)
		
	if load_bg: 
		file_path = path_to_obj('background')
		obj_importer(file_path,'background')

	if plane_set:
		for obj in bpy.data.objects:
			if 'Plane' in obj.name:
				if obj.name == 'Plane':
					file_path = path_to_tex('floor_tex')
				else:
					file_path = path_to_tex('wall_tex')
				tex_importer(file_path,obj.name)
