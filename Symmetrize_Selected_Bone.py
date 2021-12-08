import bpy
import re
from . import Utility_Function
import math




class Side_Flipper:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def flip_name(self, name):

        flipped_name = None

        if self.left in name:
            flipped_name = name.replace(self.left, self.right)
        elif self.right in name:
            flipped_name = name.replace(self.right, self.left)

        return flipped_name

    def get_flipped_bone(self, bones, bone):

        flipped_bone = None
        if bones:
            if bone:
                flipped_bone_name = self.flip_name(bone.name)
                if flipped_bone_name:
                    flipped_bone = bones.get(flipped_bone_name)

        return flipped_bone

    def symmetrize_edit_bone(self, bones, bone, relation=True, create_missing=True, axis="X", flip_roll=False):

        if bones:
            if bone:
                flipped_bone_name = self.flip_name(bone.name)
                if flipped_bone_name:
                    flipped_bone = bones.get(flipped_bone_name)

                    if create_missing:
                        if not flipped_bone:
                            flipped_bone = bones.new(flipped_bone_name)

                    if flipped_bone:
                        flipped_bone.head = bone.head
                        flipped_bone.tail = bone.tail
                        flipped_bone.roll = bone.roll

                        if axis == "X":
                            flipped_bone.head.x = -bone.head.x
                            flipped_bone.tail.x = -bone.tail.x
                        if axis == "Y":
                            flipped_bone.head.y = -bone.head.y
                            flipped_bone.tail.y = -bone.tail.y
                        if axis == "Z":
                            flipped_bone.head.z = -bone.head.z
                            flipped_bone.tail.z = -bone.tail.z


                        flipped_bone.roll = bone.roll
                        if flip_roll:
                            # flipped_bone.roll = -bone.roll
                            flipped_bone.roll = bone.roll + math.radians(180)

                        if relation:

                            parent = bone.parent
                            flipped_parent_name = self.flip_name(parent.name)

                            if flipped_parent_name:
                                flipped_parent = bones.get(flipped_parent_name)

                                if flipped_parent:
                                    flipped_bone.parent = flipped_parent

                                    flipped_bone.use_connect = bone.use_connect

                                    flipped_parent.use_connect = bone.parent.use_connect


                            for child in bone.children:
                                flipped_child_name = self.flip_name(child.name)

                                if flipped_child_name:
                                    flipped_child = bones.get(flipped_child_name)
                                    if flipped_child:
                                        flipped_child.parent = flipped_bone

    # def symmetrize_pose_bone(self, bones, bone, relation=True, create_missing=True, axis="X", flip_roll=False):
    #
    #     if bones:
    #         if bone:
    #             flipped_bone_name = self.flip_name(bone.name)
    #             if flipped_bone_name:
    #                 flipped_bone = bones.get(flipped_bone_name)
    #
    #                 if flipped_bone:
    #                     flipped_bone.head = bone.head
    #                     flipped_bone.tail = bone.tail
    #                     flipped_bone.roll = bone.roll
    #
    #                     flipped_bone.rotation_quaternion = bone.rotation_quaternion
    #                     flipped_bone.scale = bone.scale
    #                     flipped_bone.location = bone.location
    #
    #                     if axis == "X":
    #                         flipped_bone.location.x = -bone.location.x
    #                         flipped_bone.rotation_quaternion.y = -bone.rotation_quaternion.y
    #                         flipped_bone.rotation_quaternion.z = -bone.rotation_quaternion.z






ENUM_Axis = [("X","X","X"),("Y","Y","Y"),("Z","Z","Z")]

class RetargetHelper_OT_Symmetrize_Selected_Bones(bpy.types.Operator):
    """Symmetrize Selected Bone"""
    bl_idname = "retarget_helper.symmetrize_selected_bones"
    bl_label = "Symmetrize Selected Bones"
    bl_options = {'REGISTER', 'UNDO'}

    left: bpy.props.StringProperty(default=".L")
    right: bpy.props.StringProperty(default=".R")
    axis: bpy.props.EnumProperty(items=ENUM_Axis)
    flip_roll: bpy.props.BoolProperty(default=False)

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    @classmethod
    def poll(cls, context):
        if context.mode in ["EDIT_ARMATURE"]:
            return True

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "axis", text="Flip Axis")
        layout.prop(self, "left", text="Left Identifier")
        layout.prop(self, "right", text="Right Identifier")
        layout.prop(self, "flip_roll", text="Flip Roll")

    def execute(self, context):

        object = context.edit_object
        mode = context.mode

        bones = context.object.data.edit_bones

        Flipper = Side_Flipper(self.left, self.right)

        if object:
            for bone in context.selected_bones:

                flipped_bone = Flipper.symmetrize_edit_bone(bones, bone, axis=self.axis, flip_roll=self.flip_roll)


        return {'FINISHED'}



classes = [RetargetHelper_OT_Symmetrize_Selected_Bones]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
