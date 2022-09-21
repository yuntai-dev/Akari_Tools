from xml.etree.ElementTree import iselement
import bpy
import os
import re
from bpy.utils import register_class, unregister_class


# class QuickImportRenderPanel(bpy.types.Panel):
def QuickImportRenderDraw(self, context):
    layout = self.layout
    if context.preferences.view.language == "en_US":
        Buttonname = "Import SC"
    else:
        Buttonname = "导入SC模型"
        layout.operator(operator='object.quickimportrender', text=Buttonname)

class QuickImportRenderOperator(bpy.types.Operator):
    bl_idname = "object.quickimportrender"
    bl_label = "快速导入渲染"

    def execute(self,context):
        path = "C://Users//Admin//AppData//Local//Temp//SCtemp"
        isExists = os.path.exists(path)
        if isExists:
            for root, dirs, files in os.walk(path, topdown=True):
                for obj in files:
                    if obj == "SC.obj":
                        objpath = path.replace('//', "\\")+"\\"+obj
                        bpy.ops.import_scene.obj(filepath=objpath, filter_glob='*.obj;*.mtl')
                        print(obj)


            return{'FINISHED'}


classes = (QuickImportRenderOperator,
            )

def register():
    global classes
    for cls in classes:
        register_class(cls)

def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)