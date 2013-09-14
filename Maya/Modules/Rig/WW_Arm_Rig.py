"""
Script: Arm_Rig
Author: Wini Wang	wini@winsi3d.com
Description: Creates an arm rig
"""

import maya.cmds as cmds
import Maya.System.WW_Joint_Utils as Joint_Utils
reload(Joint_Utils)
import Maya.System.WW_Rig_Utils as Rig_Utils
reload(Rig_Utils)
#import Maya.Modules.Controls.WW_Arm_Controls as WW_Arm_Controls
#reload(WW_Arm_Controls)
#import Maya.Modules.Controls.WW_Arm_Switch as WW_Arm_Switch
#reload(WW_Arm_Switch)

CLASS_NAME = "Arm_Rig"
TITLE = "Arm_RIG"
DESCRIPTION = "builds an arm rig"


class Arm_Rig:
	def __init__(self):
		print "In Arm Rig"

		locatorInfo = []
		rootLoc = cmds.ls(sl=True)

		rootCheck = rootLoc[0].partition("_")[2]


		if rootCheck == "root":
			print "Root is selected"

			rootChildren = cmds.listRelatives(rootLoc, allDescendents = True, type = "transform")

			for each in rootChildren:
				pos = cmds.xform(each, q=True, ws=True, t=True)
				locatorInfo.append([each, pos])


			locatorInfo.reverse()

			self.Arm_Rig(locatorInfo)

		else:
			return cmds.headsUpMessage("Please Select A Root")



	def Arm_Rig(self, locatorInfo):
		BIND_Arm_Joints = Joint_Utils.BuildJoints("BIND_", locatorInfo)
		FK_Arm_Joints = Joint_Utils.BuildJoints("FK_", locatorInfo)
		IK_Arm_Joints = Joint_Utils.BuildJoints("IK_", locatorInfo)

		cmds.select(cl=True)

		print BIND_Arm_Joints


"""

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



	"""
