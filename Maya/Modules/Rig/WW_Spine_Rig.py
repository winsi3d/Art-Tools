"""
Script: Arm_Rig
Author: Wini Wang	wini@winsi3d.com
Description: Creates a spine rig
"""

import maya.cmds as cmds
import Maya.System.WW_Joint_Utils as Joint_Utils
reload(Joint_Utils)
import Maya.System.WW_Rig_Utils as Rig_Utils
reload(Rig_Utils)


CLASS_NAME = "Spine_Rig"
TITLE = "Spine_Rig"
DESCRIPTION = "builds a spine rig"



class Spine_Rig:
	def __init__(self):
		print "In Spine Rig"
		self.Spine_Lyt_Check()



	def Spine_Lyt_Check(self, *args):
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
			locatorInfo.pop()


			spineLocatorInfo = locatorInfo[0:5]


			self.Spine_Rig(locatorInfo, spineLocatorInfo, locatorInfo, rootLoc)




		else:
			return cmds.headsUpMessage("Please Select A Root")



	def Spine_Rig(self, locatorInfo, spineLocatorInfo, LocatorInfo, rootLoc):
		part = "Spine"
		print "in love"
	
		# creates the Bind, FK, and IK joints
		BIND_Spine_Joints = Joint_Utils.BuildJoints("BIND_", locatorInfo)
		FK_Spine_Joints = Joint_Utils.BuildJoints("FK_", spineLocatorInfo)

		cmds.delete(rootLoc)

		cmds.select(cl=True)


		import Maya.System.WW_Rig_Utils as Rig_Utils
		reload(Rig_Utils)

		path = "/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/CubeCTL.ma"

		Rig_Utils.SpineSetUp(BIND_Spine_Joints[0:5], path, FK_Spine_Joints)

		FK_Controls = Rig_Utils.createFKControls(part, FK_Spine_Joints)

		Rig_Utils.CleanUp(FK_Controls, IK_Controls, BIND_Arm_Joints, FK_Spine_Joints, IK_Spine_Joints, part, FKIKSwitch, Stretchy)
