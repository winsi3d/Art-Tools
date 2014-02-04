"""
Script: armRig_UI
Author: Wini Wang   wini@winsi3d.com
Description: Creates an arm rig
"""

import maya.cmds as cmds
import Maya.Modules.Layout.WW_Hinge_Lyt as Hinge_Lyt
reload(Hinge_Lyt)
import Maya.Modules.Rig.WW_Arm_Rig as WW_Arm_Rig
reload(WW_Arm_Rig)
import Maya.Modules.Controls.WW_Arm_Controls as WW_Arm_Controls
reload(WW_Arm_Controls)
import Maya.Modules.Controls.WW_Arm_Switch as WW_Arm_Switch
reload(WW_Arm_Switch)
from functools import partial


class armRig_UI:
    
    def __init__(self):
        print "In armRig_UI"
            
   
        self.UI_Elements = {}
        
        self.windowName = "armRigUI_Window"
        if cmds.window(self.windowName, exists = True):
            cmds.deleteUI(self.windowName)
        
        windowWidth = 80
        windowHeight = 40
        
        buttonWidth = 80
        buttonHeight = 33
        
        self.UI_Elements["window"] = cmds.window(self.windowName, width = windowWidth, height = windowHeight, title = "armRig_UI", sizeable = True)

        self.UI_Elements["buttonLyt"] = cmds.flowLayout(v=True, width=windowWidth, height=windowHeight)

        fileDirectory = "/Users/Winsi/Documents/Art Tools/Maya/Modules/Layout/"
        for widget in self.returnWidgets(fileDirectory):
            print widget

            mod = __import__("Maya.Modules.Layout."+widget, {}, {}, [widget])
            reload (mod)
            title = mod.TITLE
            description = mod.DESCRIPTION
            classname = mod.CLASS_NAME

            cmds.separator(p=self.UI_Elements["buttonLyt"])
            self.UI_Elements["module_button_" + widget] = cmds.button(label=title, width=buttonWidth, height=buttonHeight, p=self.UI_Elements["buttonLyt"], c=partial(self.installLytWidget, widget))



        fileDirectory = "/Users/Winsi/Documents/Art Tools/Maya/Modules/Rig/"
        for widget in self.returnWidgets(fileDirectory):
            print widget

            mod = __import__("Maya.Modules.Rig."+widget, {}, {}, [widget])
            reload (mod)
            title = mod.TITLE
            description = mod.DESCRIPTION
            classname = mod.CLASS_NAME

            cmds.separator(p=self.UI_Elements["buttonLyt"])
            self.UI_Elements["module_button_" + widget] = cmds.button(label=title, width=buttonWidth, height=buttonHeight, p=self.UI_Elements["buttonLyt"], c=partial(self.installRigWidget, widget))




    

        

        
        cmds.showWindow(self.UI_Elements["window"])



    def installLytWidget(self, widget, *args):
        mod = __import__("Maya.Modules.Layout."+widget, {}, {}, [widget])
        reload (mod)
        widgetClass  = getattr(mod, mod.CLASS_NAME)
        widgetInstance = widgetClass()



    def installRigWidget(self, widget, *args):
        mod = __import__("Maya.Modules.Rig."+widget, {}, {}, [widget])
        reload (mod)
        widgetClass  = getattr(mod, mod.CLASS_NAME)
        widgetInstance = widgetClass()



    inst = ""

    #def createArmRig(self, *args):        
    #    self.inst = WW_Arm_Rig.Arm_Rig()
    #    print WW_Arm_Rig.DESCRIPTION

    def createArmControls(self, *args): 
        self.inst.callArmCtrl()
        print WW_Arm_Controls.DESCRIPTION
        self.inst.callArmSwitch()
        print WW_Arm_Switch.DESCRIPTION

    def returnWidgets(self, path, *args):
        import File_Utils as fileUtils
        reload(fileUtils)
        allPyFiles = fileUtils.findAllFiles(path, ".py")
        return allPyFiles

