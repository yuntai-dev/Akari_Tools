import bpy
from bpy.utils import register_class, unregister_class
from mathutils import Matrix


class PhysicsPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_PhysicsPanel"
    bl_label = "快速刚体碰撞"
    bl_category = "Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_order = 11
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        row = layout.row()
        layout.prop(wm.asset_sketcher,'physics_friction', text="Friction",slider=True)
        layout.prop(wm.asset_sketcher,'physics_time_scale', text="Time Scale")
        # layout.operator('asset_sketcher.calc_physics')
        if not wm.asset_sketcher.running_physics_calculation:
            op = row.operator('asset_sketcher.calc_physics',text = "开始模拟")
        else:
            row.prop(wm.asset_sketcher,'running_physics_calculation', text="Cancel Calculation",icon="X")



class AkariPhysics_OT_CalcPhysics(bpy.types.Operator):
    bl_idname = "asset_sketcher.calc_physics"
    bl_label = "Calculate Physics"
    bl_description = ""
    bl_options = {"REGISTER"}

    def __init__(self):
        fps = 0
        frame_start = 0
        frame_end = 0
        frame_current = 0
        world_enabled = True
        use_split_impulse = True
        world_time_scale = 1.0

    @classmethod
    def poll(cls, context):
        return True

    def add_passive_bodies(self, context, add):
        asset_sketcher = context.window_manager.asset_sketcher
        active_object = context.active_object

        for obj in context.visible_objects:
            if not obj.select_get() and obj.type == "MESH":
                context.view_layer.objects.active = obj
                if add and obj.rigid_body == None:
                    bpy.ops.rigidbody.object_add()
                    obj.rigid_body.friction = asset_sketcher.physics_friction
                    obj.rigid_body.type = "PASSIVE"
                    obj.rigid_body.collision_shape = "MESH"
                elif not add and obj.rigid_body != None:
                    bpy.ops.rigidbody.object_remove()

        context.view_layer.objects.active = canvas = active_object

    def invoke(self, context, event):

        mesh_objects = 0
        for obj in context.selected_objects:
            if obj.type == "MESH":
                mesh_objects += 1
                break
        if mesh_objects == 0:
            self.report({'WARNING'}, 'No Mesh Objects for Physics Calculation selected.')
            return {"CANCELLED"}

        wm = context.window_manager
        asset_sketcher = context.window_manager.asset_sketcher
        wm.modal_handler_add(self)
        asset_sketcher.running_physics_calculation = True

        if context.scene.rigidbody_world == None:
            bpy.ops.rigidbody.world_add()

        self.fps = context.scene.render.fps
        self.frame_start = context.scene.frame_start
        self.frame_end = context.scene.frame_end
        self.frame_current = context.scene.frame_current
        self.world_enabled = context.scene.rigidbody_world.enabled
        self.use_split_impulse = context.scene.rigidbody_world.use_split_impulse
        self.world_time_scale = context.scene.rigidbody_world.time_scale

        context.scene.rigidbody_world.time_scale = asset_sketcher.physics_time_scale
        context.scene.render.fps = 24
        context.scene.frame_start = 0
        context.scene.frame_end = 10000
        context.scene.frame_current = 0
        context.scene.rigidbody_world.enabled = True
        context.scene.rigidbody_world.use_split_impulse = True

        self.add_passive_bodies(context, True)

        bpy.ops.object.as_add_active_physics()

        bpy.ops.screen.animation_play()

        tot = context.scene.frame_end
        wm.progress_begin(0, tot)
        return {"RUNNING_MODAL"}

    def exit_modal(self, context, wm):
        asset_sketcher = context.window_manager.asset_sketcher
        asset_sketcher.running_physics_calculation = False
        bpy.ops.screen.animation_play()
        bpy.ops.object.as_apply_physics()
        # bpy.ops.screen.animation_cancel()

        context.scene.render.fps = self.fps
        context.scene.frame_start = self.frame_start
        context.scene.frame_end = self.frame_end
        context.scene.frame_current = self.frame_current
        context.scene.rigidbody_world.enabled = self.world_enabled
        context.scene.rigidbody_world.use_split_impulse = self.use_split_impulse
        context.scene.rigidbody_world.time_scale = self.world_time_scale

        self.add_passive_bodies(context, False)
        wm.progress_end()
        bpy.ops.ed.undo_push(message="Calc Physics")

    def modal(self, context, event):
        wm = context.window_manager
        asset_sketcher = context.window_manager.asset_sketcher
        if event.type in {"ESC"} or context.scene.frame_current >= 10000 or not asset_sketcher.running_physics_calculation:
            self.exit_modal(context, wm)
            return {"CANCELLED"}
        wm.progress_update(context.scene.frame_current)
        return {"PASS_THROUGH"}


class AkariPhysics_OT_AddActivePhysics(bpy.types.Operator):
    bl_idname = "object.as_add_active_physics"
    bl_label = "Add physics to Assets"
    bl_description = "Sets up Assets as rigidbody objects."

    def execute(self, context):
        asset_sketcher = context.window_manager.asset_sketcher
        active_object = context.active_object
        for obj in context.selected_objects:
            if obj.type == "MESH":
                context.view_layer.objects.active = obj
                bpy.ops.rigidbody.object_add()
                obj.rigid_body.friction = asset_sketcher.physics_friction
        context.view_layer.objects.active = active_object

        return {'FINISHED'}


class AkariPhysics_OT_ApplyPhysics(bpy.types.Operator):
    bl_idname = "object.as_apply_physics"
    bl_label = "Apply physics to Assets"
    bl_description = "Applies physics to assets and removes rigidbodies."

    def execute(self, context):
        active_object = context.active_object

        obj_transformation = []
        context.view_layer.update()

        for obj in context.selected_objects:
            obj_transformation.append({"obj": obj, "matrix_world": Matrix(obj.matrix_world)})

        for data in obj_transformation:
            obj = bpy.data.objects[data["obj"].name]

            context.view_layer.objects.active = obj
            bpy.ops.object.visual_transform_apply()
            bpy.ops.rigidbody.object_remove()

            obj.matrix_world = data["matrix_world"]

        context.view_layer.objects.active = active_object

        return {'FINISHED'}

classes = (PhysicsPanel,
            AkariPhysics_OT_CalcPhysics,
            AkariPhysics_OT_AddActivePhysics,
            AkariPhysics_OT_ApplyPhysics
            )

def register():
    global classes
    for cls in classes:
        register_class(cls)

def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)