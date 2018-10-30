no_need_to_copy = ['Camera','Lamp','Lamp.001','Lamp.002','skp_camera_Last_Saved_SketchUp_View','background'\
				,'Plane','Plane.001','Plane.002']

# static_classes = ['background','table']
# static_classes_color = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)]

static_classes = ['table']
static_classes_color = [(1.0, 0.0, 0.0)]

obj_alpha = 1.0


# changing this can remove certain object from appearing in the scene
# dynamic_classes = ['book', 'keyboard', 'mug', 'detergent', 'bottle', 'pringles']
# dynamic_classes_color = [(0.0, 1.0, 0.0), (0.0, 1.0, 1.0), (0.0, 0.0, 0.5), (0.0, 0.0, 1.0),(1.0, 1.0, 0.0), (1.0, 0.0, 1.0)]

dynamic_classes = ['pringles']
dynamic_classes_color = [(0.0, 1.0, 1.0)]

table_height = 1.
table_dim = (2., 1., 2.)
table_top_num_obj = 4

area_div = 4
v_bound = 0.75
h_bound = 0.75
h_div_unit = 0.03
v_div_unit = 0.03

num_of_lights = 3
randomize_xyz = False
lamp_xy = [(1.3, -0.75),(-1.3, -0.75),(0, 1.5)]
plane_scale = 20
light_z_range = (1.8, 3)
range_unit = 0.1

tex_idx_dict = {'table1_0':[0],\
				'book1_2': [0],\
				'book2_3':[0],\
				'book3_3': [0],\
				'book4_0': [0],\
				'book5_0': [0,1,2,3,4],\
				'table2_0':[0],\
				'bottle1_4': [0],\
				'bottle2_4': [0],\
				'bottle3_0': [0],\
				'bottle4_11':[0],\
				'bottle5_10':[0],\
				'bottle5_15':[0],\
				'bottle6_1': [0],\
				'bottle6_9': [0],\
				'bottle7_0': [0],\
				'table3_0': [0],\
				'detergent1_1':[0],\
				'detergent2_0': [0],\
				'detergent3_4': [0],\
				'detergent4_3': [0],\
				'detergent5_0': [0],\
				'detergent6_7': [0],\
				'table4_0':[2],\
				'keyboard1_24':[0],\
				'keyboard2_190':[0],\
				'keyboard3_72':[0],\
				'keyboard4_99':[0],\
				'keyboard5_484':[0],\
				'keyboard6_289':[0],\
				'table5_0':[0],\
				'mug1_0': [0],\
				'mug2_3': [0],\
				'mug3_5': [0],\
				'mug4_0': [0],\
				'mug5_7': [0],\
				'mug6_2': [0],\
				'mug7_0': [0],\
				'table6_0':[0],\
				'pringles1_2': [0],\
				'pringles2_2': [0]
				}




