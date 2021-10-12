import bpy
from . import Utility_Function

class RetargetHelper_OT_Extract_And_Constraint(bpy.types.Operator):
    """Extract and Constraint"""
    bl_idname = "retarget_helper.extract_and_constraint"
    bl_label = "Extract and Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    name: bpy.props.StringProperty()


    def invoke(self, context, event):

        object = context.object
        if object:
            self.name = "Extract_" + object.name
        return context.window_manager.invoke_props_dialog(self)


    @classmethod
    def poll(cls, context):
        if context.mode in ["POSE", "EDIT_ARMATURE"]:
            return True

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name", text="Name")

    def execute(self, context):

        object = context.object
        mode = context.mode

        if object:
            Utility_Function.Extract_Rig(context, object, self.name)




        return {'FINISHED'}



classes = [RetargetHelper_OT_Extract_And_Constraint]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
