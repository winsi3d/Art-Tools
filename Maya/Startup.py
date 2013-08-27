import maya.cmds as cmds


def createMenu():
        # Query the names of all "MayaWindows"
        mi = cmds.window("MayaWindow", ma = True, q = True)
        
        for m in mi:
            print m
            # If a name matches "UserScripts", delete
            if m == "RiggingTools":
                cmds.deleteUI("RiggingTools", m = True)
                
            # Create the "UserScripts" menu
        cmds.menu('RiggingTools', label='RiggingTools', to=True, p="MayaWindow")
        
        # Create a menu item for the RDojo UI
        cmds.menuItem("RiggingTools", label = "armRig_UI", c = createLytItem)


def createLytItem(*args):
    import Maya.System.armRig_UI as armRig_UI
    reload(armRig_UI)
    armRig_UI.armRig_UI()


createMenu()
