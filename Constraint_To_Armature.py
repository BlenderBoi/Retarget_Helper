import bpy

constraint_type = [("TRANSFORM","Copy Transform","Copy Transform"),("LOTROT","Copy Location & Copy Rotation","Lot Rot"), ("CHILD_OF","Child Of","Child Of")]

class RetargetHelper_Constraint_To_Armature(bpy.types.Operator):
    """Constraint to Armature"""
    bl_idname = "retargethelper.constraint_to_armature_name"
    bl_label = "Constraint to Armature (Name Based)"
    bl_options = {'REGISTER', 'UNDO'}

    Source_Armature: bpy.props.StringProperty()
    Target_Armature: bpy.props.StringProperty()

    Constraint_Type: bpy.props.EnumProperty(items=constraint_type)
    Clear_Constraint: bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        return context.mode in ["OBJECT", "POSE"]


    def invoke(self, context, event):

        if context.mode == "OBJECT":
            if context.object:
                if context.object.type == "ARMATURE":
                    self.Source_Armature = context.object.name

                for object in context.selected_objects:
                    if object.type == "ARMATURE":
                        if not object == context.object:
                            self.Target_Armature = object.name
                            break

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):

        layout = self.layout

        if context.mode == "OBJECT":
            layout.prop_search(self, "Source_Armature", bpy.data, "objects", text="From")

        layout.prop_search(self, "Target_Armature", bpy.data, "objects", text="To")

        layout.prop(self, "Constraint_Type", text="Constraint Type")
        layout.prop(self, "Clear_Constraint", text="Clear Constraint")

    def execute(self, context):

        Target_Armature = bpy.data.objects.get(self.Target_Armature)
        Source_Armature = bpy.data.objects.get(self.Source_Armature)


        Editing_Armature = []

        if context.mode == "OBJECT":
            if Target_Armature and Source_Armature:
                if Target_Armature.type == "ARMATURE" and Source_Armature.type == "ARMATURE":

                    for bone in Source_Armature.pose.bones:

                        if context.mode == "OBJECT":

                            if Target_Armature.pose.bones.get(bone.name):

                                if self.Constraint_Type == "TRANSFORM":
                                    constraint = bone.constraints.new("COPY_TRANSFORMS")
                                    constraint.target = Target_Armature
                                    constraint.subtarget = Target_Armature.data.bones.get(bone.name).name

                                if self.Constraint_Type == "LOTROT":
                                    constraint = bone.constraints.new("COPY_LOCATION")
                                    constraint.target = Target_Armature
                                    constraint.subtarget = Target_Armature.data.bones.get(bone.name).name

                                    constraint = bone.constraints.new("COPY_ROTATION")
                                    constraint.target = Target_Armature
                                    constraint.subtarget = Target_Armature.data.bones.get(bone.name).name

                                if self.Constraint_Type == "CHILD_OF":
                                    constraint = bone.constraints.new("CHILD_OF")
                                    constraint.target = Target_Armature
                                    constraint.subtarget = Target_Armature.data.bones.get(bone.name).name
                            else:
                                self.report({"INFO"}, "Bone Not Found, Skipped " + bone.name)

        if context.mode == "POSE":

            for object in context.selected_objects:
                if object.type == "ARMATURE":
                    Editing_Armature.append(object)

            for Source_Armature in Editing_Armature:

                if Target_Armature and Source_Armature:

                    if not Target_Armature == Source_Armature:

                        if Target_Armature.type == "ARMATURE" and Source_Armature.type == "ARMATURE":

                            for bone in Source_Armature.pose.bones:

                                if bone.bone.select:

                                    if Target_Armature.data.bones.get(bone.name):

                                        if self.Constraint_Type == "TRANSFORM":
                                            constraint = bone.constraints.new("COPY_TRANSFORMS")
                                            constraint.target = Target_Armature
                                            constraint.subtarget = Target_Armature.data.bones.get(bone.name).name

                                        if self.Constraint_Type == "LOTROT":
                                            constraint = bone.constraints.new("COPY_LOCATION")
                                            constraint.target = Target_Armature
                                            constraint.subtarget = Target_Armature.data.bones.get(bone.name).name

                                            constraint = bone.constraints.new("COPY_ROTATION")
                                            constraint.target = Target_Armature
                                            constraint.subtarget = Target_Armature.data.bones.get(bone.name).name

                                        if self.Constraint_Type == "CHILD_OF":
                                            constraint = bone.constraints.new("CHILD_OF")
                                            constraint.target = Target_Armature
                                            constraint.subtarget = Target_Armature.data.bones.get(bone.name).name



        return {'FINISHED'}




classes = [RetargetHelper_Constraint_To_Armature]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
