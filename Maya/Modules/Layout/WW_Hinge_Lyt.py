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

		LegLocNames = Lyt_Utils.LegLocatorNames
		LegLocPos = Lyt_Utils.LegLocatorPos

		FootRockLocNames = Lyt_Utils.FootRockLocNames
		FootRockPos = Lyt_Utils.FootRockPos




		# creates locators based on names and positions in ArmLocNames and ArmLocPos
		arm_loc_list = []
		leg_loc_list = []
		foot_loc_list = []

		for each in ArmLocNames:
			arm_loc_list.append(cmds.spaceLocator(n="L_"+each))
			cmds.xform(cp=True)
			cmds.xform(t=ArmLocPos[ArmLocNames.index(each)])

		for each in LegLocNames:
			leg_loc_list.append(cmds.spaceLocator(n="L_"+each))
			cmds.xform(cp=True)
			cmds.xform(t=LegLocPos[LegLocNames.index(each)])

		for each in FootRockLocNames:
			foot_loc_list.append(cmds.spaceLocator(n="L_"+each))
			cmds.xform(cp=True)
			cmds.xform(t=FootRockPos[FootRockLocNames.index(each)])
		



		# parents the locators to the root locator
		x = 0
		while x < (len(arm_loc_list)-1):
			cmds.parent(arm_loc_list[x+1], arm_loc_list[x])
			x += 1

		y = 0
		while y < (len(leg_loc_list)-1):
			cmds.parent(leg_loc_list[y+1], leg_loc_list[y])
			y += 1

		cmds.parentConstraint(leg_loc_list[len(leg_loc_list)-2], foot_loc_list[0], mo=True)
		cmds.parentConstraint(leg_loc_list[len(leg_loc_list)-2], foot_loc_list[1], mo=True)



		cmds.select(cl=True)