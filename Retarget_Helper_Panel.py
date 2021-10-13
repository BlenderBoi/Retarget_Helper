import bpy
from . import Utility_Function

class RETARGET_HELPER_PT_Side_Panel(bpy.types.Panel):
    """Simple Retarget Helper Tool"""
    bl_label = "Retarget Helper"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Retarget Helper"

    def draw(self, context):
        layout = self.layout
        layout.operator("retarget_helper.extract_and_constraint", text="Extract and Constraint")
        layout.operator("retarget_helper.generate_ik_poll_finder", text="Generate IK Poll Finder")
        layout.operator("retarget_helper.actorcore_cleanup", text="Actorcore Cleanup")



classes = [RETARGET_HELPER_PT_Side_Panel]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
