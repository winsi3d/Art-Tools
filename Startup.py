import maya.cmds as cmds

# changing default preferences

cmds.currentUnit(time='ntsc')

def createMenu():
        # Query the names of all "MayaWindows"
        mi = cmds.window("MayaWindow", ma = True, q = True)
        
        for m in mi:
            print m
            # If a name matches "UserScripts", delete
            if m == "DojoTools":
                cmds.deleteUI("DojoTools", m = True)
                
            # Create the "UserScripts" menu
        cmds.menu("DojoTools", label = "DojoTools", to = True, p = "MayaWindows")
        
        # Create a menu item for the RDojo UI
        # mc.menuItem("DojoTools", label = "RD_UI", c = createLytItem)
        cmds.menuItem("DojoTools", label = "RD_UI")

"""
def createLytItem(*args):
    import Maya.System.RDojo_UI as RDojo_UI
    reload(RDojo_UI)
    RDojo_UI.RDojo_UI()
"""

createMenu()
