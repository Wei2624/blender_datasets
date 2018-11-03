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

random.seed(3)

no_need_copy = ['Camera','Lamp','Lamp.001','Lamp.002','Lamp.003','skp_camera_Last_Saved_SketchUp_View','background'\
				,'Plane','Plane.001','Plane.002','Plane.003','Plane.004']


def scene_setup(load_obj,load_bg,load_table, plane_set,num_obj_i):
	return obj_loader.load_setup_objs(load_obj=load_obj, load_bg=load_bg, load_table=load_table, plane_set=plane_set,num_obj_i=num_obj_i)


def shuffle_scene(cate_list, shuffle_tex, shuffle_color, shuffle_pos, shuffle_rot, shuffle_size, shuffle_bg, table_tex):
	if table_tex:
		for obj in bpy.data.objects:
			if 'table' in obj.name:
				dict_key = obj.name.split('.')[0]
				print(obj.name)
				if dict_key in cfg.tex_idx_dict:
					tex_path = obj_loader.path_to_tex('table_tex')		
					for i in cfg.tex_idx_dict[dict_key]:
						obj_loader.tex_importer(path=tex_path,obj_name=dict_key,idx=i)
				if shuffle_color:
					for i in range(len(obj.material_slots)):
						obj.active_material_index = i
						r = max(0, min(1.0, obj.active_material.diffuse_color[0] + np.random.normal(cfg.normal_m, cfg.normal_s, 1)))
						g = max(0, min(1.0, obj.active_material.diffuse_color[1] + np.random.normal(cfg.normal_m, cfg.normal_s, 1)))
						b = max(0, min(1.0, obj.active_material.diffuse_color[2] + np.random.normal(cfg.normal_m, cfg.normal_s, 1)))
						obj.active_material.diffuse_color = (r,g,b)
	for key, cate in enumerate(cate_list):
		for obj in bpy.data.objects:
			if cate in obj.name:
				print('------------------------------------------')
				dict_key = obj.name.split('.')[0]
				if shuffle_tex and dict_key in cfg.tex_idx_dict:
					tex_type = cate+'_tex'
					tex_path = obj_loader.path_to_tex(tex_type)		
					for i in cfg.tex_idx_dict[dict_key]:
						obj_loader.tex_importer(path=tex_path,obj_name=dict_key,idx=i)
				if shuffle_color:
					for i in range(len(obj.material_slots)):
						obj.active_material_index = i
						r = max(0, min(1.0, obj.active_material.diffuse_color[0] + np.random.normal(cfg.normal_m, cfg.normal_s, 1)))
						g = max(0, min(1.0, obj.active_material.diffuse_color[1] + np.random.normal(cfg.normal_m, cfg.normal_s, 1)))
						b = max(0, min(1.0, obj.active_material.diffuse_color[2] + np.random.normal(cfg.normal_m, cfg.normal_s, 1)))
						obj.active_material.diffuse_color = (r,g,b)
		if shuffle_pos:
			coord_idx = list(np.random.choice(cfg.table_top_num_obj,obj_loader.number_obj,replace=False))
			coords = obj_loader.coord_gen_obj()
			util.obj_locator(cate,coords[coord_idx[key]][0],coords[coord_idx[key]][1],cfg.table_height)
		if shuffle_rot:
			util.obj_rotator(cate, 30)
		if shuffle_size:
			scale_ratio = max(1.1, min(2.5, 1.5 + np.random.normal(cfg.normal_m, 1, 1)))
			util.obj_resizer(cate, scale_ratio)
		if shuffle_bg:
			x,y = obj_loader.background_pos_gen()
			util.obj_locator('background',x,y,0)




def batch_generator(base_path,label_tmp_path, pahse):
	mat_copy = {}
	mat_lbl_color = {}
	for obj in bpy.data.objects:
		if not obj.name in no_need_copy:
			mat_ls = []
			for i in range(len(obj.material_slots)):
				mat_ls.append(obj.active_material.copy())
			mat_copy[obj.name] = mat_ls
			for k,v in enumerate(cfg.static_classes):
				if v in obj.name: mat_lbl_color[obj.name] = cfg.static_classes_color[k]
			for k,v in enumerate(cfg.dynamic_classes):
				if not v == 'background':
					if v in obj.name: mat_lbl_color[obj.name] = cfg.dynamic_classes_color[k]


	scn = bpy.context.scene
	for f in range(scn.frame_start, scn.frame_end + 1, scn.frame_step):
		# go to frame f
		print(f)
		scn.frame_set(f)
		scn.render.filepath = os.path.join(base_path, '{:04d}_rgba.png'.format(f-1))
		bpy.ops.render.render( write_still=True ) 

		depth_path_from = '/home/weizhang/Documents/ycb_blender/output/images/Image' + '{:04d}.png'.format(f)
		depth_path_to = os.path.join(base_path, '{:04d}_depth.png'.format(f-1))
		os.rename(depth_path_from,depth_path_to)

		#save meta

	    # output the camera matrix on the current frame
	    # Getting width, height and the camera
		w = scn.render.resolution_x*scn.render.resolution_percentage/100.0
		h = scn.render.resolution_y*scn.render.resolution_percentage/100.0
		cam = bpy.data.cameras['Camera']
		# mat = scn.camera.matrix_world
		# Getting camera parameters
		# Extrinsic
		RT = scn.camera.matrix_world.inverted()
		RT = np.asarray(RT)
		RT = RT[[0,1,2],:]
		# Intrinsic
		K = Matrix().to_3x3()
		K[0][0] = w/2 / tan(cam.angle/2)
		ratio = w/h
		K[1][1] = h/2. / tan(cam.angle/2) * ratio
		K[0][2] = w / 2.
		K[1][2] = h / 2.
		K[2][2] = 1.
		K.transpose()
		K = np.asarray(K)

		P = np.matmul(K,RT)

		meta={}
		meta['factor_depth'] = np.array([[15000]])
		meta['projection_matrix'] = P
		meta['rotation_translation_matrix'] = RT
		meta['intrinsic_matrix'] = K
		

		filename = os.path.join(base_path, '{:04d}_meta.mat'.format(f-1))

		scipy.io.savemat(filename,meta)


	for obj in bpy.data.objects:
		if not obj.name in no_need_copy:
			for i in range(len(obj.material_slots)):
				obj.active_material_index = i
				obj.active_material.diffuse_color = mat_lbl_color[obj.name]
				obj.active_material.use_shadeless = True
				obj.active_material.use_textures[0] = False
				obj.active_material.use_transparency = False
		if 'background' in obj.name:
			obj.hide_render = True



	bpy.data.objects['Plane'].hide_render = True
	bpy.data.objects['Plane.001'].hide_render = True
	bpy.data.objects['Plane.002'].hide_render = True
	bpy.data.objects['Plane.003'].hide_render = True
	bpy.data.objects['Plane.004'].hide_render = True
	# bpy.data.objects['background'].hide_render = True

	scn = bpy.context.scene
	for f in range(scn.frame_start, scn.frame_end + 1, scn.frame_step):
		# go to frame f
		print(f)
		scn.frame_set(f)
		scn.render.filepath = os.path.join(base_path, '{:04d}_label.png'.format(f-1))
		bpy.ops.render.render( write_still=True )


	bpy.data.objects['Plane'].hide_render = False
	bpy.data.objects['Plane.001'].hide_render = False
	bpy.data.objects['Plane.002'].hide_render = False
	bpy.data.objects['Plane.003'].hide_render = False
	bpy.data.objects['Plane.004'].hide_render = False


	for obj in bpy.data.objects:
		if not obj.name in no_need_copy:
			for i in range(len(obj.material_slots)):
				obj.active_material_index = i
				obj.active_material = mat_copy[obj.name][i]


	# scene_filepath = os.path.join(base_path, 'scene.obj')
	# result = bpy.ops.export_scene.obj(filepath=scene_filepath)