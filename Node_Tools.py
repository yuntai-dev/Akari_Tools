'''
Author: your name
Date: 2020-10-04 22:32:46
LastEditTime: 2021-06-02 17:34:56
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Akari_Tools\Import_Hdri.py
'''
import numpy as np
import bpy
import os
import re
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


		selobj_list = bpy.context.active_object                 #获取选中的模型
		selobj_name = selobj_list.name_full                      #获取选中模型的名称
		actmat = bpy.data.objects[selobj_name].active_material   #获取选中模型的材质
		actmat_name = actmat.name_full
		actmat_nameUP = actmat_name.upper()
		nodetree = bpy.data.materials[actmat_name].node_tree

		OPnode = bpy.data.materials[actmat_name].node_tree.nodes.active
		OPnodeloc = OPnode.location
		SSSnodelocoff = mathutils.Vector((-200.0, 0.0))
		
		blendfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Blender Node')
		blendfile = os.path.join(blendfile, 'SSS_Mat.blend')
		section   = '\\NodeTree\\'
		nodegroups    = 'SSS_Mat'
		directory = blendfile + section
		
		bpy.ops.wm.link(filename=nodegroups, directory=directory)
		bpy.ops.node.add_node(type="ShaderNodeGroup", use_transform=True, settings=[{"name":"node_tree", "value":"bpy.data.node_groups['SSS_Mat']"}])
		SSSnode = bpy.data.materials[actmat_name].node_tree.nodes.active
		SSSnode.location = OPnodeloc + SSSnodelocoff

		SSSNorP = SSSnode.inputs[7]
		SSSNorP.default_value = (0)
		SSSNorI = SSSnode.inputs[8]
		SSSNorI.default_value = (0)

		nodetree.links.new(SSSnode.outputs[0], OPnode.inputs[0])
		
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
		
		DIF = 'Dif'
		ORM = 'ORM'
		NRM = 'Nrm'
		
		selobj_list = bpy.context.active_object                 #获取选中的模型
		selobj_name = selobj_list.name_full                      #获取选中模型的名称
		actmat = bpy.data.objects[selobj_name].active_material   #获取选中模型的材质
		actmat_name = actmat.name_full
		actmat_nameUP = actmat_name.upper()
		nodetree = bpy.data.materials[actmat_name].node_tree
		
		TexNinMatN = [M for M in list_file if actmat_name in M]         #筛选含有材质关键字的文件
		TexNinMatNUP = [i.upper() for i in TexNinMatN]
		SSS_DIF = [T for T in TexNinMatN if DIF in T]                   #筛选含有材质和贴图关键字的文件
		SSS_ORM = [T for T in TexNinMatN if ORM in T]  
		SSS_NRM = [T for T in TexNinMatN if NRM in T]
		SSS_Tex = SSS_DIF + SSS_ORM + SSS_NRM
		SSSmatIP = [DIF] + [ORM] + [NRM]

		if actmat_name in ",".join(TexNinMatN):
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
			
			SSSNorP = SSSnode.inputs[7]
			SSSNorP.default_value = (1)
			SSSNorI = SSSnode.inputs[8]
			SSSNorI.default_value = (1)
			
			nodetree.links.new(SSSnode.outputs[0], OPnode.inputs[0])

			Texmap = {SSS_Tex[0]:SSSmatIP[0],SSS_Tex[1]:SSSmatIP[1],SSS_Tex[2]:SSSmatIP[2]}
			SSSmatin = 0,3,6
			Downlocoff = mathutils.Vector((0.0, -300.0))
			
			for i in range(0, len(SSS_Tex)):
				Tex = SSS_Tex[i]
				SpStr = str(Tex.split('_'))
				
				bpy.ops.image.open(filepath=selpath+Tex, directory=selpath, files=[{"name":Tex, "name":Tex}], relative_path=True, show_multiview=False)        #根据路径和筛选条件导入指定路径下的贴图文件
				Texture = bpy.data.images[Tex]                                                      #遍历获取DIF图像
				print(i)
				
				if Texmap[SSS_Tex[i]] == DIF:                                                 #判断图像关键字类型，ORM和NRM色彩空间设定为non-color
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
					
				nodetree.links.new(Texnode.outputs[0], SSSnode.inputs[SSSmatin[i]])
		
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

class RelocateImageOperator(bpy.types.Operator):
	bl_idname = "object.relocate_image"
	bl_label = "Relocate Image"
	
	def execute(self, context):
		selpath = []                                            #初始化贴图路径
		context = bpy.context
		scene = context.scene
		selfTools = scene.self_Tools                            #调用全局propertygroup参数
		selpath = selfTools.Tex_path                            #选中贴图路径

		if selpath.endswith('\\'):                              #在blender搜索栏选择的路径后缀会自带一个'\'，这里检测后缀是否带'\'，检测到就自动删除，windows复制路径不存在这个问题。
			selpath = selpath.rstrip('\\')

		selobj = bpy.context.selected_objects
		actobj = bpy.context.active_object
		actmat = actobj.active_material
		selnode = bpy.context.selected_nodes
		osdirfile = os.listdir(selpath)

		for node in selnode:
			actnodetex = bpy.data.materials[actmat.name].node_tree.nodes[node.name].image
			for file in osdirfile:                                  						#用外部文件名称重命名节点名称和节点引用的贴图名称，以替代
				if re.search(actnodetex.name.lower(), file.lower(), re.IGNORECASE):
					img = actmat.node_tree.nodes[node.name].image
					bpy.data.images[img.name].name = file
					node.name = file
					print(actnodetex.name)
				else:
					print('no')

		bpy.ops.image.reload()
		
		return {'FINISHED'}
