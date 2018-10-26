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

no_need_copy = ['Camera','Lamp','Lamp.001','Lamp.002','skp_camera_Last_Saved_SketchUp_View','background'\
				,'Plane','Plane.001','Plane.002']


def sample_generator(rgbd_path,label_path, phase):

	mat_copy = {}
	mat_lbl_color = {}
	for obj in bpy.data.objects:
		if obj.name in no_need_copy:continue
		mat_ls = []
		for i in range(len(obj.material_slots)):
			obj.active_material_index = i
			obj.active_material.use_transparency = False
			mat_ls.append(obj.active_material.copy())
		mat_copy[obj.name] = mat_ls
		if 'laptop' in obj.name : mat_lbl_color[obj.name] = (0.,0.,1.)
		if 'book' in obj.name : mat_lbl_color[obj.name] = (0.,1.,0.)
		if 'table' in obj.name : mat_lbl_color[obj.name] = (1.,0.,0.)
		if 'keyboard' in obj.name : mat_lbl_color[obj.name] = (0.,1.,1.)
		if 'bottle' in obj.name : mat_lbl_color[obj.name] = (1.,1.,0.)
		if 'monitor' in obj.name : mat_lbl_color[obj.name] = (1.,0.,1.)
		if 'mug' in obj.name : mat_lbl_color[obj.name] = (0.,0.,0.5)

	scn = bpy.context.scene
	for f in range(scn.frame_start, scn.frame_end + 1, scn.frame_step):
		# go to frame f
		print(f)
		scn.frame_set(f)
		scn.render.filepath = os.path.join(rgbd_path, '{:04d}_rgba.png'.format(f-1))
		bpy.ops.render.render( write_still=True ) 

		depth_path_from = '/home/weizhang/Documents/ycb_blender/output/images/Image' + '{:04d}.png'.format(f)
		depth_path_to = os.path.join(rgbd_path, '{:04d}_depth.png'.format(f-1))
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
		

		filename = os.path.join(rgbd_path, '{:04d}_meta.mat'.format(f-1))

		scipy.io.savemat(filename,meta)


	for obj in bpy.data.objects:
		if obj.name in no_need_copy:continue
		for i in range(len(obj.material_slots)):
			obj.active_material_index = i
			obj.active_material.diffuse_color = mat_lbl_color[obj.name]
			obj.active_material.use_shadeless = True
			obj.active_material.use_textures[0] = False
			obj.active_material.use_transparency = False



	bpy.data.objects['Plane'].hide_render = True
	bpy.data.objects['Plane.001'].hide_render = True
	bpy.data.objects['Plane.002'].hide_render = True
	bpy.data.objects['background'].hide_render = True



	scn = bpy.context.scene
	for f in range(scn.frame_start, scn.frame_end + 1, scn.frame_step):
		# go to frame f
		print(f)
		scn.frame_set(f)
		scn.render.filepath = os.path.join(rgbd_path, '{:04d}_label.png'.format(f-1))
		bpy.ops.render.render( write_still=True )
		# label_path_from = os.path.join(label_path, '{:04d}_label.png'.format(f-1))
		# label_path_to = os.path.join(rgbd_path, '{:04d}_label.png'.format(f-1))

	# bpy.data.objects['Plane'].hide_render = False


	# scn = bpy.context.scene
	# for f in range(scn.frame_start, scn.frame_end + 1, scn.frame_step):
	# 	# go to frame f
	# 	print(f)
	# 	scn.frame_set(f)
	# 	scn.render.filepath = os.path.join(rgbd_path, '{:04d}_label_plane.png'.format(f-1))
	# 	bpy.ops.render.render( write_still=True )
	


	bpy.data.objects['Plane'].hide_render = False
	bpy.data.objects['Plane.001'].hide_render = False
	bpy.data.objects['Plane.002'].hide_render = False

	for obj in bpy.data.objects:
		if obj.name in no_need_copy:continue
		for i in range(len(obj.material_slots)):
			obj.active_material_index = i
			obj.active_material = mat_copy[obj.name][i]


	scene_filepath = os.path.join(rgbd_path, 'scene.obj')
	result = bpy.ops.export_scene.obj(filepath=scene_filepath)

	plane_setup()
	obj_remover('background')
	bg_loader()

def form_conf_dict():
	obj_conf = {}
	book = []
	book_dict = {'id':'book','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/148/148.obj'}
	book.append(book_dict)
	book_dict = {'id':'book','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/319/319.obj'}
	book.append(book_dict)
	book_dict = {'id':'book','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/book1/model.dae'}
	book.append(book_dict)
	book_dict = {'id':'book','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/book2/model.dae'}
	book.append(book_dict)
	book_dict = {'id':'book','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/book3/model.dae'}
	book.append(book_dict)
	obj_conf['book'] = book


	table = []
	table_dict = {'id':'table','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/470/470.obj'}
	table.append(table_dict)
	table_dict = {'id':'table','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/474/474.obj'}
	table.append(table_dict)
	table_dict = {'id':'table','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/452/452.obj'}
	table.append(table_dict)
	table_dict = {'id':'table','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/468/468.obj'}
	table.append(table_dict)
	table_dict = {'id':'table','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/504/504.obj'}
	table.append(table_dict)
	table_dict = {'id':'table','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/525/525.obj'}
	table.append(table_dict)
	obj_conf['table'] = table


	laptop = []
	laptop_dict = {'id':'laptop','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/120/120.obj'}
	laptop.append(laptop_dict)
	laptop_dict = {'id':'laptop','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/laptop1/model.dae'}
	laptop.append(laptop_dict)
	laptop_dict = {'id':'laptop','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/laptop2/model.dae'}
	laptop.append(laptop_dict)
	laptop_dict = {'id':'laptop','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/laptop3/model.dae'}
	laptop.append(laptop_dict)
	laptop_dict = {'id':'laptop','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/laptop4/model.dae'}
	laptop.append(laptop_dict)
	laptop_dict = {'id':'laptop','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/laptop5/model.dae'}
	laptop.append(laptop_dict)
	laptop_dict = {'id':'laptop','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/laptop6/model.dae'}
	laptop.append(laptop_dict)
	obj_conf['laptop'] = laptop


	keyboard = []
	keyboard_dict = {'id':'keyboard','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/keyboard1/model.dae'}
	keyboard.append(keyboard_dict)
	laptop_dict = {'id':'keyboard','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/keyboard2/model.dae'}
	keyboard.append(keyboard_dict)
	keyboard_dict = {'id':'keyboard','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/keyboard3/model.dae'}
	keyboard.append(keyboard_dict)
	keyboard_dict = {'id':'keyboard','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/keyboard4/model.dae'}
	keyboard.append(keyboard_dict)
	keyboard_dict = {'id':'keyboard','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/keyboard5/model.dae'}
	keyboard.append(keyboard_dict)
	keyboard_dict = {'id':'keyboard','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/keyboard6/model.dae'}
	obj_conf['keyboard'] = keyboard




	bottle = []
	bottle_dict = {'id':'bottle','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/bottle1/model.dae'}
	bottle.append(bottle_dict)
	laptop_dict = {'id':'bottle','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/bottle2/model.dae'}
	bottle.append(bottle_dict)
	bottle_dict = {'id':'bottle','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/bottle3/model.dae'}
	bottle.append(bottle_dict)
	bottle_dict = {'id':'bottle','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/bottle4/model.dae'}
	bottle.append(bottle_dict)
	bottle_dict = {'id':'bottle','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/bottle5/model.dae'}
	bottle.append(bottle_dict)
	bottle_dict = {'id':'bottle','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/bottle6/model.dae'}
	bottle.append(bottle_dict)
	bottle_dict = {'id':'bottle','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/243/243.obj'}
	obj_conf['bottle'] = bottle




	monitor = []
	monitor_dict = {'id':'monitor','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/monitor1/model.dae'}
	monitor.append(monitor_dict)
	monitor_dict = {'id':'monitor','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/monitor2/model.dae'}
	monitor.append(monitor_dict)
	monitor_dict = {'id':'monitor','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/monitor3/model.dae'}
	monitor.append(monitor_dict)
	monitor_dict = {'id':'monitor','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/monitor4/model.dae'}
	monitor.append(monitor_dict)
	monitor_dict = {'id':'monitor','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/monitor5/model.dae'}
	monitor.append(monitor_dict)
	monitor_dict = {'id':'monitor','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/monitor6/model.dae'}
	obj_conf['monitor'] = monitor



	mug = []
	mug_dict = {'id':'mug','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/mug1/model.dae'}
	mug.append(mug_dict)
	mug_dict = {'id':'mug','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/mug2/model.dae'}
	mug.append(mug_dict)
	mug_dict = {'id':'mug','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/mug3/model.dae'}
	mug.append(mug_dict)
	mug_dict = {'id':'mug','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/mug4/model.dae'}
	mug.append(mug_dict)
	mug_dict = {'id':'mug','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/mug5/model.dae'}
	mug.append(mug_dict)
	mug_dict = {'id':'mug','file_type':'dae'\
					,'file_path':'/home/weizhang/Documents/suncg/3dWarehouse/mug6/model.dae'}
	mug.append(mug_dict)
	mug_dict = {'id':'mug','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/s__1660/s__1660.obj'}
	obj_conf['mug'] = mug

	return obj_conf

def plane_conf():
	wall_tex_path = ['/home/weizhang/Documents/suncg/texture/bricks_1.jpg'\
					,'/home/weizhang/Documents/suncg/texture/bricks_1_2.jpg'\
					,'/home/weizhang/Documents/suncg/texture/bricks_1_3.jpg'\
					,'/home/weizhang/Documents/suncg/texture/bricks_1_4.jpg'\
					,'/home/weizhang/Documents/suncg/texture/bricks_2.jpg'\
					,'/home/weizhang/Documents/suncg/texture/bricks_2_2.jpg'\
					,'/home/weizhang/Documents/suncg/texture/bricks_2_3.jpg'\
					,'/home/weizhang/Documents/suncg/texture/bricks_2_4.jpg']
	floor_tex_path = ['/home/weizhang/Documents/suncg/texture/carpet.jpg'\
					 ,'/home/weizhang/Documents/suncg/texture/carpet_1_1.jpg'\
					 ,'/home/weizhang/Documents/suncg/texture/carpet_1_2.jpg'\
					 ,'/home/weizhang/Documents/suncg/texture/carpet_1_3.jpg'\
					 ,'/home/weizhang/Documents/suncg/texture/carpet_1_4.jpg'\
					 ,'/home/weizhang/Documents/suncg/texture/carpet_1_5.jpg'\
					 ,'/home/weizhang/Documents/suncg/texture/carpet_1_6.jpg'\
					 ,'/home/weizhang/Documents/suncg/texture/tile1.jpg'\
					 ,'/home/weizhang/Documents/suncg/texture/tile2.jpg'\
					 ,'/home/weizhang/Documents/suncg/texture/tile_1_1.jpg'\
					 ,'/home/weizhang/Documents/suncg/texture/tile_1_2.jpg'\
					 ,'/home/weizhang/Documents/suncg/texture/tile_2_1.jpg'\
					 ,'/home/weizhang/Documents/suncg/texture/tile_2_2.jpg']

	return wall_tex_path,floor_tex_path

def bg_conf():
	bg = []
	bg_dict = {'id':'background','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/s__2413/s__2413.obj'}
	bg.append(bg_dict)
	bg_dict = {'id':'background','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/s__2414/s__2414.obj'}
	bg.append(bg_dict)
	bg_dict = {'id':'background','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/s__2415/s__2415.obj'}
	bg.append(bg_dict)
	bg_dict = {'id':'background','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/s__2416/s__2416.obj'}
	bg.append(bg_dict)
	bg_dict = {'id':'background','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/167/167.obj'}
	bg.append(bg_dict)
	bg_dict = {'id':'background','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/168/168.obj'}
	bg.append(bg_dict)
	bg_dict = {'id':'background','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/169/169.obj'}
	bg.append(bg_dict)
	bg_dict = {'id':'background','file_type':'obj'\
					,'file_path':'/home/weizhang/Documents/suncg/object/170/170.obj'}
	bg.append(bg_dict)

	return bg

def bg_loader():
	bg_list = bg_conf()
	idx = random.randint(0,len(bg_list)-1)
	if bg_list[idx]['file_type'] == 'obj':
		result = bpy.ops.import_scene.obj(filepath=bg_list[idx]['file_path'])
	else: 
		result = bpy.ops.wm.collada_import(filepath=bg_list[idx]['file_path'])
	for o in bpy.context.selected_objects:
			o.name = 'background'



def plane_setup():
	wall_tex_path,floor_tex_path = plane_conf()
	wall_path_1 = wall_tex_path[random.randint(0,len(wall_tex_path)-1)]
	wall_path_2 = wall_tex_path[random.randint(0,len(wall_tex_path)-1)]
	floor_path = floor_tex_path[random.randint(0,len(floor_tex_path)-1)]

	img = bpy.data.images.load(floor_path, check_existing=False)
	tex = bpy.data.textures.new(name='floor_text',type='IMAGE')
	tex.image = img
	bpy.data.objects['Plane'].active_material.active_texture = tex

	img = bpy.data.images.load(wall_path_1, check_existing=False)
	tex = bpy.data.textures.new(name='floor_text',type='IMAGE')
	tex.image = img
	bpy.data.objects['Plane.001'].active_material.active_texture = tex

	img = bpy.data.images.load(wall_path_2, check_existing=False)
	tex = bpy.data.textures.new(name='floor_text',type='IMAGE')
	tex.image = img
	bpy.data.objects['Plane.002'].active_material.active_texture = tex



def load_obj(cate_list,bg):
	obj_conf = form_conf_dict()
	for each in cate_list:
		idx = random.randint(0,len(obj_conf[each])-1)
		if obj_conf[each][idx]['file_type'] == 'obj':
			result = bpy.ops.import_scene.obj(filepath=obj_conf[each][idx]['file_path'])
		else: 
			result = bpy.ops.wm.collada_import(filepath=obj_conf[each][idx]['file_path'])

		for o in bpy.context.selected_objects:
			o.name = each
	if bg: bg_loader()


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

def batch_generator():
	phase = 1
	start_idx = 0
	# cate_list_toadd = ['laptop','bottle','table','book','keyboard','monitor','mug']
	cate_list_toadd = ['laptop','bottle','table','book','keyboard','monitor','mug']


	if phase == 1: load_obj(cate_list_toadd)
	if phase == 2: obj_selector('laptop')
	if phase == 3:
		for i in range(start_idx,start_idx + 1):
			print(i)
			rgbd_path = '/home/weizhang/Documents/ycb_blender/output/'  + '{:04d}/'.format(i)
			label_path = '/home/weizhang/Documents/ycb_blender/output/'  + '{:04d}_label/'.format(i)
			if not os.path.exists(rgbd_path):
				os.mkdir(rgbd_path)
			if not os.path.exists(label_path):
				os.mkdir(label_path)
			sample_generator(rgbd_path,label_path,phase)
			os.rmdir(label_path)
	if phase == 4:obj_remover()


batch_generator()































laptop_path = '/home/weizhang/Documents/suncg/3dWarehouse/laptop1/model.dae'

result = bpy.ops.wm.collada_import(filepath=laptop_path)

for o in bpy.context.selected_objects:
	print(o.name)
	o.name = 'laptop'
	print(o.name)


print(result)





book_path = '/home/weizhang/Documents/suncg/object/148/148.obj'


result = bpy.ops.import_scene.obj(filepath=book_path)
if result.pop():book_object = bpy.context.selected_objects[0]
print(len(book_object.material_slots))

book_object.name = 'book'
print('Imported name: ', book_object.name)

book_img_path = '/home/weizhang/Pictures/alog_texture.jpg'
img = bpy.data.images.load(book_img_path, check_existing=False)
tex = bpy.data.textures.new(name='book_text',type='IMAGE')
tex.image = img

book_object.active_material.active_texture = tex

book_mat_copy = book_object.active_material.copy()

book_object.active_material.use_textures[0] = False
book_object.active_material.diffuse_color = (1,0,0)
book_object.active_material.use_shadeless = True

book_object.active_material = book_mat_copy






def loadImage(imgName):
    img = bpy.data.add_image(imgName)
    tex = bpy.data.textures.new('TexName')
    tex.type = 'IMAGE' 
    print("Recast", tex, tex.type)
    tex = tex.recast_type()
    print("Done", tex, tex.type)
    tex.image = img
    mat = bpy.data.materials.new('MatName')
    mat.add_texture(texture = tex, texture_coordinates = 'ORCO', map_to = 'COLOR') 
    ob = bpy.context.object
    bpy.ops.object.material_slot_remove()
    me = ob.data
    me.add_material(mat)
    return

loadImage('/home/thomas/picture.jpg')