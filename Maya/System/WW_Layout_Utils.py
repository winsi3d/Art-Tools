"""
Script: Locator_Lyt
Author: Wini Wang	wini@winsi3d.com
Description: information about the locator names and positions
"""


# Arm Locators
ArmLocatorNames = [ "arm_root", "clavicle", "shoulder", "elbow", "wrist"]
ArmLocatorPos = ([1.00, 15.0, 0.88], [1.00, 15, 0.88], [1.7, 15.0, 0.0], [4.47, 15.0, -0.5], [7.2, 15.0, 0.0 ])

HandLocatorNames = ["hand", "thumb_01", "thumb_02", "thumb_03", "thumb_04", "index_01", "index_02", "index_03", "index_04", "middle_01", "middle_02", "middle_03", "middle_04", "ring_01", "ring_02", "ring_03", "ring_04", "pinky_01", "pinky_02", "pinky_03", "pinky_04"]
HandLocatorPos = ([7.5, 15.0, 0.0], [7.55, 15, .589], [7.65, 15, 0.966], [7.793, 15, 1.282], [8.112, 15, 1.71], [8.445, 15, 0.464], [8.814, 15, 0.464], [9.225, 15, 0.464], [9.678, 15, 0.464], [8.523, 15, 0.148], [9.00, 15, 0.148], [9.408, 15, 0.148], [9.862, 15, 0.148], [8.504, 15, -0.192], [8.900, 15, -0.192], [9.315, 15, -0.192], [9.67, 15, -0.192], [8.444, 15, -0.506], [8.804, 15, -0.506], [9.133, 15, -0.506], [9.418, 15, -0.506])

# Leg Locators
LegLocatorNames = ["leg_root", "pelvis", "hip", "knee", "ankle", "heel", "ball", "toe_End"]
LegLocatorPos = ([-0.06, 10.4, 0], [-0.06, 10.4, 0], [1.25, 9.8, 0], [1.25, 5.6, 0.15], [1.25, 1.50, -0.3], [1.25, 0.28, -1.00],[1.25, 0.28, 0.9], [1.25, 0.28, 1.9] )

FootRockLocNames = ["outer_foot_loc", "inner_foot_loc"]
FootRockPos = ([2, 0, 0], [0.5, 0, 0])

# Spine Locators
SpineLocatorNames = ["spine_root", "cog", "spine_01", "spine_02", "spine_03", "chest", "neck", "head", "head_End"] 
SpineLocatorPos = ([0, 11.25, 0], [0, 11.25, 0], [0, 12.0, 0], [0, 12.75, 0], [0, 13.5, 0], [0, 14.25, 0], [0, 15.5, 0], [0, 16, 0], [0, 18, 0])

# Head Locators
HeadLocatorNames = ["neck", "head", "head_End"]
HeadLocatorPos = ([0, 15.5, 0], [0, 16, 0], [0, 18, 0])