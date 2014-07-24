"""
Script: Arm_Rig
Author: Wini Wang	wini@winsi3d.com
Description: Creates an arm rig
"""

import maya.cmds as cmds
import Maya.System.WW_Joint_Utils as Joint_Utils
reload(Joint_Utils)
import Maya.System.WW_Rig_Utils as Rig_Utils
reload(Rig_Utils)


CLASS_NAME = "Arm_Rig"
TITLE = "Arm_Rig"
DESCRIPTION = "builds an arm rig"


class Arm_Rig:
	def __init__(self):
		print "In Arm Rig"
		self.Arm_Lyt_Check()


	def Arm_Lyt_Check(self, *args):
		locatorInfo = []
		armLocatorInfo = []
		handLocatorInfo = []
		rootLoc = cmds.ls(sl=True)
		print rootLoc
		print rootLoc[0]

		rootCheck = rootLoc[0].rpartition("_")[2]
		print rootCheck

		if rootCheck == "root":
			print "Root is selected"


			rootChildren = cmds.listRelatives(rootLoc, allDescendents = True, type = "transform")
			rootChildren.reverse()

			for each in rootChildren:
				pos = cmds.xform(each, q=True, ws=True, t=True)
				locatorInfo.append([each, pos])

			clavArmLocatorInfo = locatorInfo[0:4]
			armLocatorInfo = locatorInfo[1:4]

			handLocatorInfo = locatorInfo[4:]


			self.Arm_Rig(locatorInfo, clavArmLocatorInfo, armLocatorInfo, handLocatorInfo, rootLoc)


		else:
			return cmds.headsUpMessage("Please Select A Root")



	def Arm_Rig(self, locatorInfo, clavArmLocatorInfo, armLocatorInfo, handLocatorInfo, rootLoc):
		part = "Arm"
		Lside = "L_"
		Rside = "R_"
		skin = "_skJnt"
		rg = "_rgJnt"
		typeIk = "IK_"
		typeFk = "FK_"
		typeNone = ""

		PVtranslate = (0, 0, -10)
		SwitchTranslate = (0, 1, 0)



		"""
		
		----------------------------------------
		This creates the joints on the left side
		----------------------------------------
		
		"""
		
		# creates the Bind, FK, and IK joints
		L_BIND_Arm_Joints = Joint_Utils.BuildJoints(Lside, typeNone, clavArmLocatorInfo, skin)
		L_FK_Arm_Joints = Joint_Utils.BuildJoints(Lside, typeFk, armLocatorInfo, rg)
		L_IK_Arm_Joints = Joint_Utils.BuildJoints(Lside, typeIk, armLocatorInfo, rg)
		L_Hand_Joints = Joint_Utils.BuildJoints(Lside, typeNone, handLocatorInfo, skin)

		# parents the finger joints to the hand joint
		cmds.delete(rootLoc)
		cmds.parent(Lside + "hand" + skin, L_BIND_Arm_Joints[len(L_BIND_Arm_Joints)-1])
		cmds.parent(Lside + "thumb_01" + skin, Lside + "*hand" + skin)
		cmds.parent(Lside + "index_01" + skin, Lside + "hand" + skin)
		cmds.parent(Lside + "middle_01" + skin, Lside + "hand" + skin)
		cmds.parent(Lside + "ring_01" + skin, Lside + "hand" + skin)

		L_thumbJoints = cmds.listRelatives(Lside + "thumb_01" + skin, allDescendents=True)
		L_thumbJoints.append(Lside + "thumb_01" + skin)
		L_thumbJoints.reverse()

		L_indexJoints = cmds.listRelatives(Lside + "index_01" + skin, allDescendents=True)
		L_indexJoints.append(Lside + "index_01" + skin)
		L_indexJoints.reverse()

		L_middleJoints = cmds.listRelatives(Lside + "middle_01" + skin, allDescendents=True)
		L_middleJoints.append(Lside + "middle_01" + skin)
		L_middleJoints.reverse()

		L_ringJoints = cmds.listRelatives(Lside + "ring_01" + skin, allDescendents=True)
		L_ringJoints.append(Lside + "ring_01" + skin)
		L_ringJoints.reverse()

		L_pinkyJoints = cmds.listRelatives(Lside + "pinky_01" + skin, allDescendents=True)
		L_pinkyJoints.append(Lside + "pinky_01" + skin)
		L_pinkyJoints.reverse()


		cmds.select(cl=True)







		"""
		
		------------------------------------------------
		This mirrors the joints across to the right side
		------------------------------------------------
		
		"""

		# mirrors joints across
		R_BIND_Arm_Joints = cmds.mirrorJoint(L_BIND_Arm_Joints[0], mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_") )
		R_Hand_Joints = R_BIND_Arm_Joints[4:]
		R_BIND_Arm_Joints = R_BIND_Arm_Joints[:4]	
	
		R_FK_Arm_Joints = cmds.mirrorJoint(L_FK_Arm_Joints[0], mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_") )
		R_IK_Arm_Joints = cmds.mirrorJoint(L_IK_Arm_Joints[0], mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_") )







		"""
		
		-----------------------------------------
		This creates the arm rig on the left side
		-----------------------------------------
		
		"""

		# creates the IK handle
		L_IK_handle = Rig_Utils.createIK(Lside, part, L_IK_Arm_Joints[0], L_IK_Arm_Joints[2])

		# constrains the FK and IK joints to the Bind joints
		L_bindConstraints = Rig_Utils.constrainFKIK(L_BIND_Arm_Joints[1:], L_FK_Arm_Joints, L_IK_Arm_Joints)	

		# create FK and IK controls
		path = "/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/CubeCTL.ma"
		PVpath = "/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/PoleVectorCTL.ma"
		FK_Controls = Rig_Utils.createFKControls(part, L_FK_Arm_Joints)
		
		# create FK finger controls
		L_fingersList = L_thumbJoints[0:3] + L_indexJoints[0:3] + L_middleJoints[0:3] + L_ringJoints[0:3] + L_pinkyJoints[0:3]
		L_FingerControls = Rig_Utils.HandSetUp(path, L_fingersList, L_Hand_Joints)

		# create IK controls
		IK_Controls = Rig_Utils.createIKControls(Lside, part, path, L_IK_handle, PVpath, PVtranslate)

		# create stretchy IK
		Stretchy = Rig_Utils.createStretchy(Lside, part, L_IK_Arm_Joints[0], L_IK_handle, L_IK_Arm_Joints[1], L_IK_Arm_Joints[2], IK_Controls)

		# create the FK IK switch
		SwitchPath = "/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/fkik_switch.ma"
		FKIKSwitch = Rig_Utils.FKIKSwitch(Lside, part, SwitchPath, L_BIND_Arm_Joints, L_FK_Arm_Joints, L_IK_Arm_Joints, L_bindConstraints, FK_Controls, IK_Controls, SwitchTranslate)

		# clean up - tidies up the hierarchy, lock and hide unnecessary channels
		Rig_Utils.CleanUp(FK_Controls, IK_Controls, L_BIND_Arm_Joints, L_FK_Arm_Joints, L_IK_Arm_Joints, Lside, part, FKIKSwitch, Stretchy)

		cmds.select(cl=True)




		"""
		
		-----------------------------------------
		This creates the arm rig on the right side
		-----------------------------------------
		
		"""
		
		
		R_thumbJoints = cmds.listRelatives(Rside + "thumb_01" + skin, allDescendents=True)
		R_thumbJoints.append(Rside + "thumb_01" + skin)
		R_thumbJoints.reverse()

		R_indexJoints = cmds.listRelatives(Rside + "index_01" + skin, allDescendents=True)
		R_indexJoints.append(Rside + "index_01" + skin)
		R_indexJoints.reverse()

		R_middleJoints = cmds.listRelatives(Rside + "middle_01" + skin, allDescendents=True)
		R_middleJoints.append(Rside + "middle_01" + skin)
		R_middleJoints.reverse()

		R_ringJoints = cmds.listRelatives(Rside + "ring_01" + skin, allDescendents=True)
		R_ringJoints.append(Rside + "ring_01" + skin)
		R_ringJoints.reverse()

		R_pinkyJoints = cmds.listRelatives(Rside + "pinky_01" + skin, allDescendents=True)
		R_pinkyJoints.append(Rside + "pinky_01" + skin)
		R_pinkyJoints.reverse()


		cmds.select(cl=True)
		

		
		
		# creates the IK handle
		R_IK_handle = Rig_Utils.createIK(Rside, part, R_IK_Arm_Joints[0], R_IK_Arm_Joints[2])

		# constrains the FK and IK joints to the Bind joints
		R_bindConstraints = Rig_Utils.constrainFKIK(R_BIND_Arm_Joints[1:], R_FK_Arm_Joints, R_IK_Arm_Joints)	

		# create FK and IK controls
		path = "/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/CubeCTL.ma"
		PVpath = "/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/PoleVectorCTL.ma"
		FK_Controls = Rig_Utils.createFKControls(part, R_FK_Arm_Joints)

		
		# create FK finger controls
		R_fingersList = R_thumbJoints[0:3] + R_indexJoints[0:3] + R_middleJoints[0:3] + R_ringJoints[0:3] + R_pinkyJoints[0:3]
		R_FingerControls = Rig_Utils.HandSetUp(path, R_fingersList, R_Hand_Joints)

		
		
		IK_Controls = Rig_Utils.createIKControls(Rside, part, path, R_IK_handle, PVpath, PVtranslate)

		# create stretchy IK
		Stretchy = Rig_Utils.createStretchy(Rside, part, R_IK_Arm_Joints[0], R_IK_handle, R_IK_Arm_Joints[1], R_IK_Arm_Joints[2], IK_Controls)

		# create the FK IK switch
		SwitchPath = "/Users/Winsi/Documents/Art Tools/Maya/ControllerCurves/fkik_switch.ma"
		FKIKSwitch = Rig_Utils.FKIKSwitch(Lside, part, SwitchPath, R_BIND_Arm_Joints, R_FK_Arm_Joints, R_IK_Arm_Joints, R_bindConstraints, FK_Controls, IK_Controls, SwitchTranslate)

		Rig_Utils.CleanUp(FK_Controls, IK_Controls, R_BIND_Arm_Joints, R_FK_Arm_Joints, R_IK_Arm_Joints, Rside, part, FKIKSwitch, Stretchy)


