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

	def __init__(self, FK, IK):
		print "In Arm controls"
		
		self.FK_list = FK
		self.IK_list = IK

		self.WW_Arm_Controls()


	def WW_Arm_Controls(self):
		# create a square controller for the IK control
		

		# create circle controllers for the FK chain
		circleCtl = []
		circleCtlGrp = []
		x = 0

		for eachJoint in self.FK_list:
			circleCtl.append(cmds.circle(sections=8, ch=False, n=str(self.FK_list[x])[3:len(self.FK_list[x])-4] + "_CTL")) #creates the controller, renames
			cmds.xform(r=True, ro=(0, 90, 0)) #rotate the joint 90 degrees in y
			cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False) #freeze transformations
			circleCtlGrp.append(cmds.group(n=str(self.FK_list[x])[3:len(self.FK_list[x])-4] + "_CTL_GRP")) #groups the controller to itself, renames
			pctemp = cmds.parentConstraint(self.FK_list[x], circleCtlGrp[x], mo = False) #parent constrains the group to the joint to place it in the correct place
			cmds.delete(pctemp) #deletes the parent constraint
			cmds.orientConstraint(circleCtl[x], self.FK_list[x], mo = True) #parent constrains the joint to the controller
			x += 1

		# parents the controllers up the hierachy
		y = 0

		for eachGroup in circleCtlGrp:
			cmds.parent(circleCtlGrp[y+1], circleCtl[y])
			y += 1
			if y == len(circleCtlGrp)-1:
				break
