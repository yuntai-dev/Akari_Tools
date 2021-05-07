# context.area: IMAGE_EDITOR

import bpy
    
class EditUVchannelOperator(bpy.types.Operator):
    bl_idname = "object.edituvchannel"
    bl_label = "editUVchannel"

    def execute(self, context):
        sel = bpy.context.selected_objects
        act = bpy.context.active_object
        name = act.data.uv_layers
        lis = list(name)

        print(name)
        print(lis)
        # for act in sel:
            # print(bpy.data.meshes['act'].uv_layers.active_index)
            # type(sel)
            # print(act)
            # print(1)

        # print(sel)
        return {'FINISHED'}
