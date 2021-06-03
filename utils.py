# '''
# Author: your name
# Date: 2021-06-03 10:16:03
# LastEditTime: 2021-06-03 10:36:31
# LastEditors: Please set LastEditors
# Description: In User Settings Edit
# FilePath: \Akari_Tools\utils.py
# '''
import bpy
from bpy.utils import register_class, register_classes_factory
from . Test       import Test_OP2Operator
from . My_PropertyGroup   import MyProperties

class globle_utils(bpy.types.Operator):
    bl_idname = "utils.globle"
    bl_label = "utils"

    def execute(self,Context):
        actobj = bpy.context.active_object
        selobj = bpy.context.selected_objects
        actmat = actobj.active_material.name_full
        nodeslist = bpy.data.materials[actmat].node_tree.nodes
        outputlist = []
        for i in nodeslist:
            if i.type == 'OUTPUT_MATERIAL':
                outputname = i.name
                outputlist.append(outputname)
        Test_OP2Operator.OPlist = outputlist
        MyProperties.OPlist = outputlist
        Test_OP2Operator.actobj = actobj
        MyProperties.mat_enumset(self)


        return{'FINISHED'}
