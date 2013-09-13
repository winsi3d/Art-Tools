"""
Script: Arm_Switch
Author: Wini Wang	wini@winsi3d.com
Description: Creates arm Fk Ik switch
"""

import maya.cmds as cmds


CLASS_NAME = "Arm_Switch"
TITLE = "Arm_SWITCH"
DESCRIPTION = "creates FK IK switch for the arm"


class Arm_Switch:
	def __init__(self, FK, IK, IKH, BIND, BINDconstraints):
		print "In Arm switch"
		
		self.FK_list = FK
		self.IK_list = IK
		self.IK_handle_list = IKH
		self.BIND_list = BIND
		self.bindConstraints_list = BINDconstraints

		self.WW_Arm_Switch()


	def WW_Arm_Switch(self):
		# create an IK / FK switch
		switchCtl = []
		switchName = "IkFk_switch"

		cmds.file("/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/fkik_switch.ma", i=True) #imports the switch control
		cmds.select("switch_curve", r=True) #selects the curve
		cmds.rename(switchName) #renames it
		switchCtl.append(cmds.ls(sl=True)) #adds it to the switchCtl list
		switch_pctemp = cmds.pointConstraint(self.BIND_list[2], switchCtl[0], mo=False) #point constrains to snap it to the wrist
		cmds.delete(switch_pctemp) #deletes the pointconstraint
		cmds.xform(switchCtl[0], r=True, t=(0, 2, 0), ro=(90, 0, 0), s=(0.5, 0.5, 0.5)) #places it
		cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False) #freeze transformations
		cmds.parentConstraint(self.BIND_list[2], switchCtl[0], mo=True) #parent constrains the switch control to the wrist joint
		cmds.addAttr(ln="switch", at="enum", en="FK:IK", k=True) #adds a switch attribute


		# sets the constraints to switch from FK to IK with the switch control
		bindConstraints = self.bindConstraints_list
		FKs = self.FK_list
		IKs = self.IK_list
		
		x = 0
		for each in bindConstraints:
			constr_IK = str(each)[3:len(each)-3] + "." + IKs[x] + "W1"
			constr_FK = str(each)[3:len(each)-3] + "." + FKs[x] + "W0"

			cmds.connectAttr("IkFk_switch.switch", constr_IK)
			reverseN = cmds.createNode("reverse", n=str(self.BIND_list[x]) + "_reverseNode")
			cmds.connectAttr("IkFk_switch.switch", reverseN + ".inputX")
			cmds.connectAttr(reverseN+ ".outputX", constr_FK)

			x += 1
			cmds.select(cl=True)



		import Maya.Modules.Controls.WW_Arm_Controls as WW_Arm_Controls
		reload(WW_Arm_Controls)
		print WW_Arm_Controls

		
		circle_list = WW_Arm_Controls.Arm_Controls()

		print circle_list	