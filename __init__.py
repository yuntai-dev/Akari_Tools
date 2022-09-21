'''
Author: your name
Date: 2022-03-16 18:45:46
LastEditTime: 2022-03-17 10:07:42
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \VertexGame_Tools\__init__.py
'''
bl_info = {
	"name": "Vertex Games Tools",
	"description": "Vertex Games常用工具集",
	"author": "Baka_Akari",
	"version": (1, 2, 0),
	"blender": (3, 1, 0),
	"warning": "有部分功能处于测试阶段",
	"doc_url": "http://wiki.jingle.cn/pages/viewpage.action?pageId=134601127",
	"tracker_url": "",
	"category": "3D View"
}
import bpy
import traceback
from bpy.utils import register_class, unregister_class
from bpy.props import (PointerProperty)
from . AddonProps   import addonpropgroup

from . import AddNode
from . import AddonProps
from . import BakeVertexAO
from . import CleanMesh
from . import QuickPhysics
from . import BridgeTools
# from . import AniTools
from . import VGTPreferences
from . import Translation
from . import QuickBindAvatar
# from . import QuickImportRender

def register():
	VGTPreferences.register()
	AddNode.register()
	AddonProps.register()
	BakeVertexAO.register()
	CleanMesh.register()
	QuickPhysics.register()
	BridgeTools.register()
	# AniTools.register()
	Translation.register()
	QuickBindAvatar.register()
	# QuickImportRender.register()

	# bpy.types.TOPBAR_HT_upper_bar.append(Translation.translationdraw)
	bpy.types.STATUSBAR_HT_header.append(Translation.translationdraw)
	# bpy.types.VIEW3D_HT_header.append(QuickImportRender.QuickImportRenderDraw)

	bpy.types.Scene.addonprops = PointerProperty(type=addonpropgroup)
	bpy.types.WindowManager.quick_physics = PointerProperty(type=addonpropgroup)


def unregister():
	VGTPreferences.unregister()
	AddNode.unregister()
	AddonProps.unregister()
	BakeVertexAO.unregister()
	CleanMesh.unregister()
	QuickPhysics.unregister()
	BridgeTools.unregister()
	# AniTools.unregister()
	Translation.unregister()
	QuickBindAvatar.unregister()
	# QuickImportRender.unregister()
	# bpy.types.VIEW3D_HT_tool_header
	bpy.types.STATUSBAR_HT_header.remove(Translation.translationdraw)
	# bpy.types.VIEW3D_HT_header.remove(QuickImportRender.QuickImportRenderDraw)

	del bpy.types.Scene.addonprops
	del bpy.types.WindowManager.quick_physics

if __name__ == "__main__":
    register()
