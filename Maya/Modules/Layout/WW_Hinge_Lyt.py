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


		# creates locators based on names and positions in ArmLocNames and ArmLocPos
		loc_list = []

		for each in ArmLocNames:
			loc_list.append(cmds.spaceLocator(n="L_"+each))
			cmds.xform(cp=True)
			cmds.xform(t=ArmLocPos[ArmLocNames.index(each)])


		# parents the locators to the root locator
		x = 0
		while x < (len(loc_list)-1):
			cmds.parent(loc_list[x+1], loc_list[x])
			x += 1




		cmds.select(cl=True)