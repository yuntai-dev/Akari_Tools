import bpy
from mathutils import *
D = bpy.data
C = bpy.context

class BatchRenamePanel(bpy.types.Panel):
    bl_idname = "BatchRename"
    bl_label = "Batch Rename"
    bl_category = "Akari"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.operator('object.batchrename')
        return super().draw(context)

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

                objmat = bpy.data.objects[o.name_full].active_material
                objmat.name = collname
                objmatname = objmat.name
                Matusers = bpy.data.materials[objmatname].users
                    
                if Matusers == 1:
                    print('matusers == 1')
                    bpy.data.collections[collname].color_tag = 'NONE'
                else:
                    print('matusers > 1')
                    if Matusers <= len(incollmat):
                        # print('test')
                        objmat.name = collname
                        bpy.data.collections[collname].color_tag = 'NONE'
                    else:
                        print('Multi-user')
                        self.report({'ERROR'}, '材质用户数大于1')
                        bpy.data.collections[collname].color_tag = 'COLOR_05'
            else:
                print('non name')
                bpy.data.collections[collname].color_tag = 'NONE'
        else:
            print('no')
        
        return{'FINISHED'}
