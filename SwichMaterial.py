import bpy
from bpy import props
from bpy.types import Object, Scene
from mathutils import *

def outputmatlist(self,context):
    #这里应该写个判断排除目前没有选择激活物体或者物体没有材质，现在会在后台报错
    outmatlist = []
    actobj = bpy.context.active_object
    actmat = actobj.active_material

    if type(actobj) == Object:
        if len(actobj.material_slots) > 0:
            actnodetree = bpy.data.materials[actmat.name].node_tree.nodes
            for i in list(actnodetree):
                if i.type == 'OUTPUT_MATERIAL':
                    outmatlist.append(i)
            return [(i.name, i.name, "") for i in outmatlist]
        else:
            return
    else:
        return

class SwitchMaterialPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_SwitchMaterial"
    bl_label = "Switch Material"
    bl_category = "NodeTools"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"

    def draw(self, context):
        addonprops = context.scene.addonprops
        layout = self.layout
        row = layout.row()
        layout.prop(addonprops,'renamemat')
        layout.operator('object.renameoutputmaterial')
        layout.prop(addonprops,'OMlist')
        layout.operator('object.switchmaterial')
        return 


class RenameOutputMaterialOperator(bpy.types.Operator):
    bl_idname = "object.renameoutputmaterial"
    bl_label = "Rename Output Material"

    def execute(self, context):
        actobj = bpy.context.active_object
        actmat = actobj.active_material
        actnode = actmat.node_tree.nodes.active
        actscene = bpy.context.scene
        namedata = bpy.data.scenes[actscene.name].addonprops.renamemat
        bpy.data.materials[actmat.name].node_tree.nodes[actnode.name].name = namedata
        bpy.data.materials[actmat.name].node_tree.nodes[actnode.name].label = namedata
        return {'FINISHED'}

class SwitchMaterialOperator(bpy.types.Operator):
    bl_idname = "object.switchmaterial"
    bl_label = "Switch Material"

    def execute(self, context):
        actobj = bpy.context.active_object
        actmat = actobj.active_material
        actscene = bpy.context.scene
        allmat = bpy.data.materials
        OPdata = bpy.data.scenes[actscene.name].addonprops.OMlist
        OPmatlist = list(bpy.data.materials)
        for mat in OPmatlist:
            for i in mat.node_tree.nodes:
                if i.type == 'OUTPUT_MATERIAL':
                    i.is_active_output = False
        for i in allmat:
            for x in list(i.node_tree.nodes):
                if x.type == 'OUTPUT_MATERIAL':
                    if x.name == OPdata:
                        x.is_active_output = True
        return {'FINISHED'}
