from typing import Collection
import bpy
from bpy.types import CollectionChildren

class OBJECT_OT_CustomOp(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    def execute(self, context):
        print("test")
        actobj = bpy.context.active_object
        actcoll = bpy.data.collections
        for colls in actcoll:
            collsobj = bpy.data.collections[colls.name].all_objects
            for incollobj in collsobj:
                if actobj.name == incollobj.name:
                    Collectionname = colls.name

        layer_collection = bpy.context.view_layer.layer_collection.children[Collectionname]
        bpy.context.view_layer.active_layer_collection = layer_collection
        allactcollobj = bpy.data.collections[Collectionname].all_objects
        for obj in allactcollobj:
            print(obj.name)
            obj.select_set(True)
        return {'FINISHED'}
