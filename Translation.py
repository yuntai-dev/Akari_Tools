'''
Author: Baka_Akari exwww2000@qq.com
Date: 2022-05-29 15:52:44
LastEditors: Baka_Akari exwww2000@qq.com
LastEditTime: 2022-08-07 10:54:30
FilePath: \fixshotcute:\SynologyDrive\Python\VertexGame_Tools\Translation.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import bpy
from bpy.utils import register_class, unregister_class

def translationdraw(self, context):
    layout = self.layout
    # row = layout.row(align=True)
    if context.preferences.view.language == "en_US":
        Buttonname = "Switch CH"
    else:
        Buttonname = "切换英文"
    layout.operator(operator="object.translationoperation", text=Buttonname)
    # layout.operator(operator="object.translationoperation")

        # return super().draw(context)

class TranslationOperation(bpy.types.Operator):
    bl_idname = "object.translationoperation"
    bl_label = "切换中英文"

    def execute(self, context):
        viewlanguage = context.preferences.view.language
        prefview = context.preferences.view
        if viewlanguage == "zh_CN":
            context.preferences.view.language = "en_US"
        else:
            context.preferences.view.language = "zh_CN"
            prefview.use_translate_new_dataname = False


        return{'FINISHED'}

classes = (TranslationOperation,
            )

def register():
    global classes
    for cls in classes:
        register_class(cls)
    # bpy.types.TOPBAR_HT_upper_bar.append(translationdraw)
    

def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)
    # bpy.types.TOPBAR_HT_upper_bar.remove(translationdraw)
    