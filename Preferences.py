import bpy
import os
import pathlib

from . import Retarget_Helper_Panel

script_file = os.path.realpath(__file__)
addon_directory = os.path.dirname(script_file)
addon_name = os.path.basename(addon_directory)


def update_panel(self, context):

    addon_preferences = context.preferences.addons[addon_name].preferences
    message = ": Updating Panel locations has failed"
    try:

        if "bl_rna" in Retarget_Helper_Panel.RETARGET_HELPER_PT_Side_Panel.__dict__:
            bpy.utils.unregister_class(Retarget_Helper_Panel.RETARGET_HELPER_PT_Side_Panel)


        Retarget_Helper_Panel.RETARGET_HELPER_PT_Side_Panel.bl_category = addon_preferences.Retarget_Helper_Panel_Name
        bpy.utils.register_class(Retarget_Helper_Panel.RETARGET_HELPER_PT_Side_Panel)




    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        pass



class Retarget_Helper_user_preferences(bpy.types.AddonPreferences):

    bl_idname = addon_name

    Retarget_Helper_Panel_Name: bpy.props.StringProperty(default="Retarget Helper", update=update_panel)
    use_selected: bpy.props.BoolProperty(default=True)

    def draw(self, context):

        layout = self.layout
        layout.prop(self, "Retarget_Helper_Panel_Name", text="Panel Name")


classes = [Retarget_Helper_user_preferences]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    update_panel(None, bpy.context)

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
