bl_info = {
    "name" : "Akari_Tools_re",
    "author" : "Akari",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "Test",
    "category" : ""
}
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

from . CleanMesh import CleanMeshPanel,CleanMeshOperator
from . BatchRename  import BatchRenamePanel,BatchRenameOperator
from . AddNode  import AddNodePanel,ImportBaseMatOperator,ImportHDRImatOperator,ImportImageOperator,ReloadImageOperator
from . SwichMaterial    import SwitchMaterialPanel,SwitchMaterialOperator,RenameOutputMaterialOperator,outputmatlist
from . AddonProps   import addonpropgroup

classes = (addonpropgroup,
            CleanMeshPanel,
            CleanMeshOperator,
            BatchRenamePanel,
            BatchRenameOperator,
            AddNodePanel,
            ImportBaseMatOperator,
            ImportHDRImatOperator,
            ImportImageOperator,
            ReloadImageOperator,
            SwitchMaterialPanel,
            SwitchMaterialOperator,
            RenameOutputMaterialOperator,
            )

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.addonprops = PointerProperty(type=addonpropgroup)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    del bpy.types.Scene.addonprops

if __name__ == "__main__":
    register()