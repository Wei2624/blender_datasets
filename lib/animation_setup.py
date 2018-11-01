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

# random.seed(3)


def cam_point_to(point):
	# loc_camera = bpy.data.objects['Camera'].matrix_world.to_translation()
	loc_camera = bpy.data.objects['Camera'].location
	# print(loc_camera)

	direction = Vector(point) - loc_camera
	# point the cameras '-Z' and use its 'Y' as up
	rot_quat = direction.to_track_quat('-Z', 'Y')

	# assume we're using euler rotation
	bpy.data.objects['Camera'].rotation_euler = rot_quat.to_euler()

def clear_all_keyframes_cam():
	for obj in bpy.data.objects:
		obj.select = False
	bpy.data.objects['Camera'].select = True
	bpy.ops.anim.keyframe_clear_v3d()

def initial_cam_pos():
	scale = np.random.randint(0,int((cfg.cam_xy_range[1] - cfg.cam_xy_range[0])/cfg.range_unit)+1)
	# print(scale)
	x = cfg.cam_xy_range[0] + scale*cfg.range_unit
	scale = np.random.randint(0,int((cfg.cam_xy_range[1] - cfg.cam_xy_range[0])/cfg.range_unit)+1)
	# print(scale)
	y = cfg.cam_xy_range[0] + scale*cfg.range_unit
	scale = np.random.randint(0,int((cfg.cam_height_range[1] - cfg.cam_height_range[0])/cfg.range_unit)+1)
	# print(scale)
	z = cfg.cam_height_range[0] + scale*cfg.range_unit

	return (x,y,z)

def transform_cam_pos_2d(pos,theta):
	rot_mat = np.array([[cos(radians(theta)),-sin(radians(theta))],[sin(radians(theta)),cos(radians(theta))]])
	return np.matmul(rot_mat,np.asarray(pos))



def setup_keyframes():
	clear_all_keyframes_cam()

	rot_degrees = np.random.randint(1, cfg.num_degrees+1)*cfg.degree_interval
	# num_keyframes = 4
	# if rot_degrees > 90:
	# 	num_keyframes = int(rot_degrees/cfg.degree_interval)+1

	num_keyframes = cfg.total_frames
	theta = float(rot_degrees/num_keyframes)


	frame_interval = int(cfg.total_frames/num_keyframes)

	kf_index = 0

	cam_pos = initial_cam_pos()
	# print(cam_pos)

	# bpy.data.objects['Camera'].location = cam_pos
	# cam_point_to(cfg.target_point)

	for i in range(num_keyframes+1):
		bpy.data.objects['Camera'].location = cam_pos
		cam_point_to(cfg.target_point)


		#set keyframes
		bpy.context.scene.frame_current = i*frame_interval
		bpy.ops.anim.keyframe_insert(type='BUILTIN_KSI_LocRot')

		xy = transform_cam_pos_2d((cam_pos[0],cam_pos[1]),theta)

		cam_pos = (xy[0],xy[1],cam_pos[2])









