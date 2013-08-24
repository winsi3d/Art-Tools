"""
Script: Arm_Rig
Author: Wini Wang	wini@winsi3d.com
Description: Creates an arm rig
"""

import maya.cmds as cmds

CLASS_NAME = "Arm_Rig"
TITLE = "Arm_RIG"
DESCRIPTION = "builds an arm rig"


class Arm_Rig:
	def __init__(self):
		print "In Arm Rig"
		self.WW_Arm_Rig()


	def WW_Arm_Rig(self):
		# adds the selection to the list, armLocatorList
		armLocatorList = cmds.ls(sl=True)

		# prints the list
		print armLocatorList

		# clears the selection to prevent joints being parents to any selected object
		cmds.select(cl=True)


		# creates the BIND joints for each item in armLocatorList
		for each in armLocatorList:
			pos = cmds.xform(each, q=True, t=True)
			print pos

			cmds.joint(p=pos, n="BIND_"+each+"_jnt")

		cmds.select(cl=True)

		# creates the IK joints for each item in armLocatorList
		for each in armLocatorList:
			cmds.joint(p=pos, n="IK_"+each+"_jnt")

		cmds.select(cl=True)

		# creates the FK joints for each item in armLocatorList
		for each in armLocatorList:
			cmds.joint(p=pos, n="FK_"+each+"_jnt")
			
		cmds.select(cl=True)