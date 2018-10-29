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


def scene_setup(load_obj,load_bg,load_table, plane_set):
	obj_loader.load_setup_objs(load_obj=load_obj, load_bg=load_bg, load_table=load_table, plane_set=plane_set)