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
		jntName = prefix + each[0] + "_Jnt"
		jnt = cmds.joint(n=jntName, p=each[1])
		jointInfo.append(jnt)

		pc = cmds.parentConstraint(each[0], jnt)
		cmds.delete(pc)

		cmds.makeIdentity(jnt, apply=True, t=True, r=True, s=True, n=False)


	return jointInfo