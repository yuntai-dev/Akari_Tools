import bpy
from bpy.utils import register_class, unregister_class
from bpy.props import (StringProperty,
                       BoolProperty,
                       FloatProperty
                       )
from bpy.types import (
                       PropertyGroup,
                       )

class addonpropgroup(PropertyGroup):
    addimage_path: StringProperty(
        name='Path',
        description='',
        default='',
        maxlen=1024,
        subtype='FILE_PATH'
        )
    vgtautoipdatepath: StringProperty(
        name='Addon Path',
        description='',
        # default='\\10.234.36.135\share\美术资源\Software 软件\Blender插件\【Vertex Games Tools】',
        default='\\\\10.32.94.135\\share\\10.美术空间\\006.美术资料\\Software 软件\\Blender插件\\【Vertex Games Tools】',
        
        maxlen=1024,
        subtype='FILE_PATH'
        )

    renamemat: StringProperty(
        name='Material',
        description='New Material Name',
        default='',
        maxlen=1024,
        subtype='FILE_NAME'
        )

    addonaddress: StringProperty(
        name='addonaddress',
        description='',
        default='\\\\10.234.36.135\\share\\006.美术资料\\Software 软件\\Blender插件',
        maxlen=1024,
        subtype='NONE'
        )
    tutorialaddress: StringProperty(
        name='addonaddress',
        description='',
        default='\\\\10.234.36.135\\share\\006.美术资料\\Software 软件\\Blender插件\\Blender教程视频',
        maxlen=1024,
        subtype='NONE'
        )



    
                                    
    ### physics box
    box_physics: BoolProperty(
        description="Show/Hide Physics Box", 
        default=True
        )

    canvas_all: BoolProperty(
        description="Use any object as Canvas", 
        default=False
        )

    physics_friction: FloatProperty(
        description="Friction Value that is used for phyics calculation.", 
        default=0.5,
        min=0.0, max=1.0
        )
    running_physics_calculation: BoolProperty(
        description="", 
        default=False
        )
    physics_time_scale: FloatProperty(
        description="Time Scale that is used for calculation. Smaller Values are more accurate, but take longer to calculate.",
        default=5.0, min=0.0, max=20.0
        )

classes = (addonpropgroup)

def register():
    register_class(addonpropgroup)

def unregister():
    unregister_class(addonpropgroup)