"""
Script: Rig_Utils
Author: Wini Wang	wini@winsi3d.com
Description: Builds Rig
"""

import maya.cmds as cmds
import Maya.Modules.Layout.WW_Hinge_Lyt as Hinge_Lyt
reload(Hinge_Lyt)
import Maya.System.WW_Joint_Utils as Joint_Utils
reload(Joint_Utils)


def createIK(side, part, IKstartJoint, IKendJoint):
	print "In Create IK"

	IKName = side + part + "_ikHandle"
	IK_handle = cmds.ikHandle(n=IKName, sj=IKstartJoint, ee=IKendJoint, sol="ikRPsolver")
	cmds.select(cl=True)

	return IK_handle



def constrainFKIK(BindJoints, FKJoints, IKJoints):
	print "In Constrain FK IK Joints"

	# constrain the IK and FK joint chains to the BIND chain
	x = 0
	bindConstraints = []
	for eachJoint in BindJoints:
		bindConstraints.append(cmds.parentConstraint(FKJoints[x], IKJoints[x], BindJoints[x], mo=True))
		x += 1

	# hides the FK and IK arm joints
	cmds.setAttr(str(FKJoints[0]) + ".visibility", False)
	cmds.setAttr(str(IKJoints[0]) + ".visibility", False)


	return bindConstraints


def createFKControls(part, FK_Joints):
	print "In Create FK Controls"

	# create circle controllers for the FK chain
	circleCtl = []
	circleCtlGrp = []
	x = 0


	for eachJoint in FK_Joints:

		# set the name here
		FKname = str(FK_Joints[x])[:len(FK_Joints[x])-6]

		# create the controller
		circleCtl.append(cmds.circle(sections=8, ch=False, n=FKname + "_CTRL"))
		
		# rotates the joint 90 degrees in y and freeze transformations
		cmds.xform(r=True, ro=(0, 90, 0), s=(0.5, 0.5, 0.5))
		cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)

		# groups the controller to itself, and renames
		circleCtlGrp.append(cmds.group(n=FKname + "_CTRL_GRP"))

		#parent constrains the group to the joint to place it in the correct place, and deletes the constraint
		fk_pctemp = cmds.parentConstraint(FK_Joints[x], circleCtlGrp[x], mo = False)
		cmds.delete(fk_pctemp)

		# orient constrains the joint to the controller
		cmds.orientConstraint(circleCtl[x], FK_Joints[x], mo = True)


		x += 1


	y = 0

	# parents the controls and groups up the hierarchy

	for eachGroup in circleCtlGrp:
		cmds.parent(circleCtlGrp[y+1], circleCtl[y])
		y += 1
		if y == len(circleCtlGrp)-1:
			break



	x = 0



	handCtl = []
	handCtlGrp = []




	return circleCtl




def createIKControls(side, part, path, IK_handle, PVpath, PVtranslate):
	print "In Create IK Controls"

	Ctl = []
	CtlGrp = []

	# Find the IK effector joint
	IKEffectorJnt = cmds.listConnections(IK_handle[0][1])

	# Find the PV joint from the effector joint
	PVJoint = cmds.listRelatives(IKEffectorJnt[1], parent=True)
	

	"""
	Controls
	"""

	# import the cube control, rename, and add it to Ctl list
	cmds.file(path, i=True)
	cmds.select("curve1", r=True)
	cmds.rename(side + part + "_IK_CTRL")
	Ctl.append(cmds.ls(sl=True))

	# duplicate the curve to create the gimbal control, and rename
	Ctl.append(cmds.duplicate(n=side + part + "_IK_gimbal_CTRL", ))
	cmds.scale(0.8, 0.8, 0.8)
	cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)

	# parent the gimbal control to the main control
	cmds.parent(Ctl[1], Ctl[0])

	# select the controller
	cmds.select(Ctl[0], r=True)
	
	# groups the curve to itself
	CtlGrp.append(cmds.group(n=side + part + "_IK_CTRL_Grp"))


	# parent constrain the group to the joint to place get the translations and rotations from the joint, and deletes the constraint
	if part.rpartition("_")[2] == "Arm":
		ik_pctemp = cmds.parentConstraint(IKEffectorJnt[1], CtlGrp, mo=False)
		cmds.delete(ik_pctemp)
		print CtlGrp[0]
		print "sehfsefliehruishelirubfsefbs"
		if side == "R_":
			cmds.setAttr( "R_Arm_IK_CTRL_Grp.rotateX", 0 )

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
	cmds.parent(IK_handle[0][0], Ctl[1])
	cmds.parent(IK_handle[1][0], Ctl[1])


	"""
	Pole Vector
	"""

	# create a pole vector control
	PV = []
	PVGrp = []

	# import pole vector control and rename
	cmds.file(PVpath, i=True)
	cmds.select("PVcurve", r=True)
	cmds.rename(side + part + "_PV")

	# rotate the joint 90 degrees in x and scale down
	cmds.xform(r=True, ro=(-90, 0, 0), s=(0.2, 0.2, 0.2))

	# group it to itself
	PV.append(cmds.ls(sl=True))
	PVGrp.append(cmds.group(n=side + part + "_PV_Grp"))

	# point constrain to snap it to the elbow, and delete the constraint
	pv_pctemp = cmds.pointConstraint(PVJoint[0], PVGrp[0], mo=False)
	cmds.delete(pv_pctemp)

	# move it back in space and freeze transformations
	cmds.xform(PV[0], r=True, t=(PVtranslate))
	cmds.select(PV[0], r=True)
	cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)

	# creates the pole vector constraint
	cmds.poleVectorConstraint(PV[0], IK_handle[0][0])
	

	return Ctl, PV



def createStretchy(side, part, start, end, stretchybone1, stretchybone2, IK_Controls):
	print "In Create Stretchy IK"

	# find the positions of the start and end points
	startPos = cmds.xform(start, q=True, translation=True, worldSpace=True)
	endPos = cmds.xform(end[0], q=True, translation=True, worldSpace=True)


	# create locators at these positions and point constrain them to the start joint and end IK handle control
	startLoc = cmds.spaceLocator(n=side + part + "_DistDim_Start_LOC")[0]
	cmds.pointConstraint(start, startLoc, mo=False)

   	endLoc = cmds.spaceLocator(n=side + part + "_DistDim_End_LOC")[0]
   	cmds.pointConstraint(end[0], endLoc, mo=False)


   	# create the distance dimension shape node
   	distanceNode = cmds.createNode("distanceDimShape", n="%s_%s_distance" % (startLoc,endLoc))


   	# connect the start locator and end locator to the distance dimension startPoint and endPoint
	cmds.connectAttr(startLoc + "Shape.worldPosition[0]", distanceNode + ".startPoint")
	cmds.connectAttr(endLoc + "Shape.worldPosition[0]", distanceNode + ".endPoint")   	
   	

	# create a multiply divide node
	multdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name=side + part + "_stretchyMultDiv")
	cmds.setAttr(str(multdiv) + ".operation", 2)


	# connect the distance dimension shape node to the multiply divide input X
	cmds.connectAttr(str(distanceNode)+".distance", str(multdiv) + ".input1X")


	# find the length when the arm is fully stretched and put value into multiply divide node inpux2X
	pos1 = cmds.joint(stretchybone1, q=True, r=True, p=True)
	pos2 = cmds.joint(stretchybone2, q=True, r=True, p=True)

	restLength = pos1[0] + pos2[0]
	cmds.setAttr(str(multdiv) + ".input2X", abs(restLength))
	
	# create a condition node
	stretchyCnd = cmds.shadingNode('condition', asUtility=True, name=side + part + "_stretchyCnd")
	cmds.setAttr(str(stretchyCnd) + ".operation", 3)


	# connect multiply divide node outputX to condition node first term
	cmds.connectAttr(str(multdiv) + ".outputX", str(stretchyCnd) + ".firstTerm")
	cmds.connectAttr(str(multdiv) + ".outputX", str(stretchyCnd) + ".colorIfTrueR")

	cmds.setAttr(str(stretchyCnd) + ".secondTerm", 1.00)

	cmds.connectAttr(str(stretchyCnd) + ".outColorR", str(start) + ".scaleX")
	cmds.connectAttr(str(stretchyCnd) + ".outColorR", str(stretchybone1) + ".scaleX")

	print IK_Controls

	return startLoc, endLoc, distanceNode



def FKIKSwitch(side, part, SwitchPath, BIND_list, FKs, IKs, bindConstraints, FK_Controls, IK_Controls, SwitchTranslate):
	print "In FK IK Switch"

	# create an IK / FK switch
	switchCtl = []
	switchName = side + part + "FkIk_switch"

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
	cmds.parentConstraint(BIND_list[3], switchCtl[0], mo=True)

	# add a switch attribute
	cmds.addAttr(ln="switch", at="enum", en="FK:IK", k=True)


	# sets the constraints to switch from FK to IK with the switch control
	x = 0
	for each in bindConstraints:
		constr_IK = str(each)[3:len(each)-3] + "." + IKs[x] + "W1"
		constr_FK = str(each)[3:len(each)-3] + "." + FKs[x] + "W0"

		cmds.connectAttr(switchName + ".switch", constr_IK)
		reverseN = cmds.createNode("reverse", n=side + str(BIND_list[x]) + "_reverseNode")
		cmds.connectAttr(switchName + ".switch", reverseN + ".inputX")
		cmds.connectAttr(reverseN+ ".outputX", constr_FK)

		x += 1
		cmds.select(cl=True)



	# set the visibility
	cmds.connectAttr(switchName + ".switch", str(IK_Controls[0][0][0]) + ".visibility")
	cmds.connectAttr(switchName + ".switch", str(IK_Controls[1][0][0]) + ".visibility")

	VizReverse = cmds.createNode("reverse", n = side + part + "_FK_visibility_reverseNode")
	cmds.connectAttr(switchName + ".switch", str(VizReverse) + ".inputX")
	cmds.connectAttr(str(side) + str(part) + "_FK_visibility_reverseNode.outputX", str(FK_Controls[0])[3:len(FK_Controls[0])-3] + ".visibility")


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


def CleanUp(FK_Controls, IK_Controls, BIND_Joints, FK_Joints, IK_Joints, side, part, FKIKSwitch, Stretchy):
	print "In Rig Clean Up"

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
	cmds.setAttr(str(IK_Controls[0][1][0]) + ".sx", lock=True, keyable=False, channelBox=False)
	cmds.setAttr(str(IK_Controls[0][1][0]) + ".sy", lock=True, keyable=False, channelBox=False)
	cmds.setAttr(str(IK_Controls[0][1][0]) + ".sz", lock=True, keyable=False, channelBox=False)

	# locks and hides visibility channel for the IK gimbal control
	cmds.setAttr(str(IK_Controls[0][1][0])+".visibility", lock=True, keyable=False, channelBox=False)


	# create a null group and parent the Bind, FK and IK joint chains to this group
	skelName = side + part + "_Skeleton_Grp"
	skel = cmds.group(em=True, name=skelName)
	cmds.parent(BIND_Joints[0], skelName)
	cmds.parent(FK_Joints[0], skelName)
	cmds.parent(IK_Joints[0], skelName)

	# create a null group and parent the controls to this group
	rigName = side + part + "_Rig_Grp"
	rig = cmds.group(em=True, name=rigName)
	cmds.parent(cmds.listRelatives(FK_Controls[0], parent=True), rigName)
	cmds.parent(cmds.listRelatives(IK_Controls[0][0], parent=True), rigName)
	cmds.parent(cmds.listRelatives(IK_Controls[1][0], parent=True), rigName)
	cmds.parent(FKIKSwitch[0], rigName)

	extrasName = side + part + "_Extras"
	extras = cmds.group(em=True, name=extrasName)
	cmds.parent(Stretchy[0], extrasName)
	cmds.parent(Stretchy[1], extrasName)
	cmds.parent(Stretchy[2], extrasName)
	cmds.setAttr(str(extras) + ".visibility", 0)

	mainGrpName = side + part + "_Grp"
	cmds.group(em=True, name=mainGrpName)
	cmds.parent(skel, mainGrpName)
	cmds.parent(rig, mainGrpName)
	cmds.parent(extras, mainGrpName)




def FootSetUp(IK_Leg_Joints, IK_handle, IK_Controls):
	print "In Foot Setup"

	# Create the IK handles
	ballIK = cmds.ikHandle(n="ball_ikHandle", sj=IK_Leg_Joints[3], ee=IK_Leg_Joints[5], sol="ikSCsolver")
	toeIK = cmds.ikHandle(n="toe_ikHandle", sj=IK_Leg_Joints[5], ee=IK_Leg_Joints[6], sol="ikSCsolver")


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

	toeWiggleGrp = cmds.group(empty=True, name="ToeWiggle_Grp")
	pctemp = cmds.pointConstraint(IK_Leg_Joints[5], toeWiggleGrp)
	cmds.delete(pctemp)
	cmds.makeIdentity(toeWiggleGrp, apply=True, t=1, r=1, s=1)

	FootRockOuterGrp = cmds.group(empty=True, name="Outer_Foot_Rock_Grp")
	pctemp = cmds.pointConstraint("*outer_foot_loc", FootRockOuterGrp)
	cmds.delete(pctemp)
	cmds.makeIdentity(FootRockOuterGrp, apply=True, t=1, r=1, s=1)

	FootRockInnerGrp = cmds.group(empty=True, name="Inner_Foot_Rock_Grp")
	pctemp = cmds.pointConstraint("*inner_foot_loc", FootRockInnerGrp)
	cmds.delete(pctemp)
	cmds.makeIdentity(FootRockInnerGrp, apply=True, t=1, r=1, s=1)


	cmds.parent(FootRockInnerGrp, FootRockOuterGrp)
	cmds.parent(FootRockOuterGrp, ballPivGrp)
	cmds.parent(heelPivGrp, FootRockInnerGrp)
	cmds.parent(toePivGrp, heelPivGrp)
	cmds.parent(ankleLiftGrp, toePivGrp)
	cmds.parent(toeIK[0], toeWiggleGrp)
	cmds.parent(toeWiggleGrp, toePivGrp)
	cmds.parent(ballIK[0], ankleLiftGrp)
	cmds.parent(IK_handle[0], ankleLiftGrp)

	cmds.parent(ballPivGrp, IK_Controls[0][1])



	# Set up connections for IK foot attributes

	# Foot Roll (ball)
	footrollclamp = cmds.shadingNode('clamp', asUtility=True, name="FootRoll_Clamp")
	footrollmultdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name="FootRoll_MultDiv")
	cmds.connectAttr(IK_Controls[0][0][0] + ".footRoll", str(footrollclamp) + ".inputR")
	cmds.connectAttr(str(footrollclamp) + ".outputR", str(footrollmultdiv) + ".input1X")
	cmds.connectAttr(str(footrollmultdiv) + ".outputX", str(heelPivGrp) + ".rx")
	cmds.setAttr(str(footrollclamp) + ".minR", -10)
	cmds.setAttr(str(footrollclamp) + ".maxR", 0)
	cmds.setAttr(str(footrollmultdiv) + ".operation", 1)
	cmds.setAttr(str(footrollmultdiv) + ".input2X", 6)


	# Foot Roll (heel)
	heelrollclamp = cmds.shadingNode('clamp', asUtility=True, name="HeelRoll_Clamp")
	heelrollmultdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name="HeelRoll_MultDiv")
	cmds.connectAttr(IK_Controls[0][0][0] + ".footRoll", str(heelrollclamp) + ".inputR")
	cmds.connectAttr(str(heelrollclamp) + ".outputR", str(heelrollmultdiv) + ".input1X")
	cmds.connectAttr(str(heelrollmultdiv) + ".outputX", str(ankleLiftGrp) + ".rx")
	cmds.setAttr(str(heelrollclamp) + ".minR", 0)
	cmds.setAttr(str(heelrollclamp) + ".maxR", 10)
	cmds.setAttr(str(heelrollmultdiv) + ".operation", 1)
	cmds.setAttr(str(heelrollmultdiv) + ".input2X", 9)


	# Toe Roll
	toerollmultdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name="ToeRoll_MultDiv")
	cmds.setAttr(str(toerollmultdiv) + ".operation", 1)
	cmds.connectAttr(IK_Controls[0][0][0] + ".toeRoll", str(toerollmultdiv) + ".input1X")
	cmds.setAttr(str(toerollmultdiv) + ".input2X", 8)
	cmds.connectAttr(str(toerollmultdiv) + ".outputX", str(toePivGrp) + ".rx")


	# Toe Wiggle
	toewigglemultdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name="ToeWiggle_MultDiv")
	cmds.setAttr(str(toewigglemultdiv) + ".operation", 1)
	cmds.connectAttr(IK_Controls[0][0][0] + ".toeWiggle", str(toewigglemultdiv) + ".input1X")
	cmds.setAttr(str(toewigglemultdiv) + ".input2X", 7)
	cmds.connectAttr(str(toewigglemultdiv) + ".outputX", str(toeWiggleGrp) + ".rx")


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


	# Foot Rock #
	footrockouterclamp = cmds.shadingNode('clamp', asUtility=True, name="FootRockOuter_Clamp")
	cmds.setAttr(str(footrockouterclamp) + ".minR", 0)
	cmds.setAttr(str(footrockouterclamp) + ".maxR", 10)
	footrockoutermultdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name="FootRockOuter_MultDiv")
	cmds.setAttr(str(footrockoutermultdiv) + ".operation", 1)
	cmds.connectAttr(IK_Controls[0][0][0] + ".footRock", str(footrockouterclamp) + ".inputR")
	cmds.connectAttr(str(footrockouterclamp) + ".outputR", str(footrockoutermultdiv) + ".input1X")
	cmds.setAttr(str(footrockoutermultdiv) + ".input2X", -9)
	cmds.connectAttr(str(footrockoutermultdiv) + ".outputX", str(FootRockOuterGrp) + ".rz")


	# Foot Rock #
	footrockinnerclamp = cmds.shadingNode('clamp', asUtility=True, name="FootRockInner_Clamp")
	cmds.setAttr(str(footrockinnerclamp) + ".minR", -10)
	cmds.setAttr(str(footrockinnerclamp) + ".maxR", 0)
	footrockinnermultdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name="FootRockInner_MultDiv")
	cmds.setAttr(str(footrockinnermultdiv) + ".operation", 1)
	cmds.connectAttr(IK_Controls[0][0][0] + ".footRock", str(footrockinnerclamp) + ".inputR")
	cmds.connectAttr(str(footrockinnerclamp) + ".outputR", str(footrockinnermultdiv) + ".input1X")
	cmds.setAttr(str(footrockinnermultdiv) + ".input2X", -9)
	cmds.connectAttr(str(footrockinnermultdiv) + ".outputX", str(FootRockInnerGrp) + ".rz")


def HandSetUp(path, fingerControls, Hand_Joints, FKIKSwitch):
	print "In Hand Set Up"

	# create circle controllers for the FK chain
	fingerCtrl = []
	fingerCtrlGrp = []
	fingerCtrlSDKGrp = []

	x = 0


	for eachJoint in fingerControls:

		# set the name here
		FKname = str(fingerControls[x])[:len(fingerControls[x])-6]

		# create the controller
		fingerCtrl.append(cmds.circle(sections=8, ch=False, n=FKname + "_CTRL"))
		
		# rotates the joint 90 degrees in y and freeze transformations
		cmds.xform(r=True, ro=(0, 90, 0), s=(0.5, 0.5, 0.5))
		cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)

		# groups the controller to itself, and renames
		fingerCtrlSDKGrp.append(cmds.group(n=FKname + "_CTRL_Grp"))
		fingerCtrlGrp.append(cmds.group(n=FKname + "_zero_rg"))

		#parent constrains the group to the joint to place it in the correct place, and deletes the constraint
		fk_pctemp = cmds.parentConstraint(fingerControls[x], fingerCtrlGrp[x], mo = False)
		cmds.delete(fk_pctemp)

		# orient constrains the joint to the controller
		cmds.orientConstraint(fingerCtrl[x], fingerControls[x], mo = True)


		x += 1




	y = 0


	# parents the controls and groups up the hierarchy

	for eachGroup in fingerCtrlGrp:
		cmds.parent(fingerCtrlGrp[y+1], fingerCtrl[y])
		y += 1
		if y == len(fingerCtrlGrp)-1:
			break

	cmds.select(cl=True)

	
	
	fingerGrpName = fingerCtrlGrp[0].partition("_")[0] + "_Fingers_zero_rg"


	fingerGrp = cmds.group(n=fingerGrpName, empty=True)
	pc = cmds.parentConstraint(Hand_Joints[0], fingerGrp)
	cmds.delete(pc)


	cmds.select(fingerCtrlGrp[0], r=True)
	cmds.select(fingerCtrlGrp[3], add=True)
	cmds.select(fingerCtrlGrp[6], add=True)
	cmds.select(fingerCtrlGrp[9], add=True)
	cmds.select(fingerCtrlGrp[12], add=True)

	TopGrp = cmds.ls(sl=True)

	for each in TopGrp:
		cmds.parent(each, fingerGrp)


	cmds.parentConstraint(Hand_Joints[0], fingerGrp)

	print fingerCtrlSDKGrp

	# Add attributes for fingers
	cmds.addAttr(FKIKSwitch[0], longName="thumb", shortName="Thumb", attributeType="enum", enumName="---", k=True)
	cmds.addAttr(FKIKSwitch[0], longName="thumb_01", shortName="Thumb_01", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.addAttr(FKIKSwitch[0], longName="thumb_02", shortName="Thumb_02", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.addAttr(FKIKSwitch[0], longName="thumb_03", shortName="Thumb_03", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.setAttr(str(FKIKSwitch[0][0]) + ".thumb", lock=True)

	cmds.addAttr(FKIKSwitch[0], longName="index", shortName="Index", attributeType="enum", enumName="---", k=True)
	cmds.addAttr(FKIKSwitch[0], longName="index_01", shortName="Index_01", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.addAttr(FKIKSwitch[0], longName="index_02", shortName="Index_02", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.addAttr(FKIKSwitch[0], longName="index_03", shortName="Index_03", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.setAttr(str(FKIKSwitch[0][0]) + ".index", lock=True)

	cmds.addAttr(FKIKSwitch[0], longName="middle", shortName="Middle", attributeType="enum", enumName="---", k=True)
	cmds.addAttr(FKIKSwitch[0], longName="middle_01", shortName="Middle_01", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.addAttr(FKIKSwitch[0], longName="middle_02", shortName="Middle_02", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.addAttr(FKIKSwitch[0], longName="middle_03", shortName="Middle_03", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.setAttr(str(FKIKSwitch[0][0]) + ".middle", lock=True)

	cmds.addAttr(FKIKSwitch[0], longName="ring", shortName="Ring", attributeType="enum", enumName="---", k=True)
	cmds.addAttr(FKIKSwitch[0], longName="ring_01", shortName="Ring_01", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.addAttr(FKIKSwitch[0], longName="ring_02", shortName="Ring_02", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.addAttr(FKIKSwitch[0], longName="ring_03", shortName="Ring_03", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.setAttr(str(FKIKSwitch[0][0]) + ".ring", lock=True)

	cmds.addAttr(FKIKSwitch[0], longName="pinky", shortName="Pinky", attributeType="enum", enumName="---", k=True)
	cmds.addAttr(FKIKSwitch[0], longName="pinky_01", shortName="Pinky_01", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.addAttr(FKIKSwitch[0], longName="pinky_02", shortName="Pinky_02", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.addAttr(FKIKSwitch[0], longName="pinky_03", shortName="Pinky_03", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.setAttr(str(FKIKSwitch[0][0]) + ".pinky", lock=True)

	cmds.addAttr(FKIKSwitch[0], longName="spread", shortName="Spread", attributeType="enum", enumName="---", k=True)
	cmds.addAttr(FKIKSwitch[0], longName="thumbSpread", shortName="ThumbSpread", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.addAttr(FKIKSwitch[0], longName="indexSpread", shortName="IndexSpread", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.addAttr(FKIKSwitch[0], longName="middleSpread", shortName="MiddleSpread", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.addAttr(FKIKSwitch[0], longName="ringSpread", shortName="RingSpread", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.addAttr(FKIKSwitch[0], longName="pinkySpread", shortName="PinkySpread", attributeType="float", min=-10, max=10, dv=0, k=True)
	cmds.setAttr(str(FKIKSwitch[0][0]) + ".spread", lock=True)


	# Connect finger curl and spread
	x = 0
	for each in fingerCtrlSDKGrp:
		finger = each.partition("_CTRL")[0]
		fingerAttr = finger.partition("_")[2]
		
		multdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name=finger + "_MultDiv")
		cmds.connectAttr(FKIKSwitch[0][0] + "." + fingerAttr, str(multdiv) + ".input1Z")
		cmds.setAttr(str(multdiv) + ".input2Z", -10)
		cmds.connectAttr(str(multdiv) + ".outputZ", fingerCtrlSDKGrp[x] + ".rz")

		if fingerAttr == "thumb_01":
			multdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name="thumbSpread_MultDiv")
			cmds.connectAttr(FKIKSwitch[0][0] + ".thumbSpread", str(multdiv) + ".input1Y")
			cmds.setAttr(str(multdiv) + ".input2Y", -8)
			cmds.connectAttr(str(multdiv) + ".outputY", fingerCtrlSDKGrp[x] + ".ry")

		if fingerAttr == "index_01":
			multdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name="indexSpread_MultDiv")
			cmds.connectAttr(FKIKSwitch[0][0] + ".indexSpread", str(multdiv) + ".input1Y")
			cmds.setAttr(str(multdiv) + ".input2Y", -6)
			cmds.connectAttr(str(multdiv) + ".outputY", fingerCtrlSDKGrp[x] + ".ry")

		if fingerAttr == "middle_01":
			multdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name="middleSpread_MultDiv")
			cmds.connectAttr(FKIKSwitch[0][0] + ".indexSpread", str(multdiv) + ".input1Y")
			cmds.setAttr(str(multdiv) + ".input2Y", 2)
			cmds.connectAttr(str(multdiv) + ".outputY", fingerCtrlSDKGrp[x] + ".ry")

		if fingerAttr == "ring_01":
			multdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name="ringSpread_MultDiv")
			cmds.connectAttr(FKIKSwitch[0][0] + ".ringSpread", str(multdiv) + ".input1Y")
			cmds.setAttr(str(multdiv) + ".input2Y", 6)
			cmds.connectAttr(str(multdiv) + ".outputY", fingerCtrlSDKGrp[x] + ".ry")

		if fingerAttr == "pinky_01":
			multdiv = cmds.shadingNode('multiplyDivide', asUtility=True, name="pinkySpread_MultDiv")
			cmds.connectAttr(FKIKSwitch[0][0] + ".pinkySpread", str(multdiv) + ".input1Y")
			cmds.setAttr(str(multdiv) + ".input2Y", 10)
			cmds.connectAttr(str(multdiv) + ".outputY", fingerCtrlSDKGrp[x] + ".ry")


		x += 1




def SpineSetUp(BIND_Spine_Joints, path, FK_Spine_Joints):
	print "In Spine Set Up using a ribbon spine"

	JntPos = []
	x = 0
	for each in BIND_Spine_Joints:
		JntPos.append(cmds.xform(BIND_Spine_Joints[x], q=True, translation=True))
		x += 1

	RibbonLen = JntPos[0][0] + JntPos[1][0] + JntPos[2][0] + JntPos[3][0] + JntPos[4][0]
	RibbonLen = RibbonLen + (RibbonLen/5)


	# Create group for ribbon rig
	ribbonRigGrp = cmds.group(em=True, n=("Ribbon_Spine_Grp"))

	# Create group for follicles
	folGrp = cmds.group(em=True, n="Spine_Follicles_Grp")

	
	# Create nurbs plane
	ribbonPlane = cmds.nurbsPlane (n=("Ribbon_Spine_Plane"), p=[0, 0, 0], ax= [0, 0 ,1], w=1 ,lr=RibbonLen ,d=3, u=1, v=5, ch=0)
	cmds.rebuildSurface(rebuildType=0, direction=0, spansU=1, spansV=5, degreeU=1, degreeV=3, keepRange=0)

	cmds.parent(ribbonPlane, ribbonRigGrp)

	pc = cmds.pointConstraint(BIND_Spine_Joints[2], ribbonPlane, mo=False)
	cmds.delete(pc)
	
	# Get the shape node
	ribbonPlaneShape = cmds.listRelatives(ribbonPlane, c=True, s=True)


	folList = []
	IK_Spine_Joints = []
	x=0

	# Create a list for the follicles
	spineList = [BIND_Spine_Joints[0], BIND_Spine_Joints[1], BIND_Spine_Joints[2], BIND_Spine_Joints[3], BIND_Spine_Joints[4]]


	# Creates a follicle for each of the spine joints
	# Creates a joint for each follicle and parents it under the follicles
	for each in spineList:
		follicle = cmds.createNode("follicle", n=each + "_follicleShape")
		follicleTransform = cmds.listRelatives(follicle, p=True)
		
		cmds.connectAttr(ribbonPlaneShape[0] + ".local", follicle + ".inputSurface")
		cmds.connectAttr(ribbonPlaneShape[0] + ".worldMatrix[0]", follicle + ".inputWorldMatrix")
		cmds.connectAttr(follicle + ".outRotate", follicleTransform[0] + ".rotate")
		cmds.connectAttr(follicle + ".outTranslate", follicleTransform[0] + ".translate")

		#position the follicles along the plane
		cmds.setAttr(follicle + ".parameterU", 0.5)
		vSpanHeight = ((x+1.0)/5.0) - .1
		cmds.setAttr(follicle + ".parameterV", vSpanHeight)

		cmds.parent(follicleTransform[0], folGrp)
		folList.append(follicle)


		jntName = "IK_" + str(each).partition("_")[2]
		jnt = cmds.joint(n=jntName)
		pc = cmds.parentConstraint(follicle, jnt)
		cmds.delete(pc)

		cmds.makeIdentity(jnt, apply=True, t=True, r=True, s=True, n=False)

		cmds.setAttr(str(jnt)+".jointOrientZ", 90)

		IK_Spine_Joints.append(cmds.ls(sl=True))

		x+=1

	
	cmds.select(cl=True)



	# Creates controls to drive the joints
	# import the cube controls and circle control, rename, and add it to Ctl list
	Ctl = []
	CtlGrp = []

	cmds.file(path, i=True)
	cmds.select("curve1", r=True)
	cmds.rename("Hips_CTRL")
	Ctl.append(cmds.ls(sl=True))
	cmds.group(n="Hips_CTRL_zero_rg")
	CtlGrp.append(cmds.ls(sl=True))

	cmds.circle(n="Midriff_CTRL")
	cmds.setAttr("Midriff_CTRL.rotateY", 90)
	cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)

	Ctl.append(cmds.ls(sl=True))
	cmds.group(n="Midriff_CTRL_zero_rg")
	CtlGrp.append(cmds.ls(sl=True))

	cmds.file(path, i=True)
	cmds.select("curve1", r=True)
	cmds.rename("Chest_CTRL")
	Ctl.append(cmds.ls(sl=True))
	cmds.group(n="Chest_CTRL_zero_rg")
	CtlGrp.append(cmds.ls(sl=True))



	# Creates locators to be used as aim constraints
	locHipAim = cmds.spaceLocator(n="HipsAim_LOC")
	cmds.parent(locHipAim, Ctl[0][0])
	locHipUp = cmds.spaceLocator(n="HipsUp_LOC")
	cmds.xform(locHipUp, translation=(0, -1, 0))
	cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)
	cmds.parent(locHipUp, Ctl[0][0])

	locMidAim = cmds.spaceLocator(n="MidriffAim_LOC")
	cmds.parent(locMidAim, Ctl[1][0])
	locMidUp = cmds.spaceLocator(n="MidriffUp_LOC")
	cmds.xform(locMidUp, translation=(0, -1, 0))
	cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)
	cmds.parent(locMidUp, Ctl[1][0])

	locChestAim = cmds.spaceLocator(n="ChestAim_LOC")
	cmds.parent(locChestAim, Ctl[2][0])
	locChestUp = cmds.spaceLocator(n="ChestUp_LOC")
	cmds.xform(locChestUp, translation=(0, -1, 0))
	cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)
	cmds.parent(locChestUp, Ctl[2][0])



	# Place the ribbon spine controls
	pc = cmds.parentConstraint(spineList[0], CtlGrp[0][0], mo=False)
	cmds.delete(pc)

	pc = cmds.parentConstraint(spineList[2], CtlGrp[1][0], mo=False)
	cmds.delete(pc)

	pc = cmds.parentConstraint(spineList[4], CtlGrp[2][0], mo=False)
	cmds.delete(pc)

	cmds.select(cl=True)


	DriveJnts = []

	# Create the driver for the ribbon spine rig
	TopDrv1 = cmds.joint(n="topDriver_01_rgJnt")
	DriveJnts.append(cmds.ls(sl=True))
	pc = cmds.pointConstraint(spineList[4], TopDrv1, mo=False)
	cmds.delete(pc)

	TopDrv2 = cmds.joint(n="topDriver_02_rgJnt")
	DriveJnts.append(cmds.ls(sl=True))
	pc = cmds.pointConstraint(spineList[3], TopDrv2, mo=False)
	cmds.delete(pc)
	

	cmds.select(cl=True)

	BotDrv1 = cmds.joint(n="bottomDriver_01_rgJnt")
	DriveJnts.append(cmds.ls(sl=True))
	pc = cmds.pointConstraint(spineList[0], BotDrv1, mo=False)
	cmds.delete(pc)

	BotDrv2 = cmds.joint(n="bottomDriver_02_rgJnt")
	DriveJnts.append(cmds.ls(sl=True))
	pc = cmds.pointConstraint(spineList[1], BotDrv2, mo=False)
	cmds.delete(pc)

	cmds.select(cl=True)
	
	MidDrv = cmds.joint(n="midDriver_rgJnt")
	DriveJnts.append(cmds.ls(sl=True))
	pc = cmds.pointConstraint(spineList[2], MidDrv, mo=False)
	cmds.delete(pc)


	for each in DriveJnts:
		print each[0]
		cmds.joint( each[0], e=True, zso=True, oj='xyz', sao = 'yup' )

	cmds.setAttr(str(DriveJnts[1][0])+".jointOrientZ", 0)
	cmds.setAttr(str(DriveJnts[3][0])+".jointOrientZ", 0)
	cmds.setAttr(str(DriveJnts[4][0])+".jointOrientZ", 90)

	cmds.parent(TopDrv1, locChestAim)
	cmds.parent(BotDrv1, locHipAim)
	cmds.parent(MidDrv, locMidAim)

	
	# Create aim constraints
	cmds.aimConstraint( Ctl[2][0], locHipAim, aimVector=(0.0, 1.0, 0.0), upVector=(1.0, 0.0, 0.0), worldUpType="object", worldUpObject=locHipUp[0], mo=True )
	cmds.aimConstraint( Ctl[0][0], locChestAim, aimVector=(0.0, -1.0, 0.0), upVector=(1.0, 0.0, 0.0), worldUpType="object", worldUpObject=locChestUp[0], mo=True )

	# Create point constraint
	cmds.pointConstraint(Ctl[2][0], Ctl[0][0], CtlGrp[1][0])

	# Aim the middle control to the top control
	cmds.aimConstraint(Ctl[2][0], locMidAim, aimVector=(0.0, 1.0, 0.0), upVector=(1.0, 0.0, 0.0), worldUpType="object", worldUpObject=locMidUp[0] )


	# Bind joints
	cmds.skinCluster( ribbonPlane, TopDrv1, BotDrv1, MidDrv )


	# Spine Cleanup
	# constrain the IK and FK joint chains to the BIND chain
	x = 0
	bindConstraints = []
	for eachJoint in BIND_Spine_Joints:
		print eachJoint
		bindConstraints.append(cmds.parentConstraint(FK_Spine_Joints[x], IK_Spine_Joints[x], BIND_Spine_Joints[x], mo=True))
		x += 1

	# hides the FK and IK arm joints
	cmds.setAttr(str(FK_Spine_Joints[0]) + ".visibility", False)
	


	for each in IK_Spine_Joints:
		cmds.setAttr(str(each[0]) + ".visibility", False)

	



