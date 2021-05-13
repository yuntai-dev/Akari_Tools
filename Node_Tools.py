'''
Author: your name
Date: 2020-10-04 22:32:46
LastEditTime: 2021-05-13 11:23:57
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Addon\Import_Hdri.py
'''
import numpy as np
import bpy
import os
import mathutils
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

from . My_PropertyGroup     import MyProperties

D = bpy.data
C = bpy.context
O = bpy.ops

class Import_Hdri_node(bpy.types.Operator):
	bl_idname = "hdri.nodegroup"
	bl_label = "hdri"
	def execute(self,context):
		
		Worldnode = bpy.data.worlds['World'].node_tree
		OPnode = bpy.data.worlds['World'].node_tree.nodes.active
		OPnodeloc = OPnode.location
		HDRnodelocoff = mathutils.Vector((-200.0, 0.0))
		Texnodelocoff = mathutils.Vector((-350.0, 0.0))
		Mapnodelocoff = mathutils.Vector((-200.0, 0.0))
		Texcoordnodelocoff = mathutils.Vector((-200.0, 0.0))

		blendfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Blender Node')
		blendfile = os.path.join(blendfile, 'HDRI_World.blend')
		section   = 'NodeTree'
		nodegroups    = 'HDRI_World'
		directory = os.path.join(blendfile, section)
		
		bpy.ops.wm.link(filename=nodegroups, directory=directory)
		bpy.ops.node.add_node(type="ShaderNodeGroup", use_transform=True, settings=[{"name":"node_tree", "value":"bpy.data.node_groups['HDRI_World']"}])
		HDRnode = bpy.data.worlds['World'].node_tree.nodes.active
		HDRBack = HDRnode.inputs[1]
		HDRBack.default_value = (0.0005,0.0005,0.0005,1)
		
		HDRnode.location = OPnodeloc + HDRnodelocoff
		HDRnodeloc = HDRnode.location
		Worldnode.links.new(HDRnode.outputs[0], OPnode.inputs[0])
		
		HDRfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'HDRI')
		HDRfileTex = os.path.join(HDRfile, 'red_blue_mix_a.exr')
		bpy.ops.image.open(filepath=HDRfileTex,
							directory=HDRfile,
							relative_path=True,
							show_multiview=False)        
		Texture = bpy.data.images['red_blue_mix_a.exr'] 
		bpy.ops.node.add_node(type="ShaderNodeTexEnvironment", use_transform=True)
		Texnode = bpy.data.worlds['World'].node_tree.nodes.active
		Texnode.location = HDRnodeloc + Texnodelocoff
		Texnodeloc = Texnode.location
		print(Texnode.location)
		print(HDRnodeloc)
		Worldnode.links.new(Texnode.outputs[0], HDRnode.inputs[0])
		Texnode.image = Texture

		bpy.ops.node.add_node(type="ShaderNodeMapping", use_transform=True)
		Mapnode = bpy.data.worlds['World'].node_tree.nodes.active
		Mapnode.location = Texnodeloc + Mapnodelocoff
		Mapnodeloc = Mapnode.location
		Worldnode.links.new(Mapnode.outputs[0], Texnode.inputs[0])

		bpy.ops.node.add_node(type="ShaderNodeTexCoord", use_transform=True)
		Texcoordnode = bpy.data.worlds['World'].node_tree.nodes.active
		Texcoordnode.location = Mapnodeloc + Texcoordnodelocoff
		Worldnode.links.new(Texcoordnode.outputs[0], Mapnode.inputs[0])

		return{'FINISHED'}

class Import_SSS_mat(bpy.types.Operator):
    
    bl_idname = "mat.sssnodegroup"
    bl_label = "mat"
    testname = 'test1'

    def execute(self,context):
        blendfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Blender Node')
        blendfile = os.path.join(blendfile, 'SSS_Mat.blend')
        section   = '\\NodeTree\\'
        nodegroups    = ['SSS_Mat']
        
        directory = blendfile + section
  
        for node in nodegroups:  
            filename  = node
            bpy.ops.wm.link(filename=filename, directory=directory)
        return{'FINISHED'}


class Choose_TexOperator(bpy.types.Operator):
    bl_idname = "object.choose_tex"
    bl_label = "Choose_Texure"
    choosekeymap = []


    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    cho = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    choi = cho.keymap_items.new('object.choose_tex', type='W', value='PRESS', ctrl=True)
    choosekeymap.append((cho,choi))


    def execute(self, context):
        print('True')
        
        return {'FINISHED'}


class Import_Texture_Maps(Operator):
	bl_idname = "import.texmap"
	bl_label = "Import"
	
	def execute(self,context):
		selpath = []                                            #初始化贴图路径
		data = bpy.data
		context = bpy.context
		scene = context.scene
		selfTools = scene.self_Tools                            #调用全局propertygroup参数
		selpath = selfTools.Tex_path                            #选中贴图路径
		list_file = os.listdir(selpath)                         #路径中所有贴图list
		list_fileUP = [i.upper() for i in list_file]
		
		DIF = 'DIF'
		ORM = 'ORM'
		NRM = 'NRM'
		
		selobj_list = bpy.context.active_object                 #获取选中的模型
		selobj_name = selobj_list.name_full                      #获取选中模型的名称
		actmat = bpy.data.objects[selobj_name].active_material   #获取选中模型的材质
		actmat_name = actmat.name_full
		actmat_nameUP = actmat_name.upper()
		nodetree = bpy.data.materials[actmat_name].node_tree
		
		TexNinMatN = [M for M in list_fileUP if actmat_nameUP in M]         #筛选含有材质关键字的文件
		TexNinMatNUP = [i.upper() for i in TexNinMatN]
		SSS_DIF = [T for T in TexNinMatNUP if DIF in T]                   #筛选含有材质和贴图关键字的文件
		SSS_ORM = [T for T in TexNinMatNUP if ORM in T]  
		SSS_NRM = [T for T in TexNinMatNUP if NRM in T]
		SSS_Tex = SSS_DIF + SSS_ORM + SSS_NRM
		SSSmatIP = ['DIF'] + ['ORM'] + ['NRM']
		
		print(actmat_name)
		print(list_file)
		print(TexNinMatNUP)
		print(",".join(TexNinMatNUP))

		if actmat_nameUP in ",".join(TexNinMatNUP):
			OPnode = bpy.data.materials[actmat_name].node_tree.nodes.active
			OPnodeloc = OPnode.location
			SSSnodelocoff = mathutils.Vector((-200.0, 0.0))
			Texnodelocoff = mathutils.Vector((-400.0, 0.0))
			
			blendfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Blender Node')
			blendfile = os.path.join(blendfile, 'SSS_Mat.blend')
			section   = '\\NodeTree\\'
			nodegroups    = 'SSS_Mat'
			
			directory = blendfile + section
			
			bpy.ops.wm.link(filename=nodegroups, directory=directory)
			bpy.ops.node.add_node(type="ShaderNodeGroup", use_transform=True, settings=[{"name":"node_tree", "value":"bpy.data.node_groups['SSS_Mat']"}])
			SSSnode = bpy.data.materials[actmat_name].node_tree.nodes.active
			SSSnode.location = OPnodeloc + SSSnodelocoff
			SSSnodeloc = SSSnode.location
			
			nodetree.links.new(SSSnode.outputs[0], OPnode.inputs[0])
		
			SSSmatInD = bpy.data.node_groups['SSS_Mat'].inputs['DIF']
			SSSmatInO = bpy.data.node_groups['SSS_Mat'].inputs['ORM']
			SSSmatInN = bpy.data.node_groups['SSS_Mat'].inputs['NRM']
			
			Texmap = {SSS_Tex[0]:SSSmatIP[0],SSS_Tex[1]:SSSmatIP[1],SSS_Tex[2]:SSSmatIP[2]}
			Downlocoff = mathutils.Vector((0.0, -300.0))
			
			for i in range(0, len(SSS_Tex)):
				print(i)
				Tex = SSS_Tex[i]
				
				bpy.ops.image.open(filepath=selpath+Tex, directory=selpath, files=[{"name":Tex, "name":Tex}], relative_path=True, show_multiview=False)        #根据路径和筛选条件导入指定路径下的贴图文件
				Texture = bpy.data.images[Tex]                                                      #遍历获取DIF图像
				Texcolorspace = Texture.colorspace_settings.name
				
				if Texmap[SSS_Tex[i]] == 'DIF':                                                 #判断图像关键字类型，ORM和NRM色彩空间设定为non-color
					Texture.colorspace_settings.name = 'sRGB'
				else:
					Texture.colorspace_settings.name = 'Non-Color'
					
				bpy.ops.node.add_node(type="ShaderNodeTexImage", use_transform=False)           #添加一个图像节点
				Texnode = data.materials[actmat_name].node_tree.nodes.active                    #选择选中物体材质中，节点树里激活的节点
				Texnode.image = Texture                                                         #image name按遍历的内容设定
				if i==0:
					Texnode.location = SSSnodeloc + Texnodelocoff                     #节点依父节点偏移
					DIFloc = Texnode.location
				elif i==1:
					ORMloc = DIFloc + Downlocoff
					Texnode.location = ORMloc                     #节点依父节点偏移
					
				elif i==2:
					NRMloc = ORMloc + Downlocoff
					Texnode.location = NRMloc                     #节点依父节点偏移
					
				nodetree.links.new(Texnode.outputs[0], SSSnode.inputs[Texmap[Tex]])
		
		else:
			print('non')
		return{'FINISHED'}

class ReloadTex(bpy.types.Operator):
    bl_idname = 'reload.tex'
    bl_label = 'Reload'

    def execute(self,context):
        texlist = list(bpy.data.images)
        for i in texlist:
            i.reload()
        print('reload')
        return{'FINISHED'}