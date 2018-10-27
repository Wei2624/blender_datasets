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
from lib import obj_loader

import importlib
importlib.reload(test_config)
importlib.reload(obj_loader)



obj_loader.load_objs(test_config.dynamic_classes, load_bg=0, load_table=1, plane_set=0)
# print(test_config)
