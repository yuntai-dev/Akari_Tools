import bpy
from bpy.utils import register_class, unregister_class
from mathutils import *
import math
D = bpy.data
C = bpy.context

class AniToolsPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_AniTools"
    bl_label = "Animation Tools"
    bl_category = "ARP"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_order = 10
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        layout.operator('object.setmaleboneroll')
        # layout.operator('object.setfemaleboneroll')
        # layout.operator('object.batchsetorigin')

class SetMaleBoneRoll(bpy.types.Operator):
    bl_idname = "object.setmaleboneroll"
    bl_label = "设定骨骼Roll值"

    def execute(self, context):
        actobj = bpy.context.active_object
        if actobj.type == "ARMATURE":
            armaturename = actobj.data.name
            armature = bpy.data.armatures[armaturename]
            if armature.is_editmode == "True":
                bpy.ops.object.editmode_toggle()
                self.setroll(armature)   
            else:
                bpy.ops.object.editmode_toggle()
                self.setroll(armature)
                bpy.ops.object.editmode_toggle()
        return {'FINISHED'} 
        

    @classmethod
    def setroll(cls, armature):
        for b in armature.edit_bones:

#左手
            if b.name == 'hand_ref.l':
                b.roll = math.radians(51)
                print("hand_ref.l: "+str(b.roll))

            if b.name == "thumb1_ref.l":
                b.roll = math.radians(193)
                print("thumb1_ref.l: "+str(b.roll))

            if b.name == "thumb2_ref.l":
                b.roll = math.radians(188)
                print("thumb2_ref.l: "+str(b.roll))

            if b.name == "thumb3_ref.l":
                b.roll = math.radians(189)
                print("thumb3_ref.l: "+str(b.roll))

            if b.name == "index1_base_ref.l":
                b.roll = math.radians(62)
                print("index1_base_ref.l: "+str(b.roll))

            if b.name == "index1_ref.l":
                b.roll = math.radians(93)
                print("index1_ref.l: "+str(b.roll))

            if b.name == "index2_ref.l":
                b.roll = math.radians(113)
                print("index2_ref.l: "+str(b.roll))

            if b.name == "index3_ref.l":
                b.roll = math.radians(113)
                print("index3_ref.l: "+str(b.roll))

            if b.name == "middle1_base_ref.l":
                b.roll = math.radians(53)
                print("middle1_base_ref.l: "+str(b.roll))

            if b.name == "middle1_ref.l":
                b.roll = math.radians(81)
                print("middle1_ref.l: "+str(b.roll))

            if b.name == "middle2_ref.l":
                b.roll = math.radians(95)
                print("middle2_ref.l: "+str(b.roll))

            if b.name == "middle3_ref.l":
                b.roll = math.radians(104)
                print("middle3_ref.l: "+str(b.roll))

            if b.name == "ring1_base_ref.l":
                b.roll = math.radians(46)
                print("ring1_base_ref.l: "+str(b.roll))

            if b.name == "ring1_ref.l":
                b.roll = math.radians(74)
                print("ring1_ref.l: "+str(b.roll))

            if b.name == "ring2_ref.l":
                b.roll = math.radians(97)
                print("ring2_ref.l: "+str(b.roll))

            if b.name == "ring3_ref.l":
                b.roll = math.radians(100)
                print("ring3_ref.l: "+str(b.roll))

            if b.name == "pinky1_base_ref.l":
                b.roll = math.radians(47)
                print("pinky1_base_ref.l: "+str(b.roll))

            if b.name == "pinky1_ref.l":
                b.roll = math.radians(65)
                print("pinky1_ref.l: "+str(b.roll))

            if b.name == "pinky2_ref.l":
                b.roll = math.radians(78)
                print("pinky2_ref.l: "+str(b.roll))

            if b.name == "pinky3_ref.l":
                b.roll = math.radians(87)
                print("pinky3_ref.l: "+str(b.roll))

                

            if b.name == "shoulder_ref.l":
                b.roll = math.radians(5.4)
                print("shoulder_ref.l: "+str(b.roll))

            if b.name == "arm_ref.l":
                b.roll = math.radians(58)
                print("arm_ref.l: "+str(b.roll))

            if b.name == "forearm_ref.l":
                b.roll = math.radians(60)
                print("forearm_ref.l: "+str(b.roll))














#右手
            if b.name == 'hand_ref.r':
                b.roll = math.radians(-59)
                print("hand_ref.r: "+str(b.roll))

            if b.name == "thumb1_ref.r":
                b.roll = math.radians(167)
                print("thumb1_ref.r: "+str(b.roll))

            if b.name == "thumb2_ref.r":
                b.roll = math.radians(172)
                print("thumb2_ref.r: "+str(b.roll))

            if b.name == "thumb3_ref.r":
                b.roll = math.radians(173)
                print("thumb3_ref.r: "+str(b.roll))

            if b.name == "index1_base_ref.r":
                b.roll = math.radians(-80)
                print("index1_base_ref.r: "+str(b.roll))

            if b.name == "index1_ref.r":
                b.roll = math.radians(-100)
                print("index1_ref.r: "+str(b.roll))

            if b.name == "index2_ref.r":
                b.roll = math.radians(-110)
                print("index2_ref.r: "+str(b.roll))

            if b.name == "index3_ref.r":
                b.roll = math.radians(-108)
                print("index3_ref.r: "+str(b.roll))

            if b.name == "middle1_base_ref.r":
                b.roll = math.radians(-57)
                print("middle1_base_ref.r: "+str(b.roll))

            if b.name == "middle1_ref.r":
                b.roll = math.radians(-94)
                print("middle1_ref.r: "+str(b.roll))

            if b.name == "middle2_ref.r":
                b.roll = math.radians(-103)
                print("middle2_ref.r: "+str(b.roll))

            if b.name == "middle3_ref.r":
                b.roll = math.radians(-106)
                print("middle3_ref.r: "+str(b.roll))

            if b.name == "ring1_base_ref.r":
                b.roll = math.radians(-54)
                print("ring1_base_ref.r: "+str(b.roll))

            if b.name == "ring1_ref.r":
                b.roll = math.radians(-89)
                print("ring1_ref.r: "+str(b.roll))

            if b.name == "ring2_ref.r":
                b.roll = math.radians(-97)
                print("ring2_ref.r: "+str(b.roll))

            if b.name == "ring3_ref.r":
                b.roll = math.radians(-96)
                print("ring3_ref.r: "+str(b.roll))

            if b.name == "pinky1_base_ref.r":
                b.roll = math.radians(-48)
                print("pinky1_base_ref.r: "+str(b.roll))

            if b.name == "pinky1_ref.r":
                b.roll = math.radians(-68)
                print("pinky1_ref.r: "+str(b.roll))

            if b.name == "pinky2_ref.r":
                b.roll = math.radians(-88)
                print("pinky2_ref.r: "+str(b.roll))

            if b.name == "pinky3_ref.r":
                b.roll = math.radians(-93)
                print("pinky3_ref.r: "+str(b.roll))



            if b.name == "shoulder_ref.r":
                b.roll = math.radians(-5.4)
                print("shoulder_ref.l: "+str(b.roll))

            if b.name == "arm_ref.r":
                b.roll = math.radians(-58)
                print("arm_ref.l: "+str(b.roll))

            if b.name == "forearm_ref.r":
                b.roll = math.radians(-60)
                print("forearm_ref.l: "+str(b.roll))





#其他
            if b.name == "head_ref.x":
                b.roll = math.radians(0)
                print("head_ref.x: "+str(b.roll))

            if b.name == "neck_ref.x":
                b.roll = math.radians(0)
                print("neck_ref.x: "+str(b.roll))

            if b.name == "spine_03_ref.x":
                b.roll = math.radians(0)
                print("spine_03_ref.x: "+str(b.roll))

            if b.name == "spine_02_ref.x":
                b.roll = math.radians(0)
                print("spine_02_ref.x: "+str(b.roll))

            if b.name == "spine_01_ref.x":
                b.roll = math.radians(0)
                print("spine_01_ref.x: "+str(b.roll))

            if b.name == "root_ref.x":
                b.roll = math.radians(0)
                print("root_ref.x: "+str(b.roll))


            if b.name == "thigh_ref.l":
                b.roll = math.radians(-186)
                print("thigh_ref.l: "+str(b.roll))

            if b.name == "leg_ref.l":
                b.roll = math.radians(-185)
                print("leg_ref.l: "+str(b.roll))

            if b.name == "foot_ref.l":
                b.roll = math.radians(-192)
                print("foot_ref.l: "+str(b.roll))

            if b.name == "toes_ref.l":
                b.roll = math.radians(168)
                print("toes_ref.l: "+str(b.roll))



            if b.name == "thigh_ref.r":
                b.roll = math.radians(-174)
                print("thigh_ref.r: "+str(b.roll))

            if b.name == "leg_ref.r":
                b.roll = math.radians(-175)
                print("leg_ref.r: "+str(b.roll))

            if b.name == "foot_ref.r":
                b.roll = math.radians(192)
                print("foot_ref.r: "+str(b.roll))

            if b.name == "toes_ref.r":
                b.roll = math.radians(-168)
                print("toes_ref.r: "+str(b.roll))
















classes = (AniToolsPanel,
    SetMaleBoneRoll,
    # SetFemaleBoneRoll
            )

def register():
    global classes
    for cls in classes:
        register_class(cls)

def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)