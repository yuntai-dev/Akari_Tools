'''
Author: your name
Date: 2021-04-21 16:05:24
LastEditTime: 2021-06-03 14:38:06
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Akari_Tools\Test.py
'''
import numpy as np
import bpy
import os
import mathutils
# from . utils    import globle_utils
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

D = bpy.data
C = bpy.context
O = bpy.ops

class Test_OPOperator(bpy.types.Operator):
    bl_idname = "object.test_op"
    bl_label = "Test_OP"

    def execute(self, context):
        global outputlist
        actobj = bpy.context.active_object
        selobj = bpy.context.selected_objects
        actmat = actobj.active_material.name_full
        nodeslist = bpy.data.materials[actmat].node_tree.nodes
        outputlist = []
        for i in nodeslist:
            if i.type == 'OUTPUT_MATERIAL':
                outputname = i.name
                outputlist.append(outputname)
        bpy.types.Scene.nodeslist = outputlist

        selout = bpy.data.materials[actmat].node_tree.nodes[0]
        seloutloc = selout
        # seloutlocX = list(seloutloc)
        # seloutlocY = list(seloutloc)[1]
        print(outputlist)
        bpy.ops.node.select(wait_to_deselect_others=True, mouse_x=391, mouse_y=176, extend=False, deselect_all=True)

        return {'FINISHED'}

class Test_OP2Operator(bpy.types.Operator):
    bl_idname = "object.test_op2"
    bl_label = "Test_OP2"
    actobj = ()
    OPlist = []
    
    def execute(self, context):
        actobj = self.actobj
        OPlist = self.OPlist
        print(actobj)
        print(OPlist)
        return {'FINISHED'}