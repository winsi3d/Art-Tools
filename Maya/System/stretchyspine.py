

import maya.cmds as mc 
 
def nk_ribbonSpine():
     
    '''
    Version
    -----------------------
    v02
    * Switched the prefix so that the prefix specified of this is an offset ribbon, or a basic
    * Fixed double transforms on the nurbsPlane and the the follicles
     
    About
    -----------------------
    Creates a ribbon spine based on the Aaron Holly's method. 
     
    Returns
    -----------------------
    None
     
    Requires
    -----------------------
    None
     
    Example
    -----------------------
    Source the code, then run the following line to bring up the nk_ribbonSpine UI:
    nk_ribbonSpine()
     
    None
     
    TODO
    -----------------------
    * Add an option to switch the direction of the spine so it can be created facing in x or y
    '''
     
 
    # GUI FOR RIBBON SPLINE
 
    # delete the ui if it exists
    if (mc.window('nk_ribbonSpineGui', exists=True)):
        mc.deleteUI('nk_ribbonSpineGui')
 
    # Create the Gui 
    mc.window('nk_ribbonSpineGui', title='nk_ribbonSpine', h=125, w=150)
     
    #Create main Col
    mc.columnLayout('mainCol')
     
    # FrameLayot - Prefix
    mc.frameLayout('prefixFL', label='prefix')
    mc.textFieldGrp('prefix', label='PREFIX', text='CHAR_SIDE_LIMB')
    mc.setParent('mainCol')
     
    # FrameLayout - Ribbon Type
    mc.frameLayout('ribbonTypeFL', label='Ribbon Type')
    mc.button('basicRbnBTN', l='BASIC', c='basicRibbon()')
    mc.button('offsetRbnBTN', l='OFFSET', c='offsetRibbon()' )
    mc.setParent('mainCol')
     
     
    mc.window('nk_ribbonSpineGui', e=True, h=125, w=150)
     
    mc.showWindow('nk_ribbonSpineGui')
 
  
####RIBBON SPINE FUNCTION BELOW HERE###################
 
def nk_createRibbonSpine(prefix='CHAR_SIDE_LIMB', type='offset'):
 
    ##+++++++++++++++++++++++++++++++++##
    ##+++++++nk_createRibbonSpine++++++##
    ##+++++++++++++++++++++++++++++++++##
 
     
    #Check the type of ribbon
    if type == 'basic':
        suffix = 'rbnBasic'
 
    if type =='offset':
        suffix = 'rbnOffset'
     
     
    #create group for ribbon rig
    ribbonRigGrp = mc.group(em=True, n=(prefix + '_' + suffix + '_rig_grp'))
    # ribbonRigGrp = mc.group(em=True, n=(prefix))
 
    # Create nurbs plane
    ribbonPlane = mc.nurbsPlane (n=(prefix + '_' + suffix + 'Plane'), p=[0, 0, 0], ax= [0, 0 ,1], w=1 ,lr=5 ,d=3, u=1, v=5, ch=0)
    ribbonPlaneShape = mc.listRelatives(ribbonPlane, c=True, s=True) #get shape node
     
    # CLEANUP: Parent plane to rigGrp and turn off inheritsTransforms
    mc.parent(ribbonPlane[0], ribbonRigGrp)
    mc.setAttr('{ribbonPlane}.inheritsTransform'.format(ribbonPlane=ribbonPlane[0]),0, lock=True)
    #mc.setAttr('{ribbonPlane}.inheritsTransform'.format(ribbonPlane=ribbonPlane[0]), lock=True)
     
 
    ## rebuildSurface
    mc.rebuildSurface(ribbonPlane[0], rpo=1, rt=0, end=1, kr=0, kcp=0, kc=0, su=1, du=1, sv=0, dv=3, tol=0.01, dir=0)
     
    # Create follicles * 5
     
    ##Create an empty group for the follicles
    folGroup = mc.group(em=True, n=(prefix + '_' + suffix + '_follicleGrp'))
         
    # CLEANUP: Parent follicleGrp to rigGrp
    mc.parent(folGroup, ribbonRigGrp)
     
    ##Create a list for the follicles
    folList = []
 
    ##Create the follicles and ribbon joints
    for f in range(5):
        follicle = mc.createNode('follicle', n=('{prefix}_{suffix}_FollicleShape_{number}'.format(prefix=prefix, suffix=suffix ,number=(f+1))))
        print follicle
        follicleTransform = mc.listRelatives(follicle,  p=True) #get transform node
 
        ribbonJnt = mc.joint(n='{prefix}_{suffix}_jnt_{f}'.format(prefix=prefix,suffix=suffix,f=f+1))#create joint
        grp=mc.group(n=(ribbonJnt+'_offsetGrp'))#grp joint
 
        ## connect folliclesShapes to the plane
        mc.connectAttr(('{ribbonPlaneShape}.local'.format(ribbonPlaneShape=ribbonPlaneShape[0])) ,('{follicle}.inputSurface'.format(follicle=follicle)))
        mc.connectAttr(('{ribbonPlaneShape}.worldMatrix[0]'.format(ribbonPlaneShape=ribbonPlaneShape[0])) ,('{follicle}.inputWorldMatrix'.format(follicle=follicle)))
        ## connect follicleShapes to follicleTransform
        mc.connectAttr((follicle+'.outTranslate'), (follicleTransform[0]+'.translate') )
        mc.connectAttr((follicle+'.outRotate'), (follicleTransform[0]+'.rotate') )
 
        ##position the follicles along the plane
        mc.setAttr((follicle+'.parameterU'), 0.5)
        vSpanHeight = ((f+1.0)/5.0) - .1
        mc.setAttr((follicle+'.parameterV'), vSpanHeight)
         
        #Turn off inherit transforms on the follicles
        mc.setAttr('{follicleTransform}.inheritsTransform'.format(follicleTransform=follicleTransform[0]),0, lock=True)
         
        ##parent the follicle to the group and add to lists
        mc.parent(follicleTransform[0], folGroup)
        folList.append(follicle)
         
    # Create ribbon bind joints and setup aim constraints
    mc.select(cl=True)
 
    bindBaseJnt = mc.joint(p=(0,-2.5,0), o=(0,0,90), rad=2, n=(prefix+'_'+suffix+'_base_bind_01'))
    mc.joint(p=(0,-2,0), n=(prefix+'_ribbon_base_bind_02'))
 
    mc.select(cl=True)
 
    bindTipJnt = mc.joint(p=(0,2.5,0), o=(0,0,-90), rad=2, n=(prefix+'_'+suffix+'_tip_bind_01'))
    mc.joint(p=(0,2,0), n=(prefix+'_ribbon_tip_bind_02'))
 
    mc.select(cl=True)
 
 
    bindMidJnt = mc.joint(p=(0,0,0), o=(0,0,0), rad=2, n=(prefix+'_'+suffix+'_mid_bind_01'))
    mc.select(cl=True)
 
    # create control Locators and parent bindJoint to aimLocator
    ##baseLocators
    basePosLoc = mc.spaceLocator(n=(prefix+'_'+suffix+'_base_pos_loc'))
    baseUpLoc = mc.spaceLocator(n=(prefix+'_'+suffix+'_base_up_loc'))
    baseAimLoc = mc.spaceLocator(n=(prefix+'_'+suffix+'_base_aim_loc'))
 
    mc.parent(baseUpLoc,baseAimLoc,basePosLoc )#parent locators
    mc.xform(basePosLoc, t=(0,-2.5,0))#move locator to base position
    mc.xform(baseUpLoc, ws=True, t=(0,-2.5,2))# offset Up locator in Z
    mc.parent(bindBaseJnt,baseAimLoc)#parent jnt to aim locator
     
     
    #CLEANUP: startPosLoc to rigGrp
    mc.parent(basePosLoc, ribbonRigGrp)
     
    ##midLocators
    midPosLoc = mc.spaceLocator(n=(prefix+'_'+suffix+'_mid_pos_loc'))
    midUpLoc = mc.spaceLocator(n=(prefix+'_'+suffix+'_mid_up_loc'))
    midAimLoc = mc.spaceLocator(n=(prefix+'_'+suffix+'_mid_aim_loc'))
 
    mc.parent(midUpLoc,midAimLoc,midPosLoc )#parent locators
    mc.xform(midUpLoc, ws=True, t=(0,0,2))# offset Up locator in Z
    mc.parent(bindMidJnt,midAimLoc)#parent jnt to aim locator
     
    mc.parent(midPosLoc, ribbonRigGrp)
     
    ##tipLocators
    tipPosLoc = mc.spaceLocator(n=(prefix+'_'+suffix+'_tip_pos_loc'))
    tipUpLoc = mc.spaceLocator(n=(prefix+'_'+suffix+'_tip_up_loc'))
    tipAimLoc = mc.spaceLocator(n=(prefix+'_'+suffix+'_tip_aim_loc'))
 
    mc.parent(tipUpLoc,tipAimLoc,tipPosLoc)#parent locators
    mc.xform(tipPosLoc, t=(0,2.5,0))#move locator to tip position
    mc.xform(tipUpLoc, ws=True, t=(0,2.5,2))# offset Up locator in Z
    mc.parent(bindTipJnt,tipAimLoc)#parent jnt to aim locator
     
    #CLEANUP: tipPosLoc to rigGrp 
    mc.parent(tipPosLoc, ribbonRigGrp)
     
    #setup aim relationsips
    ##basic
    if type=='basic':
        ##baseAimLoc > tipPos##
        mc.aimConstraint(tipPosLoc[0],baseAimLoc[0], aim=(0,1,0), u=(0,0,1), wut='object', wuo=baseUpLoc[0])
        ##tipAimLoc > basePos##
        mc.aimConstraint(basePosLoc[0],tipAimLoc[0], aim=(0,-1,0), u=(0,0,1), wut='object', wuo=tipUpLoc[0])
        ##midAimLoc > tipPos##
        mc.aimConstraint(tipPosLoc[0],midAimLoc[0], aim=(0,1,0), u=(0,0,1), wut='object', wuo=midUpLoc[0])
         
        # midPosLoc to follow both base and tip
        mc.pointConstraint(basePosLoc[0],tipPosLoc[0],midPosLoc[0], mo=False)
        # midPosAim to follow both base and tip Aim
        mc.pointConstraint(baseUpLoc[0],tipUpLoc[0],midUpLoc[0], mo=False)
         
    if type=='offset':
         
        ##baseAimLoc > midBindJoint##
        mc.aimConstraint(bindMidJnt,baseAimLoc[0], aim=(0,1,0), u=(0,0,1), wut='object', wuo=baseUpLoc[0])
        #tipAimLoc > midBindJoint##
        mc.aimConstraint(bindMidJnt,tipAimLoc[0], aim=(0,-1,0), u=(0,0,1), wut='object', wuo=tipUpLoc[0])
        ##midAimLoc > tipPos##
        mc.aimConstraint(tipPosLoc[0],midAimLoc[0], aim=(0,1,0), u=(0,0,1), wut='object', wuo=midUpLoc[0])
         
        # midPosLoc to follow both base and tip
        mc.pointConstraint(basePosLoc[0],tipPosLoc[0],midPosLoc[0], mo=False)
        # midPosAim to follow both base and tip Aim
        mc.pointConstraint(baseUpLoc[0],tipUpLoc[0],midUpLoc[0], mo=False)
 
    # Bind skin 
    mc.select(cl=True)
    print bindBaseJnt 
    print bindMidJnt 
    print bindTipJnt
    mc.skinCluster(bindBaseJnt,bindMidJnt,bindTipJnt,ribbonPlane, n=(prefix+'_'+suffix+'_skinCluster'), tsb=True, ih=True, bm=0, sm=0, nw=1, wd=0, mi=3, omi=False, dr=4)
 
def basicRibbon():
    prefix = mc.textFieldGrp('prefix', q=True, text=True)
    nk_createRibbonSpine(prefix, type='basic')
 
def offsetRibbon():
    prefix = mc.textFieldGrp('prefix', q=True, text=True)
    nk_createRibbonSpine(prefix, type='offset')