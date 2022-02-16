import bpy
from mathutils import *
D = bpy.data
C = bpy.context

class ToolsPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_3DTools"
    bl_label = "3D Tools"
    bl_category = "Akari"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context):
        layout = self.layout
        layout.operator('object.cleanmesh')
        layout.operator('object.batchrename')
        layout.operator('object.batchsetorigin')

class CleanMeshOperator(bpy.types.Operator):
    bl_idname = "object.cleanmesh"
    bl_label = "初始化模型信息"

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

class BatchRenameOperator(bpy.types.Operator):
    bl_idname = "object.batchrename"
    bl_label = "Batch Rename"

    def execute(self, context):
        coll = bpy.context.collection
        collname = bpy.context.collection.name
        obj = list(bpy.context.collection.objects)
        collobj = coll.all_objects
        collobjlist = list(collobj)

        incollmat = []

        for s in collobjlist:
            if s.type=='MESH':
                incollmat.append(s.active_material)

        for i,o in enumerate(collobjlist):
            if o.type=='MESH':                                      #检测对象是否为mesh
                print('mesh')
                o.name = collname+'_'+str(i+1).zfill(2)             #重命名
        else:
            print('no')
        
        return{'FINISHED'}

class BatchSetOriginOperator(bpy.types.Operator):
    bl_idname = "object.batchsetorigin"
    bl_label = "Batch Set Origin"

    def execute(self,context):
        selobj = bpy.context.selected_objects
        for i in selobj:
            bpy.context.view_layer.objects.active = i
            print(bpy.data.objects[i.name_full].dimensions.z)
            # bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        return{'FINISHED'}
