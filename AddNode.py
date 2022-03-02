from posixpath import split
import bpy
from bpy import context
import mathutils 
import os
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

class AddNodePanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_AddNode"
    bl_label = "Node Tools"
    bl_category = "Tool"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"

    def draw(self, context):
        addonprops = context.scene.addonprops
        layout = self.layout
        row = layout.row()
        # row.operator('object.importbasemat')
        # row.operator('object.importhdrimat')
        layout.prop(addonprops,'addimage_path')
        layout.operator('object.importimage')
        layout.operator('object.acestextool')
        return 


class ImportBaseMatOperator(bpy.types.Operator):
    bl_idname = "object.importbasemat"
    bl_label = "Import Base Materil"

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
        
        return {'FINISHED'}

class ImportHDRImatOperator(bpy.types.Operator):
    bl_idname = "object.importhdrimat"
    bl_label = "Import HDRI"

    def execute(self, context):

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
        

class ImportImageOperator(bpy.types.Operator):
    bl_idname = "object.importimage"
    bl_label = "Import Image"

    def execute(self, context):
        selpath = []                                            #初始化贴图路径
        data = bpy.data
        context = bpy.context
        scene = context.scene
        selpath = scene.addonprops.addimage_path                            #选中贴图路径
        list_file = os.listdir(selpath)                         #路径中所有贴图list

        DIF = 'DIF'
        ORM = 'ORM'
        NRM = 'NRM'

        selobj_list = bpy.context.active_object                 #获取选中的模型
        selobj_name = selobj_list.name_full                      #获取选中模型的名称
        actmat = bpy.data.objects[selobj_name].active_material   #获取选中模型的材质
        actmat_name = actmat.name_full
        nodetree = bpy.data.materials[actmat_name].node_tree

        TexNinMatN = [M for M in list_file if actmat_name in M]         #筛选含有材质关键字的文件
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

        return {'FINISHED'}


class ACESTexToolOperator(bpy.types.Operator):
    bl_idname = "object.acestextool"
    bl_label = "ACES SRGB色彩空间切换"

    def execute(self, context):
        ColType = ['albedo','c','color','diffuse','base color','col']
        HDRType = ['hdr','exr']
        device = bpy.data.scenes['Scene'].display_settings.display_device
        images = bpy.data.images
        for i in images:
            sptype = i.name.split('.')
            if sptype[-1] in HDRType:   #后缀为hdr和exr的hdri图像文件，色彩空间设置为ACES线性
                if device == 'sRGB':
                    i.colorspace_settings.name = 'Linear'
                elif device == 'ACES':
                    i.colorspace_settings.name = 'Utility - Linear - sRGB'

            else:
                spname = sptype[0].split('_')
                for col in spname:
                    col = col.lower()
                    if col in ColType:
                        if device == 'sRGB':
                            i.colorspace_settings.name = 'sRGB'
                        elif device == 'ACES':
                            i.colorspace_settings.name = 'Utility - sRGB - Texture'

        return {'FINISHED'}
