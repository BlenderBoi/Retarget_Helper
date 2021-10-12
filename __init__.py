
bl_info = {
    "name": "Retarget Helper",
    "author": "BlenderBoi",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "description": "A Utiity tool that provides simple complementary tools to work with other retargeting addon to help on retargeting process base on CGDive's Workflow",
    "wiki_url": "",
    "category": "Utility",
}

import bpy
from . import Preferences
from . import Retarget_Helper_Panel
from . import Extract_And_Constraint
from . import Generate_IK_Poll_Finder

modules = [Generate_IK_Poll_Finder, Retarget_Helper_Panel, Extract_And_Constraint, Preferences]

def register():
    for module in modules:

        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
