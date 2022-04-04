'''
Author: your name
Date: 2022-03-16 18:45:46
LastEditTime: 2022-03-17 10:07:42
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \akari_tools\__init__.py
'''
bl_info = {
	"name": "Akari Tools",
	"description": "Demo addon for showcasing the blender-addon-updater module",
	"author": "Patrick W. Crawford, neomonkeus",
	"version": (1, 1, 4),
	"blender": (3, 1, 0),
	"location": "View 3D",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": ""
}
import bpy
import traceback
from bpy.utils import register_class, unregister_class
from bpy.props import (PointerProperty)
from . AddonProps   import addonpropgroup

# from . CleanMesh import ToolsPanel,CleanMeshOperator,BatchRenameOperator,BatchSetOriginOperator
# from . AddNode  import AddNodePanel,ImportBaseMatOperator,ImportHDRImatOperator,ImportImageOperator,ACESTexToolOperator,ACES_PT_Panel
# from . QuickPhysics    import PhysicsPanel,ASSET_SKETCHER_OT_CalcPhysics,ASSET_SKETCHER_OT_AddActivePhysics,ASSET_SKETCHER_OT_ApplyPhysics
# from . BakeVertexAO    import BakeVertexAOPanel,BakeVertexAOOperator,AOChangeChannelOperator


# classes = (
# 			addonpropgroup,
#             ToolsPanel,
#             CleanMeshOperator,
#             BatchRenameOperator,
#             BatchSetOriginOperator,
#             AddNodePanel,
#             ImportBaseMatOperator,
#             ImportHDRImatOperator,
#             ImportImageOperator,
#             ACESTexToolOperator,
# 			ACES_PT_Panel,
#             PhysicsPanel,
#             ASSET_SKETCHER_OT_CalcPhysics,
#             ASSET_SKETCHER_OT_AddActivePhysics,
#             ASSET_SKETCHER_OT_ApplyPhysics,
#             BakeVertexAOPanel,
#             BakeVertexAOOperator,
#             AOChangeChannelOperator,
#             )

# def register():
# 	from bpy.utils import register_class
# 	for cls in classes:
# 		register_class(cls)
# 	bpy.types.Scene.addonprops = PointerProperty(type=addonpropgroup)
# 	bpy.types.WindowManager.asset_sketcher = PointerProperty(type=addonpropgroup)



# def unregister():
# 	from bpy.utils import unregister_class
# 	for cls in classes:
# 		unregister_class(cls)
# 	del bpy.types.Scene.addonprops
# 	del bpy.types.WindowManager.asset_sketcher

# if __name__ == "__main__":
#     register()

from . import AddNode
from . import AddonProps
from . import BakeVertexAO
from . import CleanMesh
from . import QuickPhysics
from . import BridgeTools
from . import AniTools

def register():
	AddNode.register()
	AddonProps.register()
	BakeVertexAO.register()
	CleanMesh.register()
	QuickPhysics.register()
	BridgeTools.register()
	AniTools.register()

	bpy.types.Scene.addonprops = PointerProperty(type=addonpropgroup)
	bpy.types.WindowManager.asset_sketcher = PointerProperty(type=addonpropgroup)


def unregister():
	AddNode.unregister()
	AddonProps.unregister()
	BakeVertexAO.unregister()
	CleanMesh.unregister()
	QuickPhysics.unregister()
	BridgeTools.unregister()
	AniTools.unregister()

	del bpy.types.Scene.addonprops
	del bpy.types.WindowManager.asset_sketcher

if __name__ == "__main__":
    register()
