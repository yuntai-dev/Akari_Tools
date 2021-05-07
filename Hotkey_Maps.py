'''
Author: your name
Date: 2021-04-21 18:55:08
LastEditTime: 2021-04-21 18:55:08
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Akari_Toolbag\Hotkey_Maps.py
'''
'''
Author: your name
Date: 2021-04-21 10:53:37
LastEditTime: 2021-04-21 13:56:07
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Akari_Toolbag\Hotkey_Maps.py
'''
import bpy
from mathutils import *
D = bpy.data
C = bpy.context


class HotkeyOperator(bpy.types.Operator):
    bl_idname = "object.hotkey"
    bl_label = "Hotkey"
    addon_keymaps = []
    print('Test')
    # def execute():

    def register():
        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='choose',space_type='NODE_EDITOR')
        kmi = km.keymap_items.new('object.choose_tex',type='F',value='ANY',shift=False)
        print(km)
        print(kmi.values)

        return {'FINISHED'}

        