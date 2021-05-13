'''
Author: your name
Date: 2020-10-01 17:47:39
LastEditTime: 2021-05-13 11:52:59
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Addon\__init__.py
'''
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Akari Toolbag",
    "author" : "Baka_Akari",
    "description" : "Akari Toolbag",
    "blender" : (2, 90, 0),
    "version" : (0, 0, 1, 3),
    "location" : "",
    "warning" : "Developing",
    "category": "3D View"
}

import bpy
from bpy.props import (StringProperty,BoolProperty,IntProperty,FloatProperty,FloatVectorProperty,EnumProperty,PointerProperty,)
from bpy.types import (Panel,Menu,Operator,PropertyGroup,)

from . Test                 import Test_OPOperator
from . UI_panel             import Add_Nodegroups,SimpleTools,UVTools
from . Node_Tools           import Import_Hdri_node,Import_SSS_mat,Import_Texture_Maps,Choose_TexOperator,ReloadTex
from . View3D_Tools         import Collection_rename,LoopEdit,ParallelEdit,CleanNormalOperator
from . UV_Tools             import EditUVchannelOperator
from . My_PropertyGroup     import MyProperties
from . Export_to_marmoset   import Export_To_Marmoset


classes = (
    Test_OPOperator,
    Add_Nodegroups,
    SimpleTools,
    UVTools,
    MyProperties,
    Import_Hdri_node,
    Import_SSS_mat,
    Collection_rename,
    LoopEdit,
    ParallelEdit,
    EditUVchannelOperator,
    Import_Texture_Maps,
    Export_To_Marmoset,
    ReloadTex,
    Choose_TexOperator,
    CleanNormalOperator,
)
print('test')

def register():
    print('register')
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)
    bpy.types.Scene.self_Tools = PointerProperty(type=MyProperties)
    
    # bpy.ops.script.reload()
    # bpy.ops.script.reload()
    # choosekeymap = []



def unregister():
    print('unregister')
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    del bpy.types.Scene.self_Tools

    cho = Choose_TexOperator.cho
    choi = Choose_TexOperator.choi
    choosekeymap = Choose_TexOperator.choosekeymap

    for cho,choi in choosekeymap:
        cho.keymap_items.remove(choi)
    choosekeymap.clear()





    