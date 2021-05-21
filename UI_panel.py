'''
Author: your name
Date: 2020-10-05 00:06:21
LastEditTime: 2021-05-21 14:24:36
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Addon\panel.py
'''
import bpy
from . AddonPropertyGroup   import MyProperties
# from . Import_Operator       import Import_Texture_Maps

#####draw panel#####
class Add_Nodegroups(bpy.types.Panel):
    bl_idname = "SSS_Nodegroups"
    bl_label = "Akari Tools"
    bl_category = "SSS Node"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"

    def draw(self,context):
        layout = self.layout
        row = layout.row()
        scene = context.scene
        selfTools = scene.self_Tools
        
        row = layout.row()
        row.label(text='HDRI')
        row.operator('hdri.nodegroup')
        
        row = layout.row()
        row.label(text='SSSmat')
        row.operator('mat.sssnodegroup')
        
        layout.label(text="Textuer Path")
        layout.prop(selfTools, "Tex_path")
        layout.operator("object.relocate_image")
        layout.operator("import.texmap")

        box = layout.box()
        row = box.row()
        row.label(text='Reload Image')
        row.operator('reload.tex')

        box = layout.box()
        box.label(text='NodeTest Button')
        box.operator('object.test_op')

class SimpleTools(bpy.types.Panel):
    bl_idname = "SSS_Simple_Tools"
    bl_label = "Akari Tools"
    bl_category = "SSS Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self,context):
        return context.object
    def draw(self,context):
        layout = self.layout
        column = layout.column()

        scene = context.scene
        selfTools = scene.self_Tools


        box = layout.box()
        box.label(text='3D Module')
        editbox = box.box()
        row = editbox.row()
        row.operator('parallel.edit')
        row.operator('loop.edit')
        row = editbox.row()
        row.operator('object.cleannormal')

        box = layout.box()
        box.label(text='Bake Module')
        bakefirstbox = box.box()
        row = bakefirstbox.row()
        bakescendbox = bakefirstbox.box()
        row.label(text="Batch Rename")
        row.operator('collection.rename')
        bakescendbox.label(text='Export to Marmoset')
        bakescendbox.prop(selfTools, "Ept_to_mar_path")
        bakescendbox.operator('export.marmoset')

        
        box = layout.box()
        boxrow = box.row()
        box.label(text='3DTest Button')
        box.operator('object.test_op')



class UVTools(bpy.types.Panel):
    bl_idname = "SSS_UV_Tools"
    bl_label = "Akari Tools"
    bl_category = "SSS Tools"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"

    def draw(self,context):
        layout = self.layout

        row = layout.row()
        row.label(text='UV')
        row.operator('object.edituvchannel')



