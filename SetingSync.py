import bpy

class SettingSyncPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_SETTINGSYNC"
    bl_label = "SettingSync"
    bl_category = "Akari"
    bl_space_type = "PREFERENCES"
    bl_region_type = "WINDOW"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.settingsyncop")

        # return {'FINISHED'}


class SettingSyncOPOperator(bpy.types.Operator):
    bl_idname = "object.settingsyncop"
    bl_label = "SettingSyncOP"

    def execute(self, context):
        print("test")
        return {'FINISHED'}
