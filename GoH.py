from cmath import log
import bpy
from mathutils import *
D = bpy.data
C = bpy.context

class GoHPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_GoToHoudini"
    bl_label = "GoB"
    bl_category = "Akari"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context):
        layout = self.layout
        layout.operator('object.gotohoudini')

class GoHOperator(bpy.types.Operator):
    bl_idname = "object.gotohoudini"
    bl_label = "重载模型"

    def execute(self, context):
        selection = bpy.context.selected_objects
        for i in selection:
            modifiles = bpy.data.objects[i.name].modifiers
            for m in modifiles:
                if m.type == "ARMATURE":
                    # m.object == bpy.data.objects["us-cag-1.qc_skeleton"]
                    bpy.context.view_layer.objects.active = i
                    # bpy.context.scene.objects.active = i
                    bpy.context.object.modifiers[m.name].object = bpy.data.objects["us-cag-1.qc_skeleton"]
                    bpy.context.object.modifiers[m.name].use_deform_preserve_volume = True

                    # print(bpy.data.objects[i.name].modifiers[m.name].object)
                    # print(bpy.data.objects["us-cag-1.qc_skeleton"])



        # bpy.data.objects["us-cag-equipment_lonhf_us_assault_torso1"].modifiers["骨架"].object

        return {'FINISHED'}
