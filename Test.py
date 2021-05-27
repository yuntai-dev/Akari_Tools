'''
Author: your name
Date: 2021-04-21 16:05:24
LastEditTime: 2021-05-27 15:33:10
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Akari_Toolbag\Test.py
'''
import numpy as np
import bpy
import os
import mathutils
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

from . My_PropertyGroup     import MyProperties

D = bpy.data
C = bpy.context
O = bpy.ops


class Test_OPOperator(bpy.types.Operator):
    bl_idname = "object.test_op"
    bl_label = "Test_OP"


    def execute(self, context):
        #=================================================================================================================
        # selpath = []                                            #初始化贴图路径
        # context = bpy.context
        # scene = context.scene
        # selfTools = scene.self_Tools                            #调用全局propertygroup参数
        # selpath = selfTools.Tex_path                            #选中贴图路径

        # if selpath.endswith('\\'):                              #在blender搜索栏选择的路径后缀会自带一个'\'，这里检测后缀是否带'\'，检测到就自动删除，windows复制路径不存在这个问题。
        #     selpath = selpath.rstrip('\\')

        # selobj = bpy.context.selected_objects
        # actobj = bpy.context.active_object
        # actmat = actobj.active_material
        # selnode = bpy.context.selected_nodes

        # for sel in selobj:
        #     if sel.type == 'MESH':

        #         for i in selnode:
        #             img = actmat.node_tree.nodes[i.name].image
        #             bpy.data.images[img.name].filepath = ''
        #             refilepath = selpath + '\\' + img.name
        #             bpy.data.images[img.name].filepath = refilepath
        #             print(refilepath)

        #         bpy.ops.image.reload()
        #=================================================================================================================

        # selpath = []                                            #初始化贴图路径
        # context = bpy.context
        # scene = context.scene
        # selfTools = scene.self_Tools                            #调用全局propertygroup参数
        # selpath = selfTools.Tex_path                            #选中贴图路径
        # actobj = bpy.context.active_object
        # actmat = actobj.active_material
        # selnode = bpy.context.selected_nodes
        # print(selnode)

        # if selpath.endswith('\\'):                              #在blender搜索栏选择的路径后缀会自带一个'\'，这里检测后缀是否带'\'，检测到就自动删除，windows复制路径不存在这个问题。
        #     selpath = selpath.rstrip('\\')
        # print(selpath)
        
        # osdirfile = os.listdir(selpath)


        # for file in osdirfile:                                  #用外部文件名称重命名节点名称和节点引用的贴图名称，以替代
        #     for node in selnode:
        #         if re.search(node.name, file, re.IGNORECASE):
        #             print(node.name)
        #             img = actmat.node_tree.nodes[node.name].image

        #             bpy.data.images[img.name].name = file
        #             node.name = file

        #             print('yes')
        #         else:
        #             print(node.name)
        #             print('no')
        #=================================================================================================================



        # selpath = []                                            #初始化贴图路径
        # data = bpy.data
        # context = bpy.context
        # scene = context.scene
        # selfTools = scene.self_Tools                            #调用全局propertygroup参数
        # selpath = selfTools.Tex_path                            #选中贴图路径
        # list_file = os.listdir(selpath)                         #路径中所有贴图list
        # list_fileUP = [i.upper() for i in list_file]
        
        # DIF = 'DIF'
        # ORM = 'ORM'
        # NRM = 'NRM'
        
        # selobj_list = bpy.context.active_object                 #获取选中的模型
        # selobj_name = selobj_list.name_full                      #获取选中模型的名称
        # actmat = bpy.data.objects[selobj_name].active_material   #获取选中模型的材质
        # actmat_name = actmat.name_full
        # actmat_nameUP = actmat_name.upper()
        # nodetree = bpy.data.materials[actmat_name].node_tree
        
        # TexNinMatN = [M for M in list_file if actmat_name in M]         #筛选含有材质关键字的文件
        # TexNinMatNUP = [i.upper() for i in TexNinMatN]
        # SSS_DIF = [T for T in TexNinMatN if DIF in T]                   #筛选含有材质和贴图关键字的文件
        # SSS_ORM = [T for T in TexNinMatN if ORM in T]  
        # SSS_NRM = [T for T in TexNinMatN if NRM in T]
        # SSS_Tex = SSS_DIF + SSS_ORM + SSS_NRM
        # SSSmatIP = ['DIF'] + ['ORM'] + ['NRM']

        # print(SSS_ORM)

        actobj = bpy.context.active_object
        actmat = actobj.active_material
        selobj = bpy.context.selected_objects
        actmat = actobj.active_material

        for obj in selobj:
            print(obj)
            obj.active_material = actmat








        return {'FINISHED'}