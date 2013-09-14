"""
Script: Rig_Utils
Author: Wini Wang	wini@winsi3d.com
Description: Builds Rig
"""

import maya.cmds as cmds

def createIK(part, IKstartJoint, IKendJoint):
	print "In Create IK"

	IKName = part + "_IK_handle"
	cmds.ikHandle(n=IKName, sj=IKstartJoint, ee=IKendJoint, sol="ikRPsolver")
	cmds.select(cl=True)




def constrainFKIK(BIND_Arm_Joints, FK_Arm_Joints, IK_Arm_Joints):
	print "In Constrain FK IK Joints"


	# constrain the IK and FK joint chains to the BIND chain
	x = 0
	bindConstraints = []
	for eachJoint in BIND_Arm_Joints:
		bindConstraints.append(cmds.parentConstraint(FK_Arm_Joints[x], IK_Arm_Joints[x], BIND_Arm_Joints[x]))
		x += 1

	# hides the FK and IK arm joints
	cmds.setAttr(str(FK_Arm_Joints[0]) + ".visibility", False)
	cmds.setAttr(str(IK_Arm_Joints[0]) + ".visibility", False)
