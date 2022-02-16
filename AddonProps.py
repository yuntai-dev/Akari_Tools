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

    ### physics box
    box_physics: BoolProperty(description="Show/Hide Physics Box", default=True)

    canvas_all: BoolProperty(description="Use any object as Canvas", default=False)

    physics_friction: FloatProperty(description="Friction Value that is used for phyics calculation.", default=0.5,
                                     min=0.0, max=1.0)
    running_physics_calculation: BoolProperty(description="", default=False)
    physics_time_scale: FloatProperty(
        description="Time Scale that is used for calculation. Smaller Values are more accurate, but take longer to calculate.",
        default=5.0, min=0.0, max=20.0)
