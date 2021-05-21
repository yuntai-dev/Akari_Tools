'''
Author: your name
Date: 2021-04-21 16:05:24
LastEditTime: 2021-05-21 14:42:42
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Akari_Toolbag\Test.py
'''
import bpy
from mathutils import *
import re
import os

D = bpy.data
C = bpy.context


class Test_OPOperator(bpy.types.Operator):
    bl_idname = "object.test_op"
    bl_label = "Test_OP"


    def execute(self, context):
        selpath = []                                            #初始化贴图路径
        context = bpy.context
        scene = context.scene
        selfTools = scene.self_Tools                            #调用全局propertygroup参数
        selpath = selfTools.Tex_path                            #选中贴图路径

        if selpath.endswith('\\'):                              #在blender搜索栏选择的路径后缀会自带一个'\'，这里检测后缀是否带'\'，检测到就自动删除，windows复制路径不存在这个问题。
            selpath = selpath.rstrip('\\')

        selobj = bpy.context.selected_objects
        actobj = bpy.context.active_object
        actmat = actobj.active_material
        selnode = bpy.context.selected_nodes

        for sel in selobj:
            if sel.type == 'MESH':

                for i in selnode:
                    img = actmat.node_tree.nodes[i.name].image
                    bpy.data.images[img.name].filepath = ''
                    refilepath = selpath + '\\' + img.name
                    bpy.data.images[img.name].filepath = refilepath
                    print(refilepath)

                bpy.ops.image.reload()

        return {'FINISHED'}