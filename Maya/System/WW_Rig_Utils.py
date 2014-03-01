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



def constrainFKIK(BindJoints, FKJoints, IKJoints):
	print "In Constrain FK IK Joints"

	# constrain the IK and FK joint chains to the BIND chain
	x = 0
	bindConstraints = []
	for eachJoint in BindJoints:
		bindConstraints.append(cmds.parentConstraint(FKJoints[x], IKJoints[x], BindJoints[x]))
		x += 1

	# hides the FK and IK arm joints
	cmds.setAttr(str(FKJoints[0]) + ".visibility", False)
	cmds.setAttr(str(IKJoints[0]) + ".visibility", False)


	return bindConstraints


def createFKControls(part, FK_Arm_Joints):
	print "In Create FK Controls"

	# create circle controllers for the FK chain
	circleCtl = []
	circleCtlGrp = []
	x = 0


	for eachJoint in FK_Arm_Joints:

		# set the name here
		FKname = str(FK_Arm_Joints[x])[3:len(FK_Arm_Joints[x])-4]

		# create the controller
		circleCtl.append(cmds.circle(sections=8, ch=False, n=FKname + "_CTL"))
		
		# rotates the joint 90 degrees in y and freeze transformations
		cmds.xform(r=True, ro=(0, 90, 0), s=(1.5, 1.5, 1.5))
		cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)

		# groups the controller to itself, and renames
		circleCtlGrp.append(cmds.group(n=FKname + "_CTL_GRP"))

		#parent constrains the group to the joint to place it in the correct place, and deletes the constraint
		fk_pctemp = cmds.parentConstraint(FK_Arm_Joints[x], circleCtlGrp[x], mo = False)
		cmds.delete(fk_pctemp)

		# parent constrains the joint to the controller
		cmds.orientConstraint(circleCtl[x], FK_Arm_Joints[x], mo = True)


		x += 1


	y = 0

	# parents the controls and groups up the hierarchy
	for eachGroup in circleCtlGrp:
		cmds.parent(circleCtlGrp[y+1], circleCtl[y])
		y += 1
		if y == len(circleCtlGrp)-1:
			break

	return circleCtl




def createIKControls(part, path, IK_handle, PVpath, PVtranslate):
	print "In Create IK Controls"
	print part

	Ctl = []
	CtlGrp = []

	# Find the IK effector joint
	IKEffectorJnt = cmds.listConnections(IK_handle[1])
	print IKEffectorJnt

	# Find the PV joint from the effector joint
	PVJoint = cmds.listRelatives(IKEffectorJnt[1], parent=True)
	print PVJoint
	

	"""
	Controls
	"""

	# import the cube control, rename, and add it to Ctl list
	cmds.file(path, i=True)
	cmds.select("curve1", r=True)
	cmds.rename(part + "_IK_CTL")
	Ctl.append(cmds.ls(sl=True))

	# duplicate the curve to create the gimbal control, and rename
	Ctl.append(cmds.duplicate(n=part + "_IK_gimbal_CTL", ))
	cmds.scale(0.8, 0.8, 0.8)
	cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)

	# parent the gimbal control to the main control
	cmds.parent(Ctl[1], Ctl[0])

	# select the controller
	cmds.select(Ctl[0], r=True)
	
	# groups the curve to itself
	CtlGrp.append(cmds.group(n=part + "_IK_CTL_GRP"))
	

	# parent constrain the group to the joint to place get the translations and rotations from the joint, and deletes the constraint
	if part.rpartition("_")[2] == "Arm":
		ik_pctemp = cmds.parentConstraint(IKEffectorJnt[1], CtlGrp, mo=False)
		cmds.delete(ik_pctemp)

	elif part.rpartition("_")[2] == "Leg":
		ik_pctemp = cmds.pointConstraint(IKEffectorJnt[1], CtlGrp, mo=False)
		cmds.delete(ik_pctemp)
		
		cmds.select(Ctl[0])
		cmds.addAttr(longName="Roll", attributeType="enum", en="---", keyable=True)
		cmds.addAttr(longName="footRoll", attributeType="float", min=-10, max=10, dv=0, keyable=True)
		cmds.addAttr(longName="toeRoll", attributeType="float", min=-10, max=10, dv=0, keyable=True)
		cmds.addAttr(longName="toeWiggle", attributeType="float", min=-10, max=10, dv=0, keyable=True)

		cmds.addAttr(longName="Rock", attributeType="enum", en="---", keyable=True)
		cmds.addAttr(longName="footRock", attributeType="float", min=-10, max=10, dv=0, keyable=True)

		cmds.addAttr(longName="Pivot", attributeType="enum", en="---", keyable=True)
		cmds.addAttr(longName="toePivot", attributeType="float", min=-10, max=10, dv=0, keyable=True)
		cmds.addAttr(longName="ballPivot", attributeType="float", min=-10, max=10, dv=0, keyable=True)
		cmds.addAttr(longName="heelPivot", attributeType="float", min=-10, max=10, dv=0, keyable=True)

		

		cmds.setAttr(Ctl[0][0]+".Roll", lock=True)
		cmds.setAttr(Ctl[0][0]+".Rock", lock=True)
		cmds.setAttr(Ctl[0][0]+".Pivot", lock=True)
		

	cmds.select(Ctl[0])
	cmds.addAttr(longName="Extra", attributeType="enum", en="---", keyable=True)
	cmds.setAttr(Ctl[0][0]+".Extra", lock=True)
	cmds.addAttr(longName="Gimbal", attributeType="bool", keyable=True)
	cmds.connectAttr(Ctl[0][0]+".Gimbal", Ctl[1][0] + ".visibility")
		
		
	# parent the IK handle to the controller
	cmds.parent(IK_handle[0], Ctl[1])



	"""
	Pole Vector
	"""

	# create a pole vector control
	PV = []
	PVGrp = []

	# import pole vector control and rename
	cmds.file(PVpath, i=True)
	cmds.select("PVcurve", r=True)
	cmds.rename(part + "_PV")

	# rotate the joint 90 degrees in x and scale down
	cmds.xform(r=True, ro=(-90, 0, 0), s=(0.2, 0.2, 0.2))

	# group it to itself
	PV.append(cmds.ls(sl=True))
	PVGrp.append(cmds.group(n=part + "_PV_GRP"))

	# point constrain to snap it to the elbow, and delete the constraint
	pv_pctemp = cmds.pointConstraint(PVJoint[0], PVGrp[0], mo=False)
	cmds.delete(pv_pctemp)

	# move it back in space and freeze transformations
	cmds.xform(PV[0], r=True, t=(PVtranslate))
	cmds.select(PV[0], r=True)
	cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)

	# creates the pole vector constraint
	cmds.poleVectorConstraint(PV[0], IK_handle[0])

	return Ctl, PV



def createStretchy(part, start, end, stretchybone1, stretchybone2):
	print "In Create Stretchy IK"

	# find the positions of the start and end points
	startPos = cmds.xform(start, q=True, translation=True, worldSpace=True)
	endPos = cmds.xform(end[0], q=True, translation=True, worldSpace=True)


	# create locators at these positions and point constrain them to the start joint and end IK handle control
	startLoc = cmds.spaceLocator(n=part + "_DistDim_Start_LOC")[0]
	cmds.pointConstraint(start, startLoc, mo=False)

   	endLoc = cmds.spaceLocator(n=part + "_DistDim_End_LOC")[0]
   	cmds.pointConstraint(end[0], endLoc, mo=False)


   	# create the distance dimension shape node
   	distanceNode = cmds.createNode("distanceDimShape", n="%s_%s_distance" % (startLoc,endLoc))


   	# connect the start locator and end locator to the distance dimension startPoint and endPoint
	cmds.connectAttr(startLoc + "Shape.worldPosition[0]", distanceNode + ".startPoint")
	cmds.connectAttr(endLoc + "Shape.worldPosition[0]", distanceNode + ".endPoint")   	
   	

	# create a multiply divide node
	multdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name=part + "_stretchyMultDiv")
	cmds.setAttr(str(multdiv) + ".operation", 2)


	# connect the distance dimension shape node to the multiply divide input X
	cmds.connectAttr(str(distanceNode)+".distance", str(multdiv) + ".input1X")


	# find the length when the arm is fully stretched and put value into multiply divide node inpux2X
	restLength = cmds.getAttr(str(stretchybone1) + ".translateX") + cmds.getAttr(str(stretchybone2) + ".translateX")
	cmds.setAttr(str(multdiv) + ".input2X", restLength)


	# create a condition node
	stretchyCnd = cmds.shadingNode('condition', asUtility=True, name=part + "_stretchyCnd")
	cmds.setAttr(str(stretchyCnd) + ".operation", 3)


	# connect multiply divide node outputX to condition node first term
	cmds.connectAttr(str(multdiv) + ".outputX", str(stretchyCnd) + ".firstTerm")
	cmds.connectAttr(str(multdiv) + ".outputX", str(stretchyCnd) + ".colorIfTrueR")

	cmds.setAttr(str(stretchyCnd) + ".secondTerm", 1.00)

	cmds.connectAttr(str(stretchyCnd) + ".outColorR", str(start) + ".scaleX")
	cmds.connectAttr(str(stretchyCnd) + ".outColorR", str(stretchybone1) + ".scaleX")


	return startLoc, endLoc, distanceNode



def FKIKSwitch(part, SwitchPath, BIND_list, FKs, IKs, bindConstraints, FK_Controls, IK_Controls, SwitchTranslate):
	print "In FK IK Switch"

	# create an IK / FK switch
	switchCtl = []
	switchName = part + "FkIk_switch"

	# import the switch control and rename
	cmds.file(SwitchPath, i=True)
	cmds.select("switch_curve", r=True)
	cmds.rename(switchName)

	# add the curve to the switchCtl list
	switchCtl.append(cmds.ls(sl=True))

	# point constrain to snap it in place and delete the constraint
	switch_pctemp = cmds.pointConstraint(IK_Controls[0][0], switchCtl[0], mo=False)
	cmds.delete(switch_pctemp)

	# place the switch controller and freezes transformation
	cmds.xform(switchCtl[0], r=True, t=(SwitchTranslate), ro=(90, 0, 0), s=(0.5, 0.5, 0.5))
	cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)

	# parent constrains the switch control
	cmds.parentConstraint(BIND_list[2], switchCtl[0], mo=True)

	# add a switch attribute
	cmds.addAttr(ln="switch", at="enum", en="FK:IK", k=True)


	# sets the constraints to switch from FK to IK with the switch control
	x = 0
	for each in bindConstraints:
		constr_IK = str(each)[3:len(each)-3] + "." + IKs[x] + "W1"
		constr_FK = str(each)[3:len(each)-3] + "." + FKs[x] + "W0"

		cmds.connectAttr(switchName + ".switch", constr_IK)
		reverseN = cmds.createNode("reverse", n=str(BIND_list[x]) + "_reverseNode")
		cmds.connectAttr(switchName + ".switch", reverseN + ".inputX")
		cmds.connectAttr(reverseN+ ".outputX", constr_FK)

		x += 1
		cmds.select(cl=True)



	# set the visibility
	cmds.connectAttr(switchName + ".switch", str(IK_Controls[0][0][0]) + ".visibility")
	cmds.connectAttr(switchName + ".switch", str(IK_Controls[1][0][0]) + ".visibility")

	VizReverse = cmds.createNode("reverse", n = part + "_FK_visibility_reverseNode")
	cmds.connectAttr(switchName + ".switch", str(part) + "_FK_visibility_reverseNode.inputX")
	cmds.connectAttr(str(part) + "_FK_visibility_reverseNode.outputX", str(FK_Controls[0])[3:len(FK_Controls[0])-3] + ".visibility")


	# locks and hides translate channels for the switch
	cmds.setAttr(switchName+".tx", lock=True, keyable=False, channelBox=False)
	cmds.setAttr(switchName+".ty", lock=True, keyable=False, channelBox=False)
	cmds.setAttr(switchName+".tz", lock=True, keyable=False, channelBox=False)

	# locks and hides rotate channels for the switch
	cmds.setAttr(switchName+".rx", lock=True, keyable=False, channelBox=False)
	cmds.setAttr(switchName+".ry", lock=True, keyable=False, channelBox=False)
	cmds.setAttr(switchName+".rz", lock=True, keyable=False, channelBox=False)

	# locks and hides scale channels for the switch
	cmds.setAttr(switchName+".sx", lock=True, keyable=False, channelBox=False)
	cmds.setAttr(switchName+".sy", lock=True, keyable=False, channelBox=False)
	cmds.setAttr(switchName+".sz", lock=True, keyable=False, channelBox=False)

	# locks and hides visibility channel
	cmds.setAttr(switchName+".visibility", lock=True, keyable=False, channelBox=False)

	if part.rpartition("_")[2] == "Arm":
		cmds.setAttr(switchCtl[0][0] + ".switch", 0)
	elif part.rpartition("_")[2] == "Leg":
		cmds.setAttr(switchCtl[0][0] + ".switch", 1)


	return switchCtl


def CleanUp(FK_Controls, IK_Controls, BIND_Joints, FK_Joints, IK_Joints, part, FKIKSwitch, Stretchy):
	print "In Rig Clean Up"
	print IK_Controls
	print IK_Controls[1][0][0]

	for each in FK_Controls:
		# locks and hides translate channels
		cmds.setAttr(str(each[0]) + ".tx", lock=True, keyable=False, channelBox=False)
		cmds.setAttr(str(each[0]) + ".ty", lock=True, keyable=False, channelBox=False)
		cmds.setAttr(str(each[0]) + ".tz", lock=True, keyable=False, channelBox=False)

		# locks and hides scale channels
		cmds.setAttr(str(each[0]) + ".sx", lock=True, keyable=False, channelBox=False)
		cmds.setAttr(str(each[0]) + ".sy", lock=True, keyable=False, channelBox=False)
		cmds.setAttr(str(each[0]) + ".sz", lock=True, keyable=False, channelBox=False)

		# locks and hides visibility channel
		cmds.setAttr(str(each[0]) + ".visibility", lock=True, keyable=False, channelBox=False)


	for each in IK_Controls:
		# locks and hides scale channels for the IK control
		cmds.setAttr(str(each[0][0]) + ".sx", lock=True, keyable=False, channelBox=False)
		cmds.setAttr(str(each[0][0]) + ".sy", lock=True, keyable=False, channelBox=False)
		cmds.setAttr(str(each[0][0]) + ".sz", lock=True, keyable=False, channelBox=False)

		# locks and hides visibility channel for the IK control
		cmds.setAttr(str(each[0][0]) + ".visibility", lock=True, keyable=False, channelBox=False)


	# locks and hides rotate channels for the PV
	cmds.setAttr(IK_Controls[1][0][0] + ".rx", lock=True, keyable=False, channelBox=False)
	cmds.setAttr(IK_Controls[1][0][0] + ".ry", lock=True, keyable=False, channelBox=False)
	cmds.setAttr(IK_Controls[1][0][0] + ".rz", lock=True, keyable=False, channelBox=False)


	# locks and hides scale channels for the IK gimbal control
	cmds.setAttr(str(IK_Controls[0][1][0])+".sx", lock=True, keyable=False, channelBox=False)
	cmds.setAttr(str(IK_Controls[0][1][0])+".sy", lock=True, keyable=False, channelBox=False)
	cmds.setAttr(str(IK_Controls[0][1][0])+".sz", lock=True, keyable=False, channelBox=False)

	# locks and hides visibility channel for the IK gimbal control
	cmds.setAttr(str(IK_Controls[0][1][0])+".visibility", lock=True, keyable=False, channelBox=False)


	# create a null group and parent the Bind, FK and IK joint chains to this group
	skelName = part + "_Skeleton_Grp"
	skel = cmds.group(em=True, name=skelName)
	cmds.parent(BIND_Joints[0], skelName)
	cmds.parent(FK_Joints[0], skelName)
	cmds.parent(IK_Joints[0], skelName)

	# create a null group and parent the controls to this group
	rigName = part + "_Rig_Grp"
	rig = cmds.group(em=True, name=rigName)
	cmds.parent(cmds.listRelatives(FK_Controls[0], parent=True), rigName)
	cmds.parent(cmds.listRelatives(IK_Controls[0][0], parent=True), rigName)
	cmds.parent(cmds.listRelatives(IK_Controls[1][0], parent=True), rigName)
	cmds.parent(FKIKSwitch[0], rigName)

	extrasName = part + "_Extras"
	extras = cmds.group(em=True, name=extrasName)
	cmds.parent(Stretchy[0], extrasName)
	cmds.parent(Stretchy[1], extrasName)
	cmds.parent(Stretchy[2], extrasName)

	mainGrpName = part + "_Grp"
	cmds.group(em=True, name=mainGrpName)
	cmds.parent(skel, mainGrpName)
	cmds.parent(rig, mainGrpName)
	cmds.parent(extras, mainGrpName)


def FootSetUp(IK_Leg_Joints, IK_handle, IK_Controls):
	print "In Foot Setup"
	print IK_Leg_Joints

	# Create the IK handles
	ballIK = cmds.ikHandle(n="ball_ikHandle", sj=IK_Leg_Joints[3], ee=IK_Leg_Joints[5], sol="ikRPsolver")
	toeIK = cmds.ikHandle(n="toe_ikHandle", sj=IK_Leg_Joints[5], ee=IK_Leg_Joints[6], sol="ikRPsolver")


	# Create empty groups
	footLiftGrp = cmds.group(empty=True, name="FootLift_Grp")
	pctemp = cmds.pointConstraint(IK_Leg_Joints[3], footLiftGrp)
	cmds.delete(pctemp)
	cmds.makeIdentity(footLiftGrp, apply=True, t=1, r=1, s=1)


	ballPivGrp = cmds.group(empty=True, name="BallPiv_Grp")
	pctemp = cmds.pointConstraint(IK_Leg_Joints[5], ballPivGrp)
	cmds.delete(pctemp)
	cmds.makeIdentity(ballPivGrp, apply=True, t=1, r=1, s=1)

	heelPivGrp = cmds.group(empty=True, name="HeelPiv_Grp")
	pctemp = cmds.pointConstraint(IK_Leg_Joints[4], heelPivGrp)
	cmds.delete(pctemp)
	cmds.makeIdentity(heelPivGrp, apply=True, t=1, r=1, s=1)

	toePivGrp = cmds.group(empty=True, name="ToePiv_Grp")
	pctemp = cmds.pointConstraint(IK_Leg_Joints[6], toePivGrp)
	cmds.delete(pctemp)
	cmds.makeIdentity(toePivGrp, apply=True, t=1, r=1, s=1)

	ankleLiftGrp = cmds.group(empty=True, name="AnkleLift_Grp")
	pctemp = cmds.pointConstraint(IK_Leg_Joints[5], ankleLiftGrp)
	cmds.delete(pctemp)
	cmds.makeIdentity(ankleLiftGrp, apply=True, t=1, r=1, s=1)



	cmds.parent(ballPivGrp, footLiftGrp)
	cmds.parent(heelPivGrp, ballPivGrp)
	cmds.parent(toePivGrp, heelPivGrp)
	cmds.parent(ankleLiftGrp, toePivGrp)
	cmds.parent(toeIK[0], toePivGrp)
	cmds.parent(ballIK[0], ankleLiftGrp)
	cmds.parent(IK_handle[0], ankleLiftGrp)

	cmds.parent(footLiftGrp, IK_Controls[0][1])



	# Set up connections for IK foot attriutes


	# Toe Pivot
	toemultdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name="ToePiv_MultDiv")
	cmds.setAttr(str(toemultdiv) + ".operation", 1)
	cmds.connectAttr(IK_Controls[0][0][0] + ".toePivot", str(toemultdiv) + ".input1X")
	cmds.setAttr(str(toemultdiv) + ".input2X", 6)
	cmds.connectAttr(str(toemultdiv) + ".outputX", str(toePivGrp) + ".ry")

	# Ball Pivot
	ballmultdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name="BallPiv_MultDiv")
	cmds.setAttr(str(ballmultdiv) + ".operation", 1)
	cmds.connectAttr(IK_Controls[0][0][0] + ".ballPivot", str(ballmultdiv) + ".input1X")
	cmds.setAttr(str(ballmultdiv) + ".input2X", 3)
	cmds.connectAttr(str(ballmultdiv) + ".outputX", str(ballPivGrp) + ".ry")

	# Heel Pivot
	footmultdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name="HeelPiv_MultDiv")
	cmds.setAttr(str(footmultdiv) + ".operation", 1)
	cmds.connectAttr(IK_Controls[0][0][0] + ".heelPivot", str(footmultdiv) + ".input1X")
	cmds.setAttr(str(footmultdiv) + ".input2X", 6)
	cmds.connectAttr(str(footmultdiv) + ".outputX", str(heelPivGrp) + ".ry")



"""



Heel Pivot -10			HeelPiv_Grp ry -60
Heel PIvot 0 			HeelPiv_Grp ry 0
Heel PIvot 10			HeelPiv_Grp ry 60			


"""