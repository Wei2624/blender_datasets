no_need_to_copy = ['Camera','Lamp','Lamp.001','Lamp.002','skp_camera_Last_Saved_SketchUp_View','background'\
				,'Plane','Plane.001','Plane.002']

# static_classes = ['background','table']
# static_classes_color = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)]

off_table_classes = ['chair']

static_classes = ['table']
static_classes_color = [(1.0, 0.0, 0.0)]

obj_alpha = 1.0


# changing this can remove certain object from appearing in the scene
# dynamic_classes = ['book', 'keyboard', 'mug', 'detergent', 'bottle', 'pringles']
# dynamic_classes_color = [(0.0, 1.0, 0.0), (0.0, 1.0, 1.0), (0.0, 0.0, 0.5), (0.0, 0.0, 1.0),(1.0, 1.0, 0.0), (1.0, 0.0, 1.0)]

dynamic_classes = ['can']
dynamic_classes_color = [(0.0, 1.0, 1.0)]

#table dimension parameters
table_height = 1.
table_dim = (2., 1., 2.)
table_top_num_obj = 4
area_div = 4
v_bound = 0.75
h_bound = 0.75
h_div_unit = 0.03
v_div_unit = 0.03

#Lights parameters
num_of_lights = 3
randomize_xyz = False
lamp_xy = [(1.3, -0.75),(-1.3, -0.75),(0, 1.5)]
plane_scale = 20
light_z_range = (1.8, 3)
range_unit = 0.1

# texture information
tex_idx_dict = {'table1_0':[0],\
				'book1_2': [0],'book2_1':[0],'book3_3': [0],'book4_0': [0],'book5_0': [0,1,2,3,4],\
				'table2_0':[0],\
				'bottle1_4': [0],'bottle2_4': [0],'bottle3_0': [0],'bottle4_11':[0],'bottle5_10':[0],'bottle5_15':[0],'bottle6_1': [0],'bottle6_9': [0],'bottle7_0': [0],\
				'table3_0': [0],\
				'detergent1_1':[0],'detergent2_0': [0],'detergent3_4': [0],'detergent4_3': [0],'detergent4_5': [0],'detergent5_0': [0],'detergent6_7': [0],\
				'table4_0':[2],\
				'keyboard1_24':[0],'keyboard2_190':[0],'keyboard3_72':[0],'keyboard4_99':[0],'keyboard5_484':[0],'keyboard6_289':[0],\
				'table5_0':[0],\
				'mug1_0': [0],'mug2_3': [0],'mug3_5': [0],'mug4_0': [0],'mug5_7': [0],'mug6_2': [0],'mug7_0': [0],\
				'table6_0':[0],\
				'pringles1_1': [0],'pringles1_2': [0],'pringles2_2': [0],\
				'cerealbox0_0': [0],'cerealbox0_1': [0],'cerealbox0_3': [0],'cerealbox0_5': [0],'cerealbox0_6': [0],'cerealbox0_7': [0],'cerealbox0_8': [0],\
				'cerealbox1_71': [0],'cerealbox1_166': [0],'cerealbox1_66': [0],'cerealbox1_123': [0],\
				'cerealbox2_493': [0],'cerealbox2_302': [0],'cerealbox2_349': [0],'cerealbox2_256': [0],'cerealbox2_194': [0],'cerealbox2_494': [0],'cerealbox2_225': [0],'cerealbox2_257': [0], 'cerealbox2_203': [0],\
				'cerealbox3_1': [0],'cerealbox3_5': [0],'cerealbox3_4': [0],'cerealbox3_0': [0],'cerealbox3_2': [0],\
				'cerealbox4_42': [0], \
				'cerealbox5_0': [0], 'cerealbox5_1': [0],'cerealbox5_2': [0],'cerealbox5_4': [0],\
				'cerealbox6_6': [0], 'cerealbox7_0': [0], 'cerealbox8_5':[0],'cerealbox8_0':[0],'cerealbox8_1':[0],'cerealbox8_6':[0],\
				'cerealbox9_5':[0],\
				'bowl0_2': [0],'bowl1_0': [0],'bowl2_2': [0], 'bowl3_1': [0], 'bowl4_1': [0], 'bowl5_0': [0], 'bowl6_0':[0],\
				'can0_3': [0], 'can1_8': [0], 'can2_0': [0], 'can3_0': [0], 'can4_5': [0], 'can5_1': [0]
				}


# Gaussian samples
normal_m = 0
normal_s = 0.2

# position of background in range on x y
background_range = (2, 3.5)

# interval where script reloads a scene
change_scene_interval = 4


# camera parameters for keyframes
degree_interval = 30
num_degrees = 12
cam_height_range = (1.3, 3.0)
cam_xy_range = (1.2, 2.5)

total_frames = 100

target_point = (0,0,1.2)




