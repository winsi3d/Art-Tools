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
		# Add selection to the list
		

"""
		# create a joint based on the position values of the locator
		for eachLoc in listLocator:
			i = listLocator.index(eachLoc)
	    	item = str(listLocator[i])[3:] #slice first three chars from list item 
	    	item = item[:len(item)-2] # slice last two chars from list item
	    	jointLoc = cmds.getAttr(item+'.translate') # jointLoc is an array of the position vals for the locator
	    	
	    	# cmds.select (cl=True); # prevents parenting
	    	cmds.joint (p=(jointLoc[0][0], jointLoc[0][1], jointLoc[0][2]), n=item+'_jnt')
"""