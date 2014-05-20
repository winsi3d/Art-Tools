"""
Script: Hinge_Lyt
Author: Wini Wang	wini@winsi3d.com
Description: Creates a hinge layout
"""

import maya.cmds as cmds
import Maya.System.WW_Layout_Utils as Lyt_Utils
reload(Lyt_Utils)



CLASS_NAME = "Hinge_Lyt"
TITLE = "Hinge_Lyt"
DESCRIPTION = "builds a hinge layout"


class Hinge_Lyt:
	def __init__(self):
		print "In Hinge Lyt"
		self.Hinge_Lyt()


	def Hinge_Lyt(self):
		# Gets lists from Lyt_Utils
		ArmLocNames = Lyt_Utils.ArmLocatorNames
		ArmLocPos = Lyt_Utils.ArmLocatorPos

		HandLocNames = Lyt_Utils.HandLocatorNames
		HandLocPos = Lyt_Utils.HandLocatorPos

		LegLocNames = Lyt_Utils.LegLocatorNames
		LegLocPos = Lyt_Utils.LegLocatorPos

		FootRockLocNames = Lyt_Utils.FootRockLocNames
		FootRockPos = Lyt_Utils.FootRockPos

		SpineLocNames = Lyt_Utils.SpineLocatorNames
		SpineLocPos = Lyt_Utils.SpineLocatorPos




		# creates locators based on names and positions in ArmLocNames and ArmLocPos
		arm_loc_list = []
		hand_loc_list = []
		leg_loc_list = []
		foot_loc_list = []
		spine_loc_list = []

		
		arm_root_loc = cmds.spaceLocator(n="L+" + ArmLocNames[0])
		cmds.xform(cp=True)
		cmds.xform(t=ArmLocPos[0])

		cmds.select(cl=True)
		

		x = 1

		for each in ArmLocNames[1:]:
			arm_loc_list.append(cmds.joint(n="L_"+each, a=True, p=ArmLocPos[x]))
			x += 1

		for each in arm_loc_list:
			cmds.joint( each, e=True, zso=True, oj='xyz', sao = 'yup' )


		z = 0
		for each in HandLocNames:
			hand_loc_list.append(cmds.joint(n="L_"+each, a=True, p=HandLocPos[z]))
			if (each == "hand") or (each == "thumb_04") or (each == "index_04") or (each == "middle_04") or (each == "ring_04") or (each == "pinky_04"):
				cmds.select(cl=True)
			z += 1

		for each in hand_loc_list:
			cmds.joint( each, e=True, zso=True, oj='xyz', sao = 'yup' )


		cmds.parent("*thumb_01", "*hand")
		cmds.parent("*index_01", "*hand")
		cmds.parent("*middle_01", "*hand")
		cmds.parent("*ring_01", "*hand")
		cmds.parent("*pinky_01", "*hand")
		


		leg_root_loc = cmds.spaceLocator(n="L+" + LegLocNames[0])
		cmds.xform(cp=True)
		cmds.xform(t=LegLocPos[0])

		cmds.select(cl=True)



		y=1

		for each in LegLocNames[1:]:
			leg_loc_list.append(cmds.joint(n="L_"+each, a=True, p=LegLocPos[y]))
			y += 1
			#cmds.xform(cp=True)
			#cmds.xform(t=LegLocPos[LegLocNames.index(each)])

		for each in FootRockLocNames:
			foot_loc_list.append(cmds.spaceLocator(n="L_"+each))
			cmds.xform(cp=True)
			cmds.xform(t=FootRockPos[FootRockLocNames.index(each)])

		for each in leg_loc_list:
			cmds.joint( each, e=True, zso=True, oj='xyz', sao = 'yup' )
		

		cmds.parent(arm_loc_list[0], arm_root_loc)
		cmds.parent(leg_loc_list[0], leg_root_loc)

		if cmds.objExists("*leg"):
			cmds.parentConstraint(leg_loc_list[len(leg_loc_list)-2], foot_loc_list[0], mo=True)
			cmds.parentConstraint(leg_loc_list[len(leg_loc_list)-2], foot_loc_list[1], mo=True)

		cmds.select(cl=True)




		spine_root_loc = cmds.spaceLocator(n=SpineLocNames[0])
		cmds.xform(cp=True)
		cmds.xform(t=SpineLocPos[0])

		cmds.select(cl=True)
		

		x = 1

		for each in SpineLocNames[1:]:
			spine_loc_list.append(cmds.joint(n="L_"+each, a=True, p=SpineLocPos[x]))
			x += 1

		for each in spine_loc_list:
			cmds.joint( each, e=True, zso=True, oj='xyz', sao = 'yup' )

		cmds.parent(spine_loc_list[0], spine_root_loc)