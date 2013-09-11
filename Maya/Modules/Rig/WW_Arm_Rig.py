"""
Script: Arm_Rig
Author: Wini Wang	wini@winsi3d.com
Description: Creates an arm rig
"""

import maya.cmds as cmds
import Maya.Modules.Controls.WW_Arm_Controls as WW_Arm_Controls
reload(WW_Arm_Controls)
import Maya.Modules.Controls.WW_Arm_Switch as WW_Arm_Switch
reload(WW_Arm_Switch)

CLASS_NAME = "Arm_Rig"
TITLE = "Arm_RIG"
DESCRIPTION = "builds an arm rig"


class Arm_Rig:
	def __init__(self):
		print "In Arm Rig"
		self.WW_Arm_Rig()


	def WW_Arm_Rig(self):
		# adds the selection to the list, armLocatorList
		armLocatorList = cmds.ls(sl=True)

		# prints the list
		print armLocatorList

		# clears the selection to prevent joints being parents to any selected object
		cmds.select(cl=True)

		# creates an empty list for the BIND joint chain
		BIND_Arm_Joints = []

		# creates the BIND joints for each item in armLocatorList
		for each in armLocatorList:
			pos = cmds.xform(each, q=True, t=True)
			print pos

			BIND_Arm_Joints.append(cmds.joint(p=pos, n="BIND_"+each+"_jnt"))

		cmds.select(cl=True)

		# creates an empty list for the IK joint chain
		IK_Arm_Joints = []
		IK_handle = []

		# creates the IK joints for each item in armLocatorList
		for each in armLocatorList:
			pos = cmds.xform(each, q=True, t=True)
			IK_Arm_Joints.append(cmds.joint(p=pos, n="IK_"+each+"_JNT"))

		# assigns the start and end joint of the chain to the variables IKstartJoint and IKendJoint
		IKstartJoint = IK_Arm_Joints[0]
		IKendJoint = IK_Arm_Joints[len(IK_Arm_Joints)-2]

		print IKstartJoint
		print IKendJoint
 
		# creates an IK handle
		cmds.ikHandle(n="armIK_handle", sj=IKstartJoint, ee=IKendJoint, sol="ikRPsolver")
		IK_handle = cmds.ls(sl=True)
		print IK_handle

		cmds.select(cl=True)

		# creates an empty list for the FK joint chain
		FK_Arm_Joints = []

		# creates the FK joints for each item in armLocatorList
		for each in armLocatorList:
			pos = cmds.xform(each, q=True, t=True)
			FK_Arm_Joints.append(cmds.joint(p=pos, n="FK_"+each+"_jnt"))

		cmds.select(cl=True)


		# constrain the IK and FK joint chains to the BIND chain
		x = 0
		bindConstraints = []

		for eachJoint in BIND_Arm_Joints:
			bindConstraints.append(cmds.parentConstraint(FK_Arm_Joints[x], IK_Arm_Joints[x], BIND_Arm_Joints[x]))
			x += 1

		# hides the FK and IK arm joints
		cmds.setAttr(str(FK_Arm_Joints[0]) + ".visibility", False)
		cmds.setAttr(str(IK_Arm_Joints[0]) + ".visibility", False)

		self.FK_list = FK_Arm_Joints
		self.IK_list = IK_Arm_Joints
		self.IK_handle_list = IK_handle
		self.BIND_list = BIND_Arm_Joints
		self.bindConstraints_list = bindConstraints

	def callArmCtrl(self):
		WW_Arm_Controls.Arm_Controls(self.FK_list, self.IK_list, self.IK_handle_list)

	def callArmSwitch(self):
		WW_Arm_Switch.Arm_Switch(self.FK_list, self.IK_list, self.IK_handle_list, self.BIND_list, self.bindConstraints_list)




