import maya.cmds as cmds

class Rdojo_UI:
    
    def __init__(self):
        print "In Rdojo_UI"
        
   
        self.UI_Elements = {}
        
        self.windowName = "RDojoUI_Window"
        if cmds.window(self.windowName, exists = True):
            cmds.deleteUI(self.windowName)
        
        windowWidth = 80
        windowHeight = 40
        
        buttonWidth = 70
        buttonHeight = 33
        
        self.UI_Elements["window"] = cmds.window(self.windowName, width = windowWidth, height = windowHeight, title = "RDojo_UI", sizeable = True)

        self.UI_Elements["buttonLyt"] = cmds.flowLayout(v=True, width=windowWidth, height=windowHeight)
        self.UI_Elements["hingeButton"] = cmds.button(label="Hinge Lyt", width=buttonWidth, height=buttonHeight, p=self.UI_Elements["buttonLyt"], c=self.doStuff)
        
        
        cmds.showWindow(self.windowName)



def doStuff(self, *args):
    cmds.button(self.UI_Elements["hingeButton"], edit=True, en=False)