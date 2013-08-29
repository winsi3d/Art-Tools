"""
Script: Arm_Controls
Author: Wini Wang	wini@winsi3d.com
Description: Creates arm controls
"""

import maya.cmds as cmds


CLASS_NAME = "Arm_Controls"
TITLE = "Arm_CONTROLS"
DESCRIPTION = "creates arm controls based off the rig"


class Arm_Controls:

	FK_list = ""
	IK_list = ""
	IK_handle_list = ""

	def __init__(self, FK, IK, IKH):
		print "In Arm controls"
		
		self.FK_list = FK
		self.IK_list = IK
		self.IK_handle_list = IKH

		self.WW_Arm_Controls()


	def WW_Arm_Controls(self):



# create an IK / FK switch
		switchCtl = []
		switchName = "IkFk_switch"

		cmds.circle(n=switchName)
        switchCtl.append(cmds.ls(sl=True))
        switch_pctemp = cmds.pointConstraint(self.FK_list[2], switchCtl[1], mo=False)# point constraint to snap it to the elbow
        cmds.delete(switch_pctemp)
        cmds.xform(switchCtl[0], r=True, t=(0, 5, 0), s=(0.2, 0,2, 0.2))
        cmds.select(switchCtl[0], r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)
        cmds.addAttr(ln=FkIk_switch, at="enum", en="FK:IK", k=True)