"""
Script: Arm_Rig
Author: Wini Wang	wini@winsi3d.com
Description: Creates an arm rig
"""

import maya.cmds as cmds
import Maya.System.WW_Joint_Utils as Joint_Utils
reload(Joint_Utils)
#import Maya.Modules.Controls.WW_Arm_Controls as WW_Arm_Controls
#reload(WW_Arm_Controls)
#import Maya.Modules.Controls.WW_Arm_Switch as WW_Arm_Switch
#reload(WW_Arm_Switch)

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


		import Maya.System.WW_Rig_Utils as Rig_Utils
		reload(Rig_Utils)

		IK_handle = Rig_Utils.createIK("L_Arm", IK_Arm_Joints[0], IK_Arm_Joints[2])

		Rig_Utils.constrainFKIK(BIND_Arm_Joints, FK_Arm_Joints, IK_Arm_Joints)	

		Rig_Utils.createStretchy(IK_Arm_Joints[0], IK_handle, IK_Arm_Joints[1], IK_Arm_Joints[2])

		path = "/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/CubeCTL.ma"

		Rig_Utils.createFKControls(FK_Arm_Joints)


		
		Rig_Utils.createIKControls(path, IK_Arm_Joints, IK_handle)

"""

	def callArmCtrl(self):
		WW_Arm_Controls.Arm_Controls(self.FK_list, self.IK_list, self.IK_handle_list)

	def callArmSwitch(self):
		WW_Arm_Switch.Arm_Switch(self.FK_list, self.IK_list, self.IK_handle_list, self.BIND_list, self.bindConstraints_list)



	"""
