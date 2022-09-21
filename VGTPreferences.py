from itertools import cycle
import bpy
from bpy.utils import register_class, unregister_class
import os
import zipfile
import getpass
# from .. import MACHIN3tools
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

def updatedraw(self, context):
    layout = self.layout
    if context.preferences.view.language == "en_US":
        Buttonname = "Update Plugin"
    else:
        Buttonname = "升级插件"
    layout.operator(operator="object.vgtimportaddons", text=Buttonname)

class VGTPreferences(bpy.types.AddonPreferences):
    bl_idname = "VertexGame_Tools"
    # test = "软件初始化配置方法："n,"更新插件集按钮：更新公司网盘内的常用插件集版本(仅用常用脚本，额外扩展脚本需要至网盘手动安装)"/N, "设置Blender参数按钮：将Blender设置配置为标准状态(会覆盖部分现有配置)"
    def draw(self, context):
        addonprops = context.scene.addonprops
        layout = self.layout
        # layout.prop(addonprops,'vgtautoipdatepath')
    
        box = layout.box()
        box1 = layout.box()
        boxrow = box1.row()

        box.label(text="功能详情点击上方文档按钮查看")
        layout.prop(addonprops, 'addonaddress', text="插件地址")
        layout.prop(addonprops, 'tutorialaddress', text="教程地址")
        boxrow.operator('object.vgtimportaddons', text="更新插件集")
        boxrow.operator(VGTDefaultSetting.bl_idname,text="设置blender参数")

		
class VGTImportAddons(bpy.types.Operator):
    bl_idname = "object.vgtimportaddons"
    bl_label = "更新插件库"
    
    def execute(self, context):
        keys = []
        newaddonfilepath = context.scene.addonprops.vgtautoipdatepath
        customaddonlist = [
                            'HOps', 
                            'MACHIN3tools', 
                            'MESHmachine',
                            'batch_ops', 
                            'Boxcutter', 
                            'Fix_Quixel_Bridge_Addon', 
                            'GoB', 
                            'Node Kit',
                            'smart_fill',
                            'sculpt_paint_wheel',
                            'better_fbx',
                            'VertexGame_Tools',
                            'Gaffer',
        ]
        defaultaddonlist = [
                            'space_view3d_modifier_tools',
                            'space_view3d_spacebar_menu',
                            'object_collection_manager',
                            'mesh_f2',
                            'mesh_tools',
                            'mesh_looptools',
                            'node_wrangler',
        ]
        for cusadd in customaddonlist:
            print(cusadd)
            bpy.ops.preferences.addon_disable(module=cusadd)

        blenderaddonpath = __file__.split('\\')
        addonpath = '\\'.join(blenderaddonpath[:-2])
        for root,dirs,files in os.walk(newaddonfilepath):
            for f in files:
                if f == "VertexGame_Tools.zip":
                    with zipfile.ZipFile(onlineaddonpath) as zf:
                        zf.extractall(addonpath)
                else:
                    onlineaddonpath = os.path.join(root,f)
                    bpy.ops.preferences.addon_install(overwrite=True, filepath=onlineaddonpath)
                    print(f)
        bpy.ops.script.reload()
        alladdonlist = customaddonlist + defaultaddonlist
        for enab in alladdonlist:
            # print(enab)
            bpy.ops.preferences.addon_enable(module=enab)
#==================================================================================================          
#重设快捷键



        # addontest = bpy.context.window_manager.keyconfigs.addon.keymaps['3D View Generic']
        # for i in addontest.keymap_items:
        #     if i.name == 'MACHIN3: Call MACHIN3tools Pie':
        #         if i.type == 'Q':
        #             i.type = 'A'
                # print(i.idname)
                # print(i.name, i.ctrl, i.shift, i.alt, i.value, i.type)
        # print(addontest)
        
        # addonpre.activate_smart_vert = True

#==========================================================================================
        # if zipfile.is_zipfile(newaddonfilepath):
        #     with zipfile.ZipFile(newaddonfilepath) as zf:
        #         zf.extractall(addonpath)
        # else:
        #     self.report({'ERROR'},'选择.zip文件')

        return{'FINISHED'}

def register_keymap(keyid,ty,alt,shift,value):
    addon_keymaps = VGTDefaultSetting.addon_keymaps
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name = "Window",space_type='EMPTY', region_type='WINDOW')
    kmi = km.keymap_items.new(keyid, type = ty, alt=alt, shift=shift, value = value)
    # kmi.properties.name = "editor_switcher_pie_menu"
    addon_keymaps.append(km)

class VGTDefaultSetting(bpy.types.Operator):
    bl_idname = "object.vgtdefaultsetting"
    bl_label = "导入初始设置(会覆盖现有设置)"
    addon_keymaps = []

    @classmethod
    def poll(cls, context):
        return True
    

    def execute(self, context):
#=====================================================================================
#设置machin3tools默认配置
        addonpre = bpy.context.preferences.addons['MACHIN3tools'].preferences
        addonpre.activate_smart_vert = True
        addonpre.activate_smart_edge = True
        addonpre.activate_smart_face = True
        addonpre.activate_clean_up = True
        addonpre.activate_edge_constraint = True
        addonpre.activate_extrude = True
        addonpre.activate_focus = True
        addonpre.activate_mirror = True
        addonpre.activate_align = True
        addonpre.activate_group = True
        addonpre.activate_smart_drive = True
        addonpre.activate_assetbrowser_tools = True
        addonpre.activate_filebrowser_tools = True
        addonpre.activate_render = True
        addonpre.activate_smooth = True
        addonpre.activate_clipping_toggle = True
        addonpre.activate_surface_slide = True
        addonpre.activate_material_picker = True
        addonpre.activate_apply = True
        addonpre.activate_select = True
        addonpre.activate_mesh_cut = True
        addonpre.activate_thread = True
        addonpre.activate_unity = True
        addonpre.activate_customize = True

        addonpre.activate_modes_pie = True
        addonpre.activate_save_pie = True
        addonpre.activate_shading_pie = True
        addonpre.activate_views_pie = True
        addonpre.activate_align_pie = True
        addonpre.activate_cursor_pie = True
        addonpre.activate_transform_pie = True
        addonpre.activate_snapping_pie = True
        addonpre.activate_collections_pie = True
        addonpre.activate_workspace_pie = True
        addonpre.activate_tools_pie = True

#=====================================================================================
#复制指定目录里的配置文件至配置文件夹内
#已废弃
        # newaddonfilepath = context.scene.addonprops.vgtautoipdatepath
        # blenderaddonpath = __file__.split('\\')
        # # print(newaddonfilepath)
        # sourceF = '\\'.join(blenderaddonpath[:-1])+'\\config'
        # targetF = '\\'.join(blenderaddonpath[:-4])+'\\config'
        # shutil.copytree(sourceF,targetF)

#=====================================================================================
# 设置cycles渲染设备
        cyclespref = bpy.context.preferences.addons['cycles'].preferences
        cyclespref.compute_device_type = 'OPTIX'

#修改默认配置选项至可用状态
        prefview = context.preferences.view
        prefsys = context.preferences.system
        prefinp = context.preferences.inputs
        prefedit = context.preferences.edit
#界面设置
        prefview.show_developer_ui = True
        prefview.show_tooltips_python = True
        prefview.show_statusbar_memory = True
        prefview.show_statusbar_stats = True
        prefview.show_statusbar_vram = True
#视图设置 
        prefview.show_object_info = False
        prefview.show_view_name = False
        prefsys.viewport_aa = "32"
        prefsys.anisotropic_filter = "FILTER_16"
#视图切换设置
        prefinp.use_mouse_depth_navigate = True

        context.preferences.view.language = "zh_CN"
        prefview.use_translate_new_dataname = False
#系统设置
        prefedit.undo_steps = 256

#=====================================================================================
#存储用户设置
        bpy.ops.preferences.associate_blend()
        bpy.ops.wm.save_userpref()

#=====================================================================================
# 设置快捷键
        winmankeys = bpy.data.window_managers["WinMan"].keyconfigs
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.addon
        for key in winmankeys:
            if key.name == "Blender addon":
                for keymap in key.keymaps:
                    if keymap.name == "3D View":
                        for keyitem in keymap.keymap_items:
                            if keyitem.idname == "wm.call_menu_pie":
                                # def register():
                                # km = kc.keymaps.new(name="3D View")
                                # kc.keymaps["3D View"].keymap_items.new("wm.call_menu_pie", type = "Q", value = "PRESS", ctrl = True, shift = True)

                                # bpy.data.window_managers["WinMan"].keyconfigs["Blender addon"].keymaps["3D View"].keymap_items["wm.call_menu_pie"].ctrl = True
                                # keyitem.key_modifier = "Q"
                                register_keymap("wm.call_menu_pie","Q",True,True,"PRESS")
                                # print(keyitem.ctrl_ui)
                                # keyitem.is_user_modified = True
                            # if keyitem.idname == "wm.call_menu":
                            #     # km = kc.keymaps.new(name="3D View")
                            #     kc.keymaps["3D View"].keymap_items.new("wm.call_menu", type = "Q", value = "PRESS", ctrl = False, shift = True)

                                # keyitem.shift_ui = True
                    # if keymap.name == "Object Non-modal":
                    #     for keyitem in keymap.keymap_items:
                    #         if keyitem.idname == "wm.call_menu_pie":
                    #             # km = kc.keymaps.new(name="3D View")
                    #             kc.keymaps["3D View"].keymap_items.new("wm.call_menu_pie", type = "Q")

                                # keyitem.type = "Q"
                    # if keymap.name == "Image":
                    #     for keyitem in keymap.keymap_items:
                    #         if keyitem.idname == "wm.call_menu_pie":
                    #             # km = kc.keymaps.new(name="3D View")
                    #             kc.keymaps["3D View"].keymap_items.new("wm.call_menu_pie", type = "Q")

                                # keyitem.type = "Q"
        # MACHIN3toolsPreferences.activate_smart_vert()

        # def update_activate_shading_pie(self, context):
        #     activate(self, register=self.activate_shading_pie, tool="shading_pie")


        return{'FINISHED'}


    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    

classes = (VGTPreferences,
            VGTImportAddons,
            VGTDefaultSetting,
            )
# addonkeymap = bpy.data.window_managers["WinMan"].keyconfigs["Blender addon"]
def register():
    global classes
    for cls in classes:
        register_class(cls)
    
    bpy.types.STATUSBAR_HT_header.append(updatedraw)
    # bpy.data.window_managers["WinMan"].keyconfigs["Blender addon"].keymaps["3D View"].keymap_items["wm.call_menu_pie"].ctrl = True
    # bpy.data.window_managers["WinMan"].keyconfigs["Blender addon"].keymaps["3D View"].keymap_items["wm.call_menu"].shift = True
    # bpy.data.window_managers["WinMan"].keyconfigs["Blender addon"].keymaps["Object Non-modal"].keymap_items["wm.call_menu_pie"].type = "Q"
    # bpy.data.window_managers["WinMan"].keyconfigs["Blender addon"].keymaps["Image"].keymap_items["wm.call_menu_pie"].type = "Q"
    



def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)

    bpy.types.STATUSBAR_HT_header.remove(updatedraw)
