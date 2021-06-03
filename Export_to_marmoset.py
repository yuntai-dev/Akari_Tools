'''
Author: your name
Date: 2021-04-16 13:49:32
LastEditTime: 2021-05-20 13:41:49
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Akari_Tools\Export_to_marmoset.py
'''
import os
import bpy
from pathlib import Path
from . My_PropertyGroup     import MyProperties
from mathutils import *
data = bpy.data
context = bpy.context
operator = bpy.types.Operator

class Export_To_Marmoset_Bake(operator):
    bl_idname = "export.marmoset"
    bl_label = "Export"

    def execute(self,context):
        scene = bpy.context.scene
        selfTools = scene.self_Tools                            #调用全局propertygroup参数
        selpath = selfTools.Ept_to_mar_path
        ospath = Path(selpath+'\\'+'Bake\\')

        selobj = context.selected_objects
        actobj = context.active_object
        actcoll = context.collection.name_full
        credir = selpath+'\\'+'Bake\\'
        
        if ospath.is_dir() is False:
            os.mkdir(selpath+'\\'+'Bake\\')
            print('yes')
        else:
            print('no')
            
        bpy.ops.export_scene.fbx(filepath=credir+actcoll+'.fbx',use_selection=True,filter_glob='*.fbx')
        return{'FINISHED'}

class Export_To_Marmoset_Render(bpy.types.Operator):
    bl_idname = "object.export_to_marmoset_render"
    bl_label = "Export_To_Marmoset_Render"

    def execute(self, context):

        for i in selobj:
            actmat = bpy.data.objects[i.name_full].active_material
            texnode = actmat.node_tree.nodes
            for s in texnode:
                
                if s.type == 'TEX_IMAGE':
                    image = bpy.data.materials[actmat.name].node_tree.nodes[s.name].image
                    print(image.name_full.split(sep='.'))                                        #字符串拆分删除无用后缀
                    imagepath = credir+image.name
                    print(imagepath)
                    bpy.ops.image.save_render(filepath=imagepath)

                else:
                    print('non')


        # actmat = bpy.data.objects[actobj_name].active_material   #获取选中模型的材质
        # actmat_name = actmat.name_full


        # bpy.ops.export_scene.fbx()
        # print(actmat_name)
        
        return{"FINISHED"}