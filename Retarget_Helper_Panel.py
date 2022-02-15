import bpy
from . import Utility_Function
import os


script_file = os.path.realpath(__file__)
addon_directory = os.path.dirname(script_file)
addon_name = os.path.basename(addon_directory)


class RETARGET_HELPER_PT_Side_Panel(bpy.types.Panel):
    """Simple Retarget Helper Tool"""
    bl_label = "Retarget Helper"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Retarget Helper"

    def draw(self, context):
        layout = self.layout


        row = layout.row(align=True)

        addon_preferences = context.preferences.addons[addon_name].preferences

        operator = row.operator("retargethelper.toogle_constraint", text="Mute", icon="HIDE_ON")
        operator.mute = True
        operator.use_selected = addon_preferences.use_selected

        operator = row.operator("retargethelper.toogle_constraint", text="Unmute", icon="HIDE_OFF")
        operator.mute = False
        operator.use_selected = addon_preferences.use_selected

        row.prop(addon_preferences, "use_selected", text="", icon="RESTRICT_SELECT_OFF")

        layout.operator("retarget_helper.extract_and_constraint", text="Extract and Constraint")
        layout.operator("retarget_helper.generate_ik_poll_finder", text="Generate IK Poll Finder")
        layout.operator("retarget_helper.actorcore_cleanup", text="Actorcore Cleanup")
        layout.operator("retarget_helper.unbind_mesh", text="Clean Unbind Mesh")
        layout.operator("retarget_helper.mixamo_cleanup", text="Mixamo Cleanup")
        layout.operator("retarget_helper.symmetrize_selected_bones", text="Symmetrize Selected Bones")
        layout.operator("retargethelper.constraint_to_armature_name", text="Constraint To Armature")




classes = [RETARGET_HELPER_PT_Side_Panel]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
