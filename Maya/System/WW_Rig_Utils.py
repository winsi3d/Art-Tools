"""
Script: Rig_Utils
Author: Wini Wang	wini@winsi3d.com
Description: Builds Rig
"""

import maya.cmds as cmds

def createIK(part, IKstartJoint, IKendJoint):
	print "In Create IK"

	IKName = part + "_IK_handle"
	IK_handle = cmds.ikHandle(n=IKName, sj=IKstartJoint, ee=IKendJoint, sol="ikRPsolver")
	cmds.select(cl=True)

	return IK_handle



def constrainFKIK(BIND_Arm_Joints, FK_Arm_Joints, IK_Arm_Joints):
	print "In Constrain FK IK Joints"


	# constrain the IK and FK joint chains to the BIND chain
	x = 0
	bindConstraints = []
	for eachJoint in BIND_Arm_Joints:
		bindConstraints.append(cmds.parentConstraint(FK_Arm_Joints[x], IK_Arm_Joints[x], BIND_Arm_Joints[x]))
		x += 1

	# hides the FK and IK arm joints
	cmds.setAttr(str(FK_Arm_Joints[0]) + ".visibility", False)
	cmds.setAttr(str(IK_Arm_Joints[0]) + ".visibility", False)




def createFKControls(FK_Arm_Joints):
	print "In Create FK Controls"


	# create circle controllers for the FK chain
	circleCtl = []
	circleCtlGrp = []		
	x = 0

	for eachJoint in FK_Arm_Joints:

		FKname = str(FK_Arm_Joints[x])[3:len(FK_Arm_Joints[x])-4] + "_CTL"

		circleCtl.append(cmds.circle(sections=8, ch=False, n=FKname)) #creates the controller, renames
		cmds.xform(r=True, ro=(0, 90, 0)) #rotate the joint 90 degrees in y
		cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False) #freeze transformations
		circleCtlGrp.append(cmds.group(n=str(FK_Arm_Joints[x])[3:len(FK_Arm_Joints[x])-4] + "_CTL_GRP")) #groups the controller to itself, renames
		fk_pctemp = cmds.parentConstraint(FK_Arm_Joints[x], circleCtlGrp[x], mo = False) #parent constrains the group to the joint to place it in the correct place
		cmds.delete(fk_pctemp) #deletes the parent constraint
		cmds.orientConstraint(circleCtl[x], FK_Arm_Joints[x], mo = True) #parent constrains the joint to the controller
		x += 1


	# parents the controllers and controller groups up the hierachy
	y = 0
	while y < (len(circleCtlGrp)-1):
		cmds.parent(circleCtlGrp[y+1], circleCtlGrp[y])
		y += 1


	cmds.select(cl=True)



def createIKControls(path, IK_Arm_Joints, IK_handle):
	print "In Create IK Controls"

	# create a square controller for the IK chain
	IK_CTL_name = "L_IK_arm" #change name of ik arm control here
	Ctl = []
	CtlGrp = []

	cmds.file(path, i=True) #imports the cube control
	cmds.select("curve1", r=True) #selects the curve
	Ctl.append(cmds.ls(sl=True)) #puts the curve in the Ctl list
	Ctl.append(cmds.duplicate(n=IK_CTL_name + "_gimbal_CTL", )) #duplicated the curve and renames - creates the gimbal control
	cmds.scale(0.8, 0.8, 0.8) #scales it down
	cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False) #freeze transformations
	cmds.parent(Ctl[1], Ctl[0]) #parents the gimbal control to the main control
	cmds.select(Ctl[0]) #selects the main control
	cmds.rename(IK_CTL_name + "_CTL") #renames it appropriately
	CtlGrp.append(cmds.group(n=IK_CTL_name + "_CTL_GRP")) #groups the curve to itself
	ik_pctemp = cmds.parentConstraint(IK_Arm_Joints[2], CtlGrp, mo=False) #parent constrains the group to the joint to place it in the correct place
	cmds.delete(ik_pctemp) #deletes the parent constraint
	cmds.parent(IK_handle[0], Ctl[1]) #parents IK handle to the controller


	# create a pole vector control
	PV = []
	PVGrp = []

	cmds.file("/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/PoleVectorCTL.ma", i=True) #imports the pole vector control
	cmds.select("PVcurve", r=True) #selects the curve
	cmds.rename(IK_CTL_name + "_PV") # rename
	cmds.xform(r=True, ro=(-90, 0, 0), s=(0.3, 0.3, 0.3)) #rotate the joint 90 degrees in x and scales down
	PV.append(cmds.ls(sl=True))
	PVGrp.append(cmds.group(n=IK_CTL_name + "_PV_GRP")) # group it to itself
	pv_pctemp = cmds.pointConstraint(IK_Arm_Joints[1], PVGrp[0], mo=False)# point constraint to snap it to the elbow
	cmds.delete(pv_pctemp) # delete the constraint
	cmds.xform(PV[0], r=True, t=(0, 0, -10)) # move it back in space
	cmds.select(PV[0], r=True)
	cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False) #freeze transformations
	cmds.poleVectorConstraint(PV[0], IK_handle[0])# create the pole vector contraint


def createFKControls(FK_Arm_Joints):
	print "In Create FK Controls"

	# create circle controllers for the FK chain
	circleCtl = []
	circleCtlGrp = []
	x = 0

	for eachJoint in FK_Arm_Joints:
		circleCtl.append(cmds.circle(sections=8, ch=False, n=str(FK_Arm_Joints[x])[3:len(FK_Arm_Joints[x])-4] + "_CTL")) #creates the controller, renames
		cmds.xform(r=True, ro=(0, 90, 0), s=(1.5, 1.5, 1.5)) #rotate the joint 90 degrees in y
		cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False) #freeze transformations
		circleCtlGrp.append(cmds.group(n=str(FK_Arm_Joints[x])[3:len(FK_Arm_Joints[x])-4] + "_CTL_GRP")) #groups the controller to itself, renames
		fk_pctemp = cmds.parentConstraint(FK_Arm_Joints[x], circleCtlGrp[x], mo = False) #parent constrains the group to the joint to place it in the correct place
		cmds.delete(fk_pctemp) #deletes the parent constraint
		cmds.orientConstraint(circleCtl[x], FK_Arm_Joints[x], mo = True) #parent constrains the joint to the controller
		x += 1

	y = 0

	for eachGroup in circleCtlGrp:
		cmds.parent(circleCtlGrp[y+1], circleCtl[y]) #parents the controls and groups up the hierarchy
		y += 1
		if y == len(circleCtlGrp)-1:
			break

	return circleCtl




def createStretchy(start, end, elbowJnt, wristJnt):
	print "In Create Stretchy IK"

	# find the positions of the start and end points
	startPos = cmds.xform(start, q=True, translation=True, worldSpace=True)
	endPos = cmds.xform(end[0], q=True, translation=True, worldSpace=True)


	# create locators at these positions and point constrain them to the start joint and end IK handle control
	startLoc = cmds.spaceLocator(n="DistDim_Start_LOC")[0]
	cmds.pointConstraint(start, startLoc, mo=False)

   	endLoc = cmds.spaceLocator(n="DistDim_End_LOC")[0]
   	cmds.pointConstraint(end[0], endLoc, mo=False)


   	# create the distance dimension shape node
   	distanceNode = cmds.createNode("distanceDimShape", n="%s_%s_distance" % (startLoc,endLoc))


   	# connect the start locator and end locator to the distance dimension startPoint and endPoint
	cmds.connectAttr(startLoc + "Shape.worldPosition[0]", distanceNode + ".startPoint")
	cmds.connectAttr(endLoc + "Shape.worldPosition[0]", distanceNode + ".endPoint")   	
   	

	# create a multiply divide node
	multdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name='stretchyMultDiv')
	cmds.setAttr(str(multdiv) + ".operation", 2)


	# connect the distance dimension shape node to the multiply divide input X
	cmds.connectAttr(str(distanceNode)+".distance", str(multdiv) + ".input1X")


	# find the length when the arm is fully stretched and put value into multiply divide node inpux2X
	restLength = cmds.getAttr(str(elbowJnt) + ".translateX") + cmds.getAttr(str(wristJnt) + ".translateX")
	cmds.setAttr(str(multdiv) + ".input2X", restLength)


	# create a condition node
	stretchyCnd = cmds.shadingNode('condition', asUtility=True, name='stretchyCnd')	
	cmds.setAttr(str(stretchyCnd) + ".operation", 3)


	# connect multiply divide node outputX to condition node first term
	cmds.connectAttr(str(multdiv) + ".outputX", str(stretchyCnd) + ".firstTerm")
	cmds.connectAttr(str(multdiv) + ".outputX", str(stretchyCnd) + ".colorIfTrueR")

	cmds.setAttr(str(stretchyCnd) + ".secondTerm", 1.00)

	cmds.connectAttr(str(stretchyCnd) + ".outColorR", str(start) + ".scaleX")
	cmds.connectAttr(str(stretchyCnd) + ".outColorR", str(elbowJnt) + ".scaleX")




