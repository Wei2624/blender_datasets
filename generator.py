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
from lib import util
from lib import scene_gen
from lib import animation_setup

import importlib
importlib.reload(cfg)
importlib.reload(obj_loader)
importlib.reload(util)
importlib.reload(scene_gen)
importlib.reload(animation_setup)

random.seed(3)


# util.obj_selector('keyboard')
# setup_scene.scene_setup(load_obj=1, load_bg=0, load_table=1, plane_set=0)
# util.obj_remover(cfg.dynamic_classes)
# util.obj_locator('table',0.5,0.5,1)
# util.obj_resizer('keyboard',(1,1,1))
# util.lights_setup()
# animation_setup.setup_keyframes()

util.obj_remover(cfg.static_classes)
util.obj_remover(cfg.dynamic_classes)
util.obj_remover(cfg.off_table_classes)


start = 61
end = 62


# def export_pcd(filepath):
# 	obj = bpy.context.active_object
# 	print(obj)
# 	# apply object transformation and modifiers
# 	mesh = obj.to_mesh(bpy.context.scene, True, "PREVIEW")
# 	objmat = obj.matrix_world
# 	points = np.zeros((len(mesh.vertices),3))
# 	print(len(mesh.vertices))
# 	for k, vert in enumerate(mesh.vertices):
# 		co = objmat * vert.co

# 		points[k,0] = co.x
# 		points[k,1] = co.y
# 		points[k,2] = co.z

# 	np.save(filepath,points)

selected_obj_list = []
offtable_obj_list = []
num_obj_i = 1
for i in range(start,end):
	print(i)
	base_path = '/home/weizhang/Documents/blender_datasets/output/dataset1/'  + '{:04d}/'.format(i)
	label_tmp_path = '/home/weizhang/Documents/blender_datasets/output/dataset1/'  + '{:04d}_label/'.format(i)
	if not os.path.exists(base_path):
		os.makedirs(base_path)
	if not os.path.exists(label_tmp_path):
		os.makedirs(label_tmp_path)


	# test_path = os.path.join(base_path,'test.npy')
	# export_pcd(test_path)


	if (i-start)%cfg.change_scene_interval == 0:
		# animation_setup.setup_keyframes()

		# if num_obj_i > 4: num_obj_i = 1
		util.obj_remover(cfg.static_classes)
		util.obj_remover(cfg.dynamic_classes)
		util.obj_remover(cfg.off_table_classes)

		selected_obj_list, offtable_obj_list = scene_gen.scene_setup(load_obj=1, load_bg=0, load_table=1, plane_set=1,\
													off_table_obj=0)
		# num_obj_i += 1

		# print(selected_obj_list)

		util.lights_setup()

		scene_gen.batch_generator(base_path,label_tmp_path, 0)

	elif (i-start)%cfg.change_scene_interval == 1:
		scene_gen.shuffle_scene(selected_obj_list, shuffle_tex=1, shuffle_color=0, \
								shuffle_pos=0, shuffle_rot=1, shuffle_size=0, shuffle_bg=0, table_tex=1,\
								shuffle_offtable=0, off_table_list=offtable_obj_list)
		util.lights_setup()
		util.plane_setup()
		scene_gen.batch_generator(base_path,label_tmp_path, 0)
	elif (i-start)%cfg.change_scene_interval == 2:
		scene_gen.shuffle_scene(selected_obj_list, shuffle_tex=1, shuffle_color=0, \
								shuffle_pos=1, shuffle_rot=1, shuffle_size=1, shuffle_bg=0, table_tex=1,\
								shuffle_offtable=0, off_table_list=offtable_obj_list)
		util.lights_setup()
		util.plane_setup()
		scene_gen.batch_generator(base_path,label_tmp_path, 0)
	elif (i-start)%cfg.change_scene_interval == 3:
		scene_gen.shuffle_scene(selected_obj_list, shuffle_tex=1, shuffle_color=1, \
								shuffle_pos=1, shuffle_rot=1, shuffle_size=1, shuffle_bg=0, table_tex=1,\
								shuffle_offtable=0, off_table_list=offtable_obj_list)
		util.lights_setup()
		util.plane_setup()
		scene_gen.batch_generator(base_path,label_tmp_path, 0)

	os.rmdir(label_tmp_path)


