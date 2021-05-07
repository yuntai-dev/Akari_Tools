'''
Author: your name
Date: 2021-04-19 12:05:27
LastEditTime: 2021-04-19 18:19:48
LastEditors: your name
Description: In User Settings Edit
FilePath: \Test_addon\My_PropertyGroup.py
'''
import bpy
from mathutils import *
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

class MyProperties(PropertyGroup):
    my_bool: BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )
    my_int: IntProperty(
        name = "Int Value",
        description="A integer property",
        default = 23,
        min = 10,
        max = 100
        )
    my_float: FloatProperty(
        name = "Float Value",
        description = "A float property",
        default = 23.7,
        min = 0.01,
        max = 30.0
        )
    my_float_vector: FloatVectorProperty(
        name = "Float Vector Value",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= 0.0, # float
        max = 0.1
    ) 
    my_string: StringProperty(
        name="User Input",
        description=":",
        default="",
        maxlen=1024,
        )
    Tex_path: StringProperty(
        name = "Directory",
        description="Choose a directory:",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
        )
    Ept_to_mar_path: StringProperty(
        name = "marmosetpath",
        description="Choose a directory:",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
        )
    my_enum: EnumProperty(
        name="Dropdown:",
        description="Apply Data to attribute.",
        items=[ ('OP1', "Option 1", ""),
                ('OP2', "Option 2", ""),
                ('OP3', "Option 3", ""),
               ]
        )
    my_test = 'test_test'