import bpy

class AkaritoolsPreferences(bpy.types.AddonPreferences):
    bl_idname = "AkaritoolsPreferences"

    def draw(self,context):
        layout = self.layout
        layout.label(text="test")
