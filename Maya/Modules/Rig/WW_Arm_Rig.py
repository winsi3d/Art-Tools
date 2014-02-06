"""
Script: Arm_Rig
Author: Wini Wang	wini@winsi3d.com
Description: Creates an arm rig
"""

import maya.cmds as cmds
import Maya.System.WW_Joint_Utils as Joint_Utils
reload(Joint_Utils)


CLASS_NAME = "Arm_Rig"
TITLE = "Arm_Rig"
DESCRIPTION = "builds an arm rig"


class Arm_Rig:
	def __init__(self):
		print "In Arm Rig"
		self.Arm_Lyt_Check()


	def Arm_Lyt_Check(self, *args):
		locatorInfo = []
		rootLoc = cmds.ls(sl=True)
		print rootLoc
		print rootLoc[0]

		rootCheck = rootLoc[0].rpartition("_")[2]
		print rootCheck

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
		part = "L_Arm"
		PVtranslate = (0, 0, -10)
		SwitchTranslate = (0, 5, 0)

		# creates the Bind, FK, and IK joints
		BIND_Arm_Joints = Joint_Utils.BuildJoints("BIND_", locatorInfo)
		FK_Arm_Joints = Joint_Utils.BuildJoints("FK_", locatorInfo)
		IK_Arm_Joints = Joint_Utils.BuildJoints("IK_", locatorInfo)

		cmds.select(cl=True)

		import Maya.System.WW_Rig_Utils as Rig_Utils
		reload(Rig_Utils)


		# creates the IK handle
		IK_handle = Rig_Utils.createIK(part, IK_Arm_Joints[0], IK_Arm_Joints[2])

		# constrains the FK and IK joints to the Bind joints
		bindConstraints = Rig_Utils.constrainFKIK(BIND_Arm_Joints, FK_Arm_Joints, IK_Arm_Joints)	

		# create stretchy IK
		Stretchy = Rig_Utils.createStretchy(part, IK_Arm_Joints[0], IK_handle, IK_Arm_Joints[1], IK_Arm_Joints[2])

		# create FK and IK controls
		path = "/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/CubeCTL.ma"
		PVpath = "/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/PoleVectorCTL.ma"
		FK_Controls = Rig_Utils.createFKControls(part, FK_Arm_Joints)
		IK_Controls = Rig_Utils.createIKControls(part, path, IK_handle, PVpath, PVtranslate)

		# create the FK IK switch
		SwitchPath = "/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/fkik_switch.ma"
		FKIKSwitch = Rig_Utils.FKIKSwitch(part, SwitchPath, BIND_Arm_Joints, FK_Arm_Joints, IK_Arm_Joints, bindConstraints, FK_Controls, IK_Controls, SwitchTranslate)

		Rig_Utils.CleanUp(FK_Controls, IK_Controls, BIND_Arm_Joints, FK_Arm_Joints, IK_Arm_Joints, part, FKIKSwitch, Stretchy)
