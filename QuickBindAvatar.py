from enum import auto
from msilib.schema import Error
from re import I
import bpy
import os
import math
from bpy.utils import register_class, unregister_class
getlogin = os.getlogin()
# from ..better_fbx import BetterImportFbx


# class QuickImportRenderPanel(bpy.types.Panel):
class QuickBindAvatarPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_QuickBind"
    bl_label = "角色快捷绑定"
    bl_category = "Tool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_order = 10
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box0 = box.box()
        box1 = box
        box2 = box
        box3 = box

        bettlefbx = 0
        autorig = 0
        quickrig = 0
        addontip = 'All addon working'
        icontype = 'CHECKMARK'

        for i in bpy.context.preferences.addons.keys():
            if i == 'better_fbx':
                bettlefbx = 1
            if i == 'auto_rig_pro-master':
                autorig = 1
            if i == 'auto_rig_pro_quick_rig':
                quickrig = 1
        
        if bettlefbx+autorig+quickrig != 3:
            icontype = 'ERROR'
            addontip = 'Missing'
            if bettlefbx == 0:
                addontip = 'Better FBX'+' '+addontip
            if autorig == 0:
                addontip = 'Auto Rig'+' '+addontip
            if quickrig == 0:
                addontip = 'Quick Rig'+' '+addontip
            

        box0.label(text=addontip, icon=icontype)
        # box0.operator('object.testoperator')

        box.label(text='Rematch Avatar')
        box1.operator('better_import.fbx', text='1. Import FBX')
        box1.operator('arp.quick_import_mapping', text='2. Import Mapping')
        box1.operator('arp.quick_make_rig', text='3. Quick Rig')
        
        box.label(text='Fix Armature')        
        box2.operator('arp.edit_ref', text='4. Edit Refbone')
        box2.operator('object.setmaleboneroll', text='5. Set Roll')
        box3.operator('arp.match_to_rig', text='6. Match Rig')
        box3.operator('object.eyecontorl', text='7. Make Eye Control')


        box.label(text='Finish Avatar')
        box3.operator('arp.set_character_name', text='8. Set Name')


class EyeContorlOperator(bpy.types.Operator):
    bl_idname = "object.eyecontorl"
    bl_label = "创建眼部控制器"

    def execute(self, context):
        actobj = bpy.context.active_object
        if actobj.type == "ARMATURE":
            armature = bpy.data.armatures[actobj.name]
        if actobj.mode == "OBJECT" and actobj.mode == "POSE":
            bpy.ops.object.mode_set(mode='EDIT')
        else:
            focalbone = armature.edit_bones.new(name='Focal')
            erf = armature.edit_bones.new(name='ErF')
            elf = armature.edit_bones.new(name='ElF')

            EyeContorlOperator.EyeAim(armature)

            # 检测是否存在骨骼
            for b in armature.bones:
                if b.name == 'Focal':
                    print('Focal exist')
                    Focalexist = 1
                else:
                    Focalexist = 0

                if b.name == 'ElF':
                    print('El exist')
                    ElFexist = 1
                else:
                    ElFexist = 0

                if b.name == 'ErF':
                    print('Er exist')
                    ErFexist = 1
                else:
                    ErFexist = 0
                continue

            if Focalexist == 0:
                focalbone.parent = armature.edit_bones['root.x']
                for i in armature.bones:
                    if i.name == 'El':
                        bone = armature.edit_bones[i.name]
                        bpy.ops.armature.select_all(action='DESELECT')
                        eyeposion = bone.head[2]
                EyeContorlOperator.Focallocation(focalbone, eyeposion)                
                
            if ElFexist == 0:
                elf.parent = armature.edit_bones['Focal']
                for i in armature.bones:
                    if i.name == 'El':
                        El = armature.edit_bones[i.name]
                        EyeContorlOperator.ElFlocation(elf, focalbone, El)

            if ErFexist == 0:
                erf.parent = armature.edit_bones['Focal']
                for i in armature.bones:
                    if i.name == 'Er':
                        Er = armature.edit_bones[i.name]
                EyeContorlOperator.ErFlocation(erf, focalbone, Er)
            
            # 姿态模式下设置控制器样式
            bpy.ops.object.mode_set(mode='POSE')
            for i in armature.bones:
                if i.name == 'Focal':
                    #激活特定骨骼
                    FocB = bpy.data.objects[actobj.name].pose.bones['Focal'].bone
                    bpy.context.object.data.bones.active = FocB
                    FocB.select = True
                    bpy.context.active_pose_bone.custom_shape = bpy.data.objects["cs_eye_aim_global"]
                    #对自定义形状进行变换
                    bpy.context.active_pose_bone.custom_shape_rotation_euler = (1.5708, 0, 1.5708)
                    bpy.context.active_pose_bone.custom_shape_scale_xyz = (0.5, 0.5, 0.5)

                if i.name == 'ElF':
                    #激活特定骨骼
                    ElFB = bpy.data.objects[actobj.name].pose.bones['ElF'].bone
                    bpy.context.object.data.bones.active = ElFB
                    ElFB.select = True
                    bpy.context.active_pose_bone.custom_shape = bpy.data.objects["cs_eye_aim"]
                    #对自定义形状进行变换
                    bpy.context.active_pose_bone.custom_shape_rotation_euler = (0, 0, 1.5708)
                    bpy.context.active_pose_bone.custom_shape_scale_xyz = (0.5, 0.5, 0.5)

                if i.name == 'ErF':
                    #激活特定骨骼
                    ErFB = bpy.data.objects[actobj.name].pose.bones['ErF'].bone
                    bpy.context.object.data.bones.active = ErFB
                    ErFB.select = True
                    bpy.context.active_pose_bone.custom_shape = bpy.data.objects["cs_eye_aim"]
                    #对自定义形状进行变换
                    bpy.context.active_pose_bone.custom_shape_rotation_euler = (0, 0, 1.5708)
                    bpy.context.active_pose_bone.custom_shape_scale_xyz = (0.5, 0.5, 0.5)
                
                if i.name == 'El':
                    ElB = bpy.data.objects[actobj.name].pose.bones['El'].bone
                    bpy.context.object.data.bones.active = ElB
                    ElB.select = True
                    bpy.ops.pose.constraint_add(type='TRACK_TO')
                    bpy.data.objects[actobj.name_full].pose.bones["El"].constraints["Track To"].target = actobj
                    bpy.data.objects["rig"].pose.bones["El"].constraints["Track To"].subtarget = 'ElF'
                    bpy.context.object.pose.bones["El"].constraints["Track To"].track_axis = 'TRACK_Y'
                    bpy.context.object.pose.bones["El"].constraints["Track To"].up_axis = 'UP_Z'

                if i.name == 'Er':
                    ErB = bpy.data.objects[actobj.name].pose.bones['Er'].bone
                    bpy.context.object.data.bones.active = ErB
                    ErB.select = True
                    bpy.ops.pose.constraint_add(type='TRACK_TO')
                    bpy.data.objects[actobj.name_full].pose.bones["Er"].constraints["Track To"].target = actobj
                    bpy.data.objects["rig"].pose.bones["Er"].constraints["Track To"].subtarget = 'ErF'
                    bpy.context.object.pose.bones["Er"].constraints["Track To"].track_axis = 'TRACK_Y'
                    bpy.context.object.pose.bones["Er"].constraints["Track To"].up_axis = 'UP_Z'


        return{'FINISHED'}

    def EyeAim(armature):
        for i in armature.bones:
            if i.name == 'El':
                El = armature.edit_bones[i.name]
        for i in armature.bones:
            if i.name == 'Er':
                Er = armature.edit_bones[i.name]
        El.tail = (El.head[0], El.tail[1], El.head[2])
        Er.tail = (Er.head[0], Er.tail[1], Er.head[2])
        print('Eye Aim Front')
        return{'FINISHED'}

    def Focallocation(focalbone, eyeposion):
        #根据eye高度创建Focal骨
        focalbone.head = (focalbone.head[0], focalbone.head[1]-0.3, eyeposion)
        focalbone.tail = (focalbone.tail[0], focalbone.tail[1]-0.5, eyeposion)
        return{'FINISHED'}

    def ElFlocation(elf, focalbone, El):
        #根据eye高度创建Focal骨
        elf.head = (El.head[0], focalbone.head[1], El.head[2])
        elf.tail = (El.tail[0], focalbone.tail[1]+0.1, El.tail[2])
        return{'FINISHED'}

    def ErFlocation(erf, focalbone, Er):
        #创建ErF骨
        erf.head = (Er.head[0], focalbone.head[1], Er.head[2])
        erf.tail = (Er.tail[0], focalbone.tail[1]+0.1, Er.tail[2])
        return{'FINISHED'}


class SetMaleBoneRoll(bpy.types.Operator):
    bl_idname = "object.setmaleboneroll"
    bl_label = "设定骨骼Roll值"

    def execute(self, context):
        actobj = bpy.context.active_object
        if actobj.type == "ARMATURE":
            armaturename = actobj.data.name
            armature = bpy.data.armatures[armaturename]
            # print(armature.is_editmode)
            # if armature.is_editmode == "True":
            if actobj.mode == "EDIT":
                # bpy.ops.object.editmode_toggle()
                self.setroll(armature)   
                bpy.ops.object.mode_set(mode='OBJECT')
            else:
                bpy.ops.object.mode_set(mode='EDIT')
                self.setroll(armature)
                bpy.ops.object.mode_set(mode='OBJECT')  
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

class TestOperator(bpy.types.Operator):
    bl_idname = "object.testoperator"
    bl_label = "测试"

    def execute(self, context):
        print(bpy.context.preferences.addons.keys())
        return{'FINISHED'}

classes = (QuickBindAvatarPanel,
            SetMaleBoneRoll,
            EyeContorlOperator,
            TestOperator,
            )

def register():
    global classes
    for cls in classes:
        register_class(cls)

def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)