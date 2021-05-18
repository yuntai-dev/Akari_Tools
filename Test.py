'''
Author: your name
Date: 2021-04-21 16:05:24
LastEditTime: 2021-05-18 13:50:26
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Akari_Toolbag\Test.py
'''
import bpy
from mathutils import *
import re

D = bpy.data
C = bpy.context


class Test_OPOperator(bpy.types.Operator):
    bl_idname = "object.test_op"
    bl_label = "Test_OP"


    def execute(self, context):

        # my_str = "abc .abc .abc1-abc3"
        # str = 'ab'
        # strlen = len(str)
        # my_list = ['t1','t2','t3','t4','t']
        # old="abc"
        # new = "xxx"

        # result = re.sub("\\b" + old + "\\b", new, my_str)
        # result3 = re.sub(r"\b%s\b" % (old), new, my_str)
        # result2 = re.sub("\." + "\\b" + "abc" + "\\b", new, my_str)
        # result1 = re.findall("\." + "\\b" + "abc" + "\\b",my_str)

        # test1 = re.search('3$',my_str)
        # print(test1)
        # print(type(test1))

        # bpy.ops.object.empty_add(type='CUBE', align='WORLD', location=(0.0859147, -0.00213459, 0.139307), scale=(1, 1, 1))
        print(cursor.location)

        # put the location to the folder where the objs are located here in this fashion
        #path_to_obj_dir = os.path.join('C:\\', 'Users', 'YOUR_NAME', 'Desktop', 'OBJS') #<-WINDOWS_OS
        path_to_obj_dir = bpy.path.abspath('//OBJ/')



        return {'FINISHED'}