# Creates a list called listNames and add locator names to the list

listNames = [ "lctr_1_arm1", "lctr_l_arm2", "lctr_l_wrist", "lctrr_l_armEnd" ]

listLocator = [];


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


# deselect all
cmds.select (cl=True); # prevents joints being parented to last created locator


# creates joints based off each locator

for eachLoc in listLocator:
    i = listLocator.index(eachLoc)
    item = str(listLocator[i])[3:] #slice first three chars from list item 
    item = item[:len(item)-2] # slice last two chars from list item
    jointLoc = cmds.getAttr(item+'.translate') # jointLoc is an array of the position vals for the locator
    
    # cmds.select (cl=True); # prevents parenting
    cmds.joint (p=(jointLoc[0][0], jointLoc[0][1], jointLoc[0][2]), n=item+'_jnt') 