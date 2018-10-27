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


def load_obj(cate_list,bg):
	number_obj = random.randint(1, len(cate_list))
	selected_obj_list = [cate_list[i] for i in list(np.random.choice(len(cate_list),number_obj))]
	for each in selected_obj_list:
		file_path = path_to_obj(each)
		if  'obj' in file_path:
			result = bpy.ops.import_scene.obj(filepath=file_path)
		else: 
			result = bpy.ops.wm.collada_import(filepath=file_path)

		for o in bpy.context.selected_objects:
			o.name = each
	# if bg: bg_loader()