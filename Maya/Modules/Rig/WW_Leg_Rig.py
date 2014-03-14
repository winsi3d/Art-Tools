"""
Script: Leg_Rig
Author: Wini Wang	wini@winsi3d.com
Description: Creates a leg rig
"""

import maya.cmds as cmds
import Maya.System.WW_Joint_Utils as Joint_Utils
reload(Joint_Utils)
import Maya.Modules.Layout.WW_Hinge_Lyt as Hinge_Lyt
reload(Hinge_Lyt)


CLASS_NAME = "Leg_Rig"
TITLE = "Leg_Rig"
DESCRIPTION = "builds a leg rig"


class Leg_Rig:
	def __init__(self):
		print "In Leg Rig"
		self.Leg_Lyt_Check()


	def Leg_Lyt_Check(self, *args):
		locatorInfo = []
		rootLoc = cmds.ls(sl=True)
		print rootLoc
		print rootLoc[0]

		rootCheck = rootLoc[0].rpartition("_")[2]
		print rootCheck

		if rootCheck == "root":
			print "Root is selected"

			rootChildren = cmds.listRelatives(rootLoc, allDescendents = True, type = "transform")
			print rootChildren

			for each in rootChildren:
				pos = cmds.xform(each, q=True, ws=True, t=True)
				locatorInfo.append([each, pos])


			locatorInfo.reverse()

			self.Leg_Rig(locatorInfo)

		else:
			return cmds.headsUpMessage("Please Select A Root")



	def Leg_Rig(self, locatorInfo):
		part = "L_Leg"
		PVtranslate = (0, 0, 5)
		SwitchTranslate = (2, 0, 0)

		# creates the Bind, FK, and IK joints
		BIND_Leg_Joints = Joint_Utils.BuildJoints("BIND_", locatorInfo)
		FK_Leg_Joints = Joint_Utils.BuildJoints("FK_", locatorInfo)
		IK_Leg_Joints = Joint_Utils.BuildJoints("IK_", locatorInfo)

		cmds.select(cl=True)

		import Maya.System.WW_Rig_Utils as Rig_Utils
		reload(Rig_Utils)



		# creates the IK handle
		IK_handle = Rig_Utils.createIK(part, IK_Leg_Joints[1], IK_Leg_Joints[3])

		# constrains the FK and IK joints to the Bind joints
		bindConstraints = Rig_Utils.constrainFKIK(BIND_Leg_Joints, FK_Leg_Joints, IK_Leg_Joints)	

		print IK_Leg_Joints
		print IK_handle

		# create stretchy IK
		Stretchy = Rig_Utils.createStretchy(part, IK_Leg_Joints[1], IK_handle, IK_Leg_Joints[2], IK_Leg_Joints[3])

		# create FK and IK controls
		path = "/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/FootCTL.ma"
		PVpath = "/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/PoleVectorCTL.ma"
		FK_Controls = Rig_Utils.createFKControls(part, FK_Leg_Joints)
		IK_Controls = Rig_Utils.createIKControls(part, path, IK_handle, PVpath, PVtranslate)


		# create the FK IK switch
		SwitchPath = "/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/fkik_switch.ma"
		FKIKSwitch = Rig_Utils.FKIKSwitch(part, SwitchPath, BIND_Leg_Joints, FK_Leg_Joints, IK_Leg_Joints, bindConstraints, FK_Controls, IK_Controls, SwitchTranslate)

		Rig_Utils.FootSetUp(IK_Leg_Joints, IK_handle, IK_Controls)

		Rig_Utils.CleanUp(FK_Controls, IK_Controls, BIND_Leg_Joints, FK_Leg_Joints, IK_Leg_Joints, part, FKIKSwitch, Stretchy)