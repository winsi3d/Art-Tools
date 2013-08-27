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
	IK_handle = ""

	def __init__(self, FK, IK, IKH):
		print "In Arm controls"
		
		self.FK_list = FK
		self.IK_list = IK
		self.IK_handle = IKH

		self.WW_Arm_Controls()


	def WW_Arm_Controls(self):
		# create a square controller for the IK control
		IK_CTL_name = "L_IK_arm" #change name of ik arm control here
		squareCtl = []
		squareCtlGrp = []

		cmds.file("/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/Cube.ma", i=True) #imports the cube control
		cmds.select("curve1", r=True) #selects the curve
		squareCtl = cmds.ls(sl=True)
		cmds.rename(IK_CTL_name + "_CTL") #renames it appropriates
		squareCtlGrp.append(cmds.group(n=IK_CTL_name + "_CTL_GRP")) #groups the curve to itself
		ik_pctemp = cmds.parentConstraint(self.IK_list[2], squareCtlGrp, mo=False) #parent constrains the group to the joint to place it in the correct place
		cmds.delete(ik_pctemp) #deletes the parent constraint

		print self.IK_handle, squareCtl
		cmds.parent(self.IK_handle[0], IK_CTL_name + "_CTL_GRP") #parents IK handle to the controller



		# create circle controllers for the FK chain
		circleCtl = []
		circleCtlGrp = []
		x = 0

		for eachJoint in self.FK_list:
			circleCtl.append(cmds.circle(sections=8, ch=False, n=str(self.FK_list[x])[3:len(self.FK_list[x])-4] + "_CTL")) #creates the controller, renames
			cmds.xform(r=True, ro=(0, 90, 0)) #rotate the joint 90 degrees in y
			cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False) #freeze transformations
			circleCtlGrp.append(cmds.group(n=str(self.FK_list[x])[3:len(self.FK_list[x])-4] + "_CTL_GRP")) #groups the controller to itself, renames
			fk_pctemp = cmds.parentConstraint(self.FK_list[x], circleCtlGrp[x], mo = False) #parent constrains the group to the joint to place it in the correct place
			cmds.delete(fk_pctemp) #deletes the parent constraint
			cmds.orientConstraint(circleCtl[x], self.FK_list[x], mo = True) #parent constrains the joint to the controller
			x += 1

		# parents the controllers up the hierachy
		y = 0

		for eachGroup in circleCtlGrp:
			cmds.parent(circleCtlGrp[y+1], circleCtl[y]) #parents the controls and groups up the hierarchy
			y += 1
			if y == len(circleCtlGrp)-1:
				break
