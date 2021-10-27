import bpy
from . import Utility_Function
import mathutils

ENUM_IK_Finder_Method = [("ADVANCED","Advanced","Advanced"),("SIMPLE","Simple","Simple")]

def update_distance_no_zero(self, context):
    if self.Distance == 0:
        self.Distance = 0.1
def update_pole_size_no_zero(self, context):
    if self.Pole_Size == 0:
        self.Pole_Size = 0.1
class RetargetHelper_OT_Generate_IK_Poll_Finder(bpy.types.Operator):
    """Extract and Constraint"""
    bl_idname = "retarget_helper.generate_ik_poll_finder"
    bl_label = "Generate IK Poll Finder"
    bl_options = {'REGISTER', 'UNDO'}


    IK_Finder_Method: bpy.props.EnumProperty(name="Finder Method", items=ENUM_IK_Finder_Method)
    Distance: bpy.props.FloatProperty(name="Distance", default=0.5, update=update_distance_no_zero)
    Pole_Bone_Name: bpy.props.StringProperty()

    Pole_Copy_Rotation: bpy.props.BoolProperty(default=False)

    MCH_Bone_Layer: bpy.props.IntProperty(min=0, max=31, default=30)
    Pole_Bone_Layer: bpy.props.IntProperty(min=0, max=31, default=0)

    Pole_Size: bpy.props.FloatProperty(default=0.5, update=update_pole_size_no_zero)

    Show_Extras: bpy.props.BoolProperty()
    Advanced_MCH_Size: bpy.props.FloatProperty(min=0.1, default=0.2)
    Advanced_MCH_Angle_Pointer_Length: bpy.props.FloatProperty(min=0.1, default=0.2)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "IK_Finder_Method", expand=True)

        layout.prop(self, "Pole_Bone_Name", text="Pole Name")
        layout.prop(self, "Distance")
        layout.prop(self, "Pole_Size", text="Pole Size")

        if self.IK_Finder_Method == "ADVANCED":
            layout.prop(self, "Pole_Copy_Rotation", text="Copy Rotation")

        row = layout.row(align=True)
        row.prop(self, "MCH_Bone_Layer", text="MCH Bone Layer")
        row.prop(self, "Pole_Bone_Layer", text="Pole Bone Layer")

        layout.prop(self, "Show_Extras", text="MCH Options")
        if self.Show_Extras:
            if self.IK_Finder_Method == "ADVANCED":
                layout.prop(self, "Advanced_MCH_Size", text="MCH Size (Advanced)")
                layout.prop(self, "Advanced_MCH_Angle_Pointer_Length", text="Angle Pointer Size (Advanced)")


    def invoke(self, context, event):

        active_bone = context.active_bone
        Lower = active_bone
        self.Pole_Bone_Name = "Pole_" + Lower.name


        return context.window_manager.invoke_props_dialog(self)

    @classmethod
    def poll(cls, context):
        if context.mode in ["POSE", "EDIT_ARMATURE"]:
            return True

    def execute(self, context):

        object = context.object
        mode = context.mode

        bpy.ops.object.mode_set(mode = 'EDIT')
        bones = object.data.edit_bones

        active_bone = context.active_bone

        Upper = active_bone.parent
        Lower = active_bone

        object.data.layers[self.Pole_Bone_Layer] = True
        object.data.layers[self.MCH_Bone_Layer] = True


        if Upper and Lower:
            if self.IK_Finder_Method == "ADVANCED":
                #Turn off Deform for MCH Bone
                Upper_Angle_Finder_Name = "MCH" + Upper.name + "Angle_Finder"
                Lower_Angle_Finder_Name = "MCH" + Lower.name + "Angle_Finder"

                Upper_Angle_Finder = bones.new(Upper_Angle_Finder_Name)
                Lower_Angle_Finder = bones.new(Lower_Angle_Finder_Name)

                Upper_Angle_Finder.head = Upper.tail
                Upper_Angle_Finder.tail = Upper.head

                Lower_Angle_Finder.head = Lower.head
                Lower_Angle_Finder.tail = Lower.tail

                Upper_Angle_Finder.length = self.Advanced_MCH_Size
                Lower_Angle_Finder.length = self.Advanced_MCH_Size

                Upper_Angle_Finder.roll = Upper.roll
                Lower_Angle_Finder.roll = Lower.roll

                Upper_Angle_Finder.parent = Lower
                Lower_Angle_Finder.parent = Lower

                Angle_Pointer_Name = "MCH" + Lower.name + "Angle_Pointer"
                Angle_Pointer = bones.new(Angle_Pointer_Name)

                Angle_Pointer.head = Utility_Function.midpoint([Upper_Angle_Finder.tail, Lower_Angle_Finder.tail], "CENTER")
                Angle_Pointer.tail = Lower.head

                if Angle_Pointer.head == Angle_Pointer.tail:
                    Angle_Pointer.tail.y += self.Advanced_MCH_Angle_Pointer_Length

                Angle_Pointer.parent = Lower

                Pole_Finder_Name = "MCH" + Lower.name + "Pole_Finder"
                Pole_Finder = bones.new(Pole_Finder_Name)
                Pole_Finder.head = Lower.head
                Pole_Finder.align_orientation(Angle_Pointer)
                Pole_Finder.length = self.Distance

                Pole_Finder.parent = Lower


                Pole_Bone = bones.new(self.Pole_Bone_Name)
                Pole_Bone.head = Pole_Finder.tail
                Pole_Bone.tail = Pole_Bone.head
                Pole_Bone.tail.z += self.Pole_Size

                if self.Pole_Copy_Rotation:
                    Pole_Bone.align_orientation(Angle_Pointer)

                Upper = Upper.name
                Lower = Lower.name
                Upper_Angle_Finder = Upper_Angle_Finder.name
                Lower_Angle_Finder = Lower_Angle_Finder.name
                Angle_Pointer = Angle_Pointer.name
                Pole_Finder = Pole_Finder.name
                Pole_Bone = Pole_Bone.name


                bpy.ops.object.mode_set(mode = 'POSE')

                bones = object.pose.bones

                Upper = bones.get(Upper)
                Lower = bones.get(Lower)
                Upper_Angle_Finder = bones.get(Upper_Angle_Finder)
                Lower_Angle_Finder = bones.get(Lower_Angle_Finder)
                Angle_Pointer = bones.get(Angle_Pointer)
                Pole_Finder = bones.get(Pole_Finder)
                Pole_Bone = bones.get(Pole_Bone)

                Constraint = Upper_Angle_Finder.constraints.new("DAMPED_TRACK")
                Constraint.target = object
                Constraint.subtarget = Upper.name

                Constraint = Lower_Angle_Finder.constraints.new("DAMPED_TRACK")
                Constraint.target = object
                Constraint.subtarget = Lower.name
                Constraint.head_tail = 1

                Constraint = Angle_Pointer.constraints.new("COPY_LOCATION")
                Constraint.target = object
                Constraint.subtarget = Upper_Angle_Finder.name
                Constraint.head_tail = 1

                Constraint = Angle_Pointer.constraints.new("COPY_LOCATION")
                Constraint.target = object
                Constraint.subtarget = Lower_Angle_Finder.name
                Constraint.head_tail = 1
                Constraint.influence = 0.5

                Constraint = Angle_Pointer.constraints.new("DAMPED_TRACK")
                Constraint.target = object
                Constraint.subtarget = Lower.name

                Constraint = Pole_Finder.constraints.new("COPY_ROTATION")
                Constraint.target = object
                Constraint.subtarget = Angle_Pointer.name

                Constraint = Pole_Bone.constraints.new("COPY_LOCATION")
                Constraint.target = object
                Constraint.subtarget = Pole_Finder.name
                Constraint.head_tail = 1

                if self.Pole_Copy_Rotation:
                    Constraint = Pole_Bone.constraints.new("COPY_ROTATION")
                    Constraint.target = object
                    Constraint.subtarget = Pole_Finder.name

                layers = [False for x in range(32)]
                layers[self.Pole_Bone_Layer] = True
                Pole_Bone.bone.layers = layers





                MCH_Bones = [Pole_Finder, Angle_Pointer, Lower_Angle_Finder, Upper_Angle_Finder]

                for bone in MCH_Bones:

                    layers = [False for x in range(32)]
                    layers[self.MCH_Bone_Layer] = True
                    bone.bone.layers = layers

            if self.IK_Finder_Method == "SIMPLE":

                Upper_Angle_Finder_Name = "MCH" + Upper.name + "Angle_Finder"
                Lower_Angle_Finder_Name = "MCH" + Lower.name + "Angle_Finder"

                Upper_Angle_Finder = bones.new(Upper_Angle_Finder_Name)
                Lower_Angle_Finder = bones.new(Lower_Angle_Finder_Name)

                Upper_Angle_Finder.head = Upper.tail
                Upper_Angle_Finder.tail = Upper.head
                Upper_Angle_Finder.roll = Upper.roll

                Lower_Angle_Finder.head = Lower.head
                Lower_Angle_Finder.tail = Lower.tail
                Lower_Angle_Finder.roll = Lower.roll

                Lower_Angle_Finder.length = -(self.Distance)
                Upper_Angle_Finder.length = -(self.Distance)

                Lower_Angle_Finder.parent = Lower
                Upper_Angle_Finder.parent = Upper

                Pole_Bone_Name = self.Pole_Bone_Name
                Pole_Bone = bones.new(Pole_Bone_Name)

                Pole_Bone.head = Utility_Function.midpoint([Upper_Angle_Finder.tail, Lower_Angle_Finder.tail], "CENTER")
                Pole_Bone.tail = Pole_Bone.head
                Pole_Bone.tail.z += self.Pole_Size

                Upper = Upper.name
                Lower = Lower.name
                Upper_Angle_Finder = Upper_Angle_Finder.name
                Lower_Angle_Finder = Lower_Angle_Finder.name
                Pole_Bone = Pole_Bone.name

                bpy.ops.object.mode_set(mode = 'POSE')

                bones = object.pose.bones

                Upper = bones.get(Upper)
                Lower = bones.get(Lower)
                Upper_Angle_Finder = bones.get(Upper_Angle_Finder)
                Lower_Angle_Finder = bones.get(Lower_Angle_Finder)
                Pole_Bone = bones.get(Pole_Bone)

                Constraint = Pole_Bone.constraints.new("COPY_LOCATION")
                Constraint.target = object
                Constraint.subtarget = Lower_Angle_Finder.name
                Constraint.head_tail = 1


                Constraint = Pole_Bone.constraints.new("COPY_LOCATION")
                Constraint.target = object
                Constraint.subtarget = Upper_Angle_Finder.name
                Constraint.head_tail = 1
                Constraint.influence = 0.5

                layers = [False for x in range(32)]
                layers[self.Pole_Bone_Layer] = True
                Pole_Bone.bone.layers = layers

                MCH_Bones = [Upper_Angle_Finder, Lower_Angle_Finder]

                for bone in MCH_Bones:

                    layers = [False for x in range(32)]
                    layers[self.MCH_Bone_Layer] = True
                    bone.bone.layers = layers

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
