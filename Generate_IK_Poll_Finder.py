import bpy
from . import Utility_Function

class RetargetHelper_OT_Generate_IK_Poll_Finder(bpy.types.Operator):
    """Extract and Constraint"""
    bl_idname = "retarget_helper.generate_ik_poll_finder"
    bl_label = "Generate IK Poll Finder"
    bl_options = {'REGISTER', 'UNDO'}

    Distance: bpy.props.FloatProperty(default=10)

    Tail_Offset: bpy.props.FloatProperty(name="Tail", default=0.2)

    Poll_Name: bpy.props.StringProperty()
    Poll_Helper_Name: bpy.props.StringProperty()

    def invoke(self, context, event):

        active_bone = context.active_bone

        self.Poll_Name = "POLL_" + active_bone.name
        self.Poll_Helper_Name = "POLL_Helper" + active_bone.name

        return context.window_manager.invoke_props_dialog(self)


    @classmethod
    def poll(cls, context):
        if context.mode in ["POSE", "EDIT_ARMATURE"]:
            return True

    def execute(self, context):

        object = context.object
        mode = context.mode
        bones = object.data.edit_bones

        bpy.ops.object.mode_set(mode = 'EDIT')

        active_bone = context.active_bone

        Upper = active_bone.parent
        Lower = active_bone


        if Upper and Lower:

            Poll_Position = Utility_Function.Calculate_Poll_Position(Upper, Lower, self.Distance)

            poll_bone = bones.new(self.Poll_Name)
            poll_bone.head = Poll_Position
            poll_bone.tail = Poll_Position
            poll_bone.tail.z += self.Tail_Offset


            helper_bone = bones.new(self.Poll_Helper_Name)
            helper_bone.head = Lower.head
            helper_bone.tail = poll_bone.head

            poll_bone.parent = helper_bone

            helper_bone.parent = Upper

            helper_bone.roll = Upper.roll

            poll_bone_name = poll_bone.name
            helper_bone_name = helper_bone.name
            Lower_bone_name = Lower.name

            bpy.ops.object.mode_set(mode = 'POSE')

            helper_bone = object.pose.bones.get(helper_bone_name)

            constraint = helper_bone.constraints.new("COPY_ROTATION")
            constraint.target = object
            constraint.subtarget = Lower_bone_name
            constraint.target_space = "LOCAL"
            constraint.owner_space = "LOCAL"
            constraint.influence = 0.5
            constraint.use_y = False

        if mode == "POSE":
            bpy.ops.object.mode_set(mode = 'POSE')
        if mode == "EDIT_ARMATURE":
            bpy.ops.object.mode_set(mode = 'EDIT')

        return {'FINISHED'}



classes = [RetargetHelper_OT_Generate_IK_Poll_Finder]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
