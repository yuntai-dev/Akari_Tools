import bpy
from mathutils import *
D = bpy.data
C = bpy.context

class CleanMeshPanel(bpy.types.Panel):
    bl_idname = "CleanMesh"
    bl_label = "Clean Mesh"
    bl_category = "Akari"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context):
        layout = self.layout
        layout.operator('object.cleanmesh')
        return super().draw(context)

class CleanMeshOperator(bpy.types.Operator):
    bl_idname = "object.cleanmesh"
    bl_label = "Clean Mesh"

    def execute(self, context):
        selection = bpy.context.selected_objects
        for o in selection:
            try:
                bpy.context.view_layer.objects.active = o
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.mark_sharp(clear=True)
                bpy.ops.mesh.mark_seam(clear=True)
                bpy.ops.transform.edge_crease(value=-1)
                bpy.ops.transform.edge_bevelweight(value=-1)
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.customdata_custom_splitnormals_clear()

            except:
                print("Object has no custom split normals: " + o.name + ", skipping")
        return {'FINISHED'}
