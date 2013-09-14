"""
Script: Joint_Utils
Author: Wini Wang	wini@winsi3d.com
Description: Builds Joints
"""

import maya.cmds as cmds

def BuildJoints(prefix, locatorInfo):
	cmds.select(d=True)
	jointInfo = []

	for each in locatorInfo:
		jntName = prefix + each[0] + "_JNT"
		jnt = cmds.joint(n=jntName, p=each[1])
		jointInfo.append(jnt)

	return jointInfo