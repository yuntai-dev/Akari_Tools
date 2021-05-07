'''
Author: your name
Date: 2021-03-19 18:49:55
LastEditTime: 2021-05-07 14:20:42
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Test_addon\view_tool.py
'''
# context.area: VIEW_3D


import bpy

class Collection_rename(bpy.types.Operator):
    bl_idname = "collection.rename"
    bl_label = "Bake Rename"

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
            print(bpy.context.material_slot)


        # for i,o in enumerate(collobjlist):
        #     o.name = collname+'_'+str(i+1).zfill(2)
        #     objmat = bpy.data.objects[o.name_full].active_material
        #     if o.type=='MESH':
        #         objmatname = objmat.name
        #         Matusers = bpy.data.materials[objmatname].users
        #         if collname != objmatname:
        #             if Matusers == 1:
        #                 # print('oneuser')
        #                 objmat.name = collname
        #                 bpy.data.collections[collname].color_tag = 'NONE'
        #             else:
        #                 print('maxuser')
                        
                        
        #                 # if Matusers <= len(incollmat):
        #                 #     print('test')
        #                 #     # objmat.name = collname
        #                 #     # bpy.data.collections[collname].color_tag = 'NONE'
        #                 # else:
        #                 #     print('Multi-user')
        #                 #     bpy.data.collections[collname].color_tag = 'COLOR_05'
        #         else:
        #             bpy.data.collections[collname].color_tag = 'NONE'
        #     else:
        #         print('no')
        
        return{'FINISHED'}

class LoopEdit(bpy.types.Operator):
    bl_idname = "loop.edit"
    bl_label = "loopedit"

    def execute(self,context):
        bpy.ops.mesh.select_nth()
        bpy.ops.mesh.loop_multi_select(ring=False)
        bpy.ops.mesh.dissolve_edges()
        return{'FINISHED'}


class ParallelEdit(bpy.types.Operator):
    bl_idname = "parallel.edit"
    bl_label = "paralleledit"

    def execute(self,context):
        bpy.ops.mesh.select_nth()
        bpy.ops.mesh.loop_multi_select(ring=True)
        bpy.ops.mesh.edge_collapse()
        return{'FINISHED'}


class CleanNormalOperator(bpy.types.Operator):
    bl_idname = "object.cleannormal"
    bl_label = "CleanNormal"

    def execute(self, context):        
        selection = bpy.context.selected_objects

        for o in selection:
            try:
                bpy.context.view_layer.objects.active = o
                bpy.ops.mesh.customdata_custom_splitnormals_clear()
            except:
                print("Object has no custom split normals: " + o.name + ", skipping")
        return {'FINISHED'}
