"""
Script: armRig_UI
Author: Wini Wang   wini@winsi3d.com
Description: Creates an arm rig
"""

import maya.cmds as cmds
import Maya.Modules.Layout.WW_Arm_Lyt as WW_Arm_Lyt
reload(WW_Arm_Lyt)
import Maya.Modules.Rig.WW_Arm_Rig as WW_Arm_Rig
reload(WW_Arm_Rig)


class armRig_UI:
    
    def __init__(self):
        print "In armRig_UI"
        
   
        self.UI_Elements = {}
        
        self.windowName = "armRigUI_Window"
        if cmds.window(self.windowName, exists = True):
            cmds.deleteUI(self.windowName)
        
        windowWidth = 80
        windowHeight = 40
        
        buttonWidth = 70
        buttonHeight = 33
        
        self.UI_Elements["window"] = cmds.window(self.windowName, width = windowWidth, height = windowHeight, title = "armRig_UI", sizeable = True)

        self.UI_Elements["buttonLyt"] = cmds.flowLayout(v=True, width=windowWidth, height=windowHeight)
        self.UI_Elements["Arm_LytButton"] = cmds.button(label="Arm Lyt", width=buttonWidth, height=buttonHeight, p=self.UI_Elements["buttonLyt"], c=self.createArmLyt)
        self.UI_Elements["Arm_RigButton"] = cmds.button(label="Arm Rig", width=buttonWidth, height=buttonHeight, p=self.UI_Elements["buttonLyt"], c=self.createArmRig)
        
        
        cmds.showWindow(self.windowName)



    def createArmLyt(self, *args):        
        WW_Arm_Lyt.Arm_Lyt()
        print WW_Arm_Lyt.DESCRIPTION


    def createArmRig(self, *args):        
        WW_Arm_Rig.Arm_Rig()
        print WW_Arm_Rig.DESCRIPTION

