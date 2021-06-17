import bpy
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
                       ShaderNodeLightFalloff,
                       Context,
                       Scene,
                       )
from . SwichMaterial    import outputmatlist

class addonpropgroup(PropertyGroup):
    addimage_path: StringProperty(
        name='Path',
        description='',
        default='',
        maxlen=1024,
        subtype='DIR_PATH'
        )

    renamemat: StringProperty(
        name='Material',
        description='New Material Name',
        default='',
        maxlen=1024,
        subtype='FILE_NAME'
        )
                                    
    OMlist: EnumProperty(
        name='test',
        description='testdes',
        items=outputmatlist)