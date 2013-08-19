import os 
import sys
import pymel.core as pm
import maya.cmds as cmds

sys.path.append(os.environ['Art Tools'])

startup = pm.evalDeferred("import Startup")