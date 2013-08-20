"""
Script: Arm_Lyt
Author: Wini Wang	wini@winsi3d.com
Description: Creates an arm layout
"""

import maya.cmds as cmds

CLASS_NAME = "Arm_Lyt"
TITLE = "Arm_LYT"
DESCRIPTION = "builds an arm layout"


class Arm_Lyt:
	def __init__(self):
		print "In Arm Lyt"
		self.WW_Arm_Lyt()


	def WW_Arm_Lyt(self):
		# Creates a list called listNames and add locator names to the list

		listNames = [ "lctr_1_arm1", "lctr_l_arm2", "lctr_l_wrist", "lctrr_l_armEnd" ]

		listLocator = []


		# Creates a for loop for each item in listNames and renames them accordingly
		for item in listNames:
			listLocator.append(cmds.spaceLocator(n = listNames[listNames.index(item)]))
			
		# print listLocators name and position    
		for eachItem in listLocator:
		    print eachItem
		    print listLocator.index(eachItem)
		 
		    
		# moves the locators    
		cmds.move( 4, 12, 0, listLocator[0], absolute=True )
		cmds.move( 12, 12, -3, listLocator[1], absolute=True )
		cmds.move( 20, 12, 0, listLocator[2], absolute=True )
		cmds.move( 23, 12, 0, listLocator[3], absolute=True )