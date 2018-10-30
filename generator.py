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

import importlib
importlib.reload(cfg)
importlib.reload(obj_loader)
importlib.reload(util)
importlib.reload(scene_gen)

random.seed(3)


# util.obj_selector('keyboard')
setup_scene.scene_setup(load_obj=1, load_bg=0, load_table=1, plane_set=0)
# util.obj_remover(cfg.dynamic_classes)
# util.obj_locator('table',0.5,0.5,1)
# util.obj_resizer('keyboard',(1,1,1))
# util.lights_setup()

