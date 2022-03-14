import bpy
import re
import math
from bpy.utils import register_class, unregister_class


class BakeVertexAOPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_Bake_Vertex_AO"
    bl_label = "烘焙顶点色AO"
    bl_category = "Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_order = 12
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.operator('object.bakevertexao')
        layout.operator('object.aochangechannel')

class BakeVertexAOOperator(bpy.types.Operator):
    bl_idname = "object.bakevertexao"
    bl_label = "烘焙AO"

    def execute(self, context):
        actobj = bpy.context.active_object
        selobj = bpy.context.selected_objects
        for i in selobj:
            actmeshname = i.data.name_full
            actmesh = bpy.data.meshes[actmeshname]
            objvercol = bpy.data.meshes[actmeshname].vertex_colors
# =====================================================================================================================================
# 添加加权法向修改器修正法线，检查顶点色通道是否存在，并清理顶点色通道只保留一个
            ModifierList = bpy.data.objects[i.name_full].modifiers
            T = 0
            VextexColor = "VextexColor"
            bpy.ops.object.shade_smooth()
            actmesh.use_auto_smooth = True
            actmesh.auto_smooth_angle = 90*math.pi/180
            for M in ModifierList:
                if M.name == 'WeightedNormal':
                    T = T+1
            if T==1:
                print("Have WeightedNormal Modifier")
            else:
                bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
                bpy.data.objects[i.name_full].modifiers["WeightedNormal"].keep_sharp = True
            if len(objvercol) == 0:
                bpy.data.meshes[actmeshname].vertex_colors.new(name=VextexColor,do_init=True)
            else:
                if len(objvercol) > 1:
                    for c in objvercol:
                        bpy.ops.mesh.vertex_color_remove()
                        if len(objvercol) > 1:
                            for v in objvercol:
                                bpy.ops.mesh.vertex_color_remove()
                else:
                    bpy.data.meshes[actmeshname].vertex_colors[0].name = VextexColor
                if len(objvercol) == 0:
                    bpy.data.meshes[actmeshname].vertex_colors.new(name=VextexColor,do_init=True)
# =====================================================================================================================================
# 切换渲染器为CYCLES做顶点色烘焙
        bpy.data.scenes["Scene"].render.engine = "CYCLES"
        bpy.data.scenes["Scene"].render.bake.target = "VERTEX_COLORS"
        bpy.ops.object.bake(type='AO')

        return{'FINISHED'}
# # ==============================================================================================================
# # 依据材质组名设置同名顶点组
# # 不需要使用顶点组，直接使用材质顶点
#         matslot = bpy.data.objects[actobj.name_full].material_slots
#         verslot = bpy.data.objects[actobj.name_full].vertex_groups
#         bpy.data.objects[actobj.name_full].active_material_index = 0
#         if len(verslot) > 0:
#             bpy.ops.object.vertex_group_remove(all=True)

#         for i in matslot:
#             bpy.ops.object.mode_set(mode='EDIT')
#             bpy.ops.mesh.select_all(action='DESELECT')
#             bpy.ops.object.material_slot_select()
#             bpy.data.objects[actobj.name_full].vertex_groups.new(name=i.name)
#             bpy.ops.object.vertex_group_assign()
#             bpy.ops.mesh.select_all(action='DESELECT')
#             bpy.ops.object.mode_set(mode='OBJECT')
#             bpy.data.objects[actobj.name_full].active_material_index =+ 1

# =====================================================================================================================================
# 处理叶子的顶点色信息【R存储AO信息，G留空为1，B存储树干树叶拆分信息，树干为0，树叶为1，A留空为1】
# 区别树叶和树干的顶点编号
# 目前可预知但应该不会碰到的问题：材质信息按面分配，顶点色按点分配，拾取材质分组的顶点会造成多个材质有多个顶点复选，如果模型相连，则会出现问题,可以用顶点组解决(?)
class AOChangeChannelOperator(bpy.types.Operator):
    bl_idname = "object.aochangechannel"
    bl_label = "修改匹配规范"

    def execute(self, context):
        selobj = bpy.context.selected_objects
        actobj = bpy.context.active_object
        matslot = 0
        leafvtx = []
        treevtx = []
        actmeshname = actobj.data.name_full
        actmesh = bpy.data.meshes[actmeshname]
        vtxcol = actmesh.vertex_colors["VextexColor"]
        actobj.active_material_index = 0

        for m in actobj.material_slots:
            if re.search('leaf',m.name.lower()):
                actobj.active_material_index = matslot
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_all(action='DESELECT') #初始化选择内容
                bpy.ops.object.material_slot_select() #选择激活材质通道的几何内容
                bpy.ops.object.editmode_toggle()
                for v in actmesh.vertices:
                    if v.select == False:
                        treevtx.append(v)
                    else:
                        leafvtx.append(v)
            matslot += 1
            

        for i in actmesh.loops:
            for l in leafvtx:
                if i.vertex_index == l.index:
                    # print(i.vertex_index,i.index)
                    bpy.data.meshes[actmeshname].vertex_colors[vtxcol.name].data[i.index].color[1:] = [1,1,1]
                    # vtxcol.data[i.index].color = [vtxcol.data[i.index].color[0],1,1,1]
                    # vtxcol.data[i.index].color[1:] = [1,1,1]
                    # vtxcol.data[i.vertex_index].color[1] = 1
                    # vtxcol.data[i.vertex_index].color[2] = 1
                    # vtxcol.data[i.vertex_index].color[3] = 1
            for t in treevtx:
                if i.vertex_index == t.index:
                    # print(i.vertex_index,i.index)
                    bpy.data.meshes[actmeshname].vertex_colors[vtxcol.name].data[i.index].color[1:] = [1,0,1]
                    # vtxcol.data[i.index].color = [vtxcol.data[i.index].color[0],1,0,1]
            #         vtxcol.data[i.index].color[1:] = [1,0,1]
            #         vtxcol.data[i.index].color[1] = 1
            #         vtxcol.data[i.index].color[2] = 0
            #         vtxcol.data[i.index].color[3] = 1
        return{'FINISHED'}

classes = (BakeVertexAOPanel,
            BakeVertexAOOperator,
            AOChangeChannelOperator)

def register():
    global classes
    for cls in classes:
        register_class(cls)

def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)