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
	def __init__():
		print "In Arm controls"
		
		self.FK_list = FK
		self.IK_list = IK
		self.IK_handle_list = IKH

		self.WW_Arm_Controls()


	def WW_Arm_Controls(self, FK, IK, IKH):
		# create a square controller for the IK chain
		IK_CTL_name = "L_IK_arm" #change name of ik arm control here
		squareCtl = []
		squareCtlGrp = []

		cmds.file("/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/CubeCTL.ma", i=True) #imports the cube control
		cmds.select("curve1", r=True) #selects the curve
		squareCtl.append(cmds.ls(sl=True)) #puts the curve in the squareCtl list
		squareCtl.append(cmds.duplicate(n=IK_CTL_name + "_gimbal_CTL", )) #duplicated the curve and renames - creates the gimbal control
		cmds.scale(0.8, 0.8, 0.8) #scales it down
		cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False) #freeze transformations
		cmds.parent(squareCtl[1], squareCtl[0]) #parents the gimbal control to the main control
		cmds.select(squareCtl[0]) #selects the main control
		cmds.rename(IK_CTL_name + "_CTL") #renames it appropriately
		squareCtlGrp.append(cmds.group(n=IK_CTL_name + "_CTL_GRP")) #groups the curve to itself
		ik_pctemp = cmds.parentConstraint(self.IK_list[2], squareCtlGrp, mo=False) #parent constrains the group to the joint to place it in the correct place
		cmds.delete(ik_pctemp) #deletes the parent constraint
		cmds.parent(self.IK_handle_list[0], squareCtl[1]) #parents IK handle to the controller

		# create a pole vector control
		PV = []
		PVGrp = []

		cmds.file("/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/PoleVectorCTL.ma", i=True) #imports the pole vector control
		cmds.select("PVcurve", r=True) #selects the curve
		cmds.rename(IK_CTL_name + "_PV") # rename
		cmds.xform(r=True, ro=(-90, 0, 0), s=(0.3, 0.3, 0.3)) #rotate the joint 90 degrees in x and scales down
		PV.append(cmds.ls(sl=True))
		PVGrp.append(cmds.group(n=IK_CTL_name + "_PV_GRP")) # group it to itself
		pv_pctemp = cmds.pointConstraint(self.IK_list[1], PVGrp[0], mo=False)# point constraint to snap it to the elbow
		cmds.delete(pv_pctemp) # delete the constraint
		cmds.xform(PV[0], r=True, t=(0, 0, -10)) # move it back in space
		cmds.select(PV[0], r=True)
		cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False) #freeze transformations
		cmds.poleVectorConstraint(PV[0], self.IK_handle_list[0])# create the pole vector contraint



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

		return circleCtl

		# parents the controllers up the hierachy
		y = 0

		for eachGroup in circleCtlGrp:
			cmds.parent(circleCtlGrp[y+1], circleCtl[y]) #parents the controls and groups up the hierarchy
			y += 1
			if y == len(circleCtlGrp)-1:
				break
				
		