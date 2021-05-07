'''
Author: your name
Date: 2021-04-21 16:05:24
LastEditTime: 2021-04-21 19:35:52
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Akari_Toolbag\Test.py
'''
import bpy
from mathutils import *
D = bpy.data
C = bpy.context


class Test_OPOperator(bpy.types.Operator):
    bl_idname = "object.test_op"
    bl_label = "Test_OP"


    def execute(self, context):
        test1 = ['111','222','333']
        test2 = ['111','222','333','444']

        return {'FINISHED'}