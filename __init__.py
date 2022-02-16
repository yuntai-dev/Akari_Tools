bl_info = {
    "name" : "Akari",
    "author" : "Akari",
    "description" : "",
    "blender" : (2, 93, 0),
    "version" : (0, 0, 3),
    "location" : "",
    "warning" : "",
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

from . AddonProps   import addonpropgroup
from . AddonPreferences import AkaritoolsPreferences
from . CleanMesh import ToolsPanel,CleanMeshOperator,BatchRenameOperator,BatchSetOriginOperator
from . AddNode  import AddNodePanel,ImportBaseMatOperator,ImportHDRImatOperator,ImportImageOperator,ReloadImageOperator
from . SwichMaterial    import SwitchMaterialPanel,SwitchMaterialOperator,RenameOutputMaterialOperator,outputmatlist
from . QuickPhysics    import PhysicsPanel,ASSET_SKETCHER_OT_CalcPhysics,ASSET_SKETCHER_OT_AddActivePhysics,ASSET_SKETCHER_OT_ApplyPhysics
from . BakeVertexAO    import BakeVertexAOPanel,BakeVertexAOOperator,AOChangeChannelOperator
from . GoH  import GoHPanel,GoHOperator
from . SetingSync   import SettingSyncPanel,SettingSyncOPOperator
from . SelectCollObj    import OBJECT_OT_CustomOp

classes = (addonpropgroup,
            AkaritoolsPreferences,
            ToolsPanel,
            CleanMeshOperator,
            BatchRenameOperator,
            BatchSetOriginOperator,
            AddNodePanel,
            ImportBaseMatOperator,
            ImportHDRImatOperator,
            ImportImageOperator,
            ReloadImageOperator,
            SwitchMaterialPanel,
            SwitchMaterialOperator,
            RenameOutputMaterialOperator,
            PhysicsPanel,
            ASSET_SKETCHER_OT_CalcPhysics,
            ASSET_SKETCHER_OT_AddActivePhysics,
            ASSET_SKETCHER_OT_ApplyPhysics,
            BakeVertexAOPanel,
            BakeVertexAOOperator,
            AOChangeChannelOperator,
            GoHPanel,
            GoHOperator,
            SettingSyncPanel,
            SettingSyncOPOperator,
            OBJECT_OT_CustomOp,
            )

addon_keymaps = []

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.addonprops = PointerProperty(type=addonpropgroup)
    bpy.types.WindowManager.asset_sketcher = PointerProperty(type=addonpropgroup)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(OBJECT_OT_CustomOp.bl_idname, type='W', value='PRESS', ctrl=True)
        addon_keymaps.append((km, kmi))



def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    del bpy.types.Scene.addonprops
    del bpy.types.WindowManager.asset_sketcher
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()