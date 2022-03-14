import bpy
from bpy.utils import register_class, unregister_class
from mathutils import *
D = bpy.data
C = bpy.context

class BridgeToolsPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_BridgeTools"
    bl_label = "Bridge Tools"
    bl_category = "Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_order = 15
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        layout.operator('object.bridgetools')


class BridgeToolsOperator(bpy.types.Operator):
    bl_idname = "object.bridgetools"
    bl_label = "切换贴图映射方式"

    def execute(self, context):
        actobj = bpy.context.active_object
        actmat = actobj.active_material
        links = bpy.data.materials[actmat.name].node_tree.links
        for node in  actmat.node_tree.nodes:
            if node.type == "TEX_COORD":
                texcoordnode = node
            if node.type == "MAPPING":
                texmapping = node
            if node.type == "TEX_IMAGE":
                if node.projection == "BOX":
                    node.projection = "FLAT"
                    links.new(texcoordnode.outputs["UV"],texmapping.inputs["Vector"])
                elif node.projection == "FLAT":
                    node.projection = "BOX"
                    links.new(texcoordnode.outputs["Object"],texmapping.inputs["Vector"])
        return {'FINISHED'}

classes = (BridgeToolsPanel,
            BridgeToolsOperator
            )

def register():
    global classes
    for cls in classes:
        register_class(cls)

def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)