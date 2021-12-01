import bpy
from . import Utility_Function


#Boss Finger Fix

def snap_tail(object, snap_this, snap_to):
    bones = object.data.edit_bones
    bone_snap_this = bones.get(snap_this)
    bone_snap_to = bones.get(snap_to)
    snap_to_location = None

    if bone_snap_this:

        if bone_snap_to:
            bone_snap_this.tail.xyz = bone_snap_to.head

        else:

            message = snap_to + " not found"
            print(message)

            empty_find = bpy.data.objects.get(snap_to)

            if empty_find:
                message = "Found " + empty_find.name + " empty instead"
                print(message)

                bone_snap_this.tail.xyz = object.matrix_world.inverted() @ empty_find.matrix_world.to_translation()

    else:

        message = snap_this + " not found"
        print(message)




def fix_roll(bones, bone_name, vector):

    bone = bones.get(bone_name)
    if bone:
        bone.align_roll(vector)




class RetargetHelper_OT_Mixamo_Cleanup(bpy.types.Operator):
    """Mixamo Cleanup"""
    bl_idname = "retarget_helper.mixamo_cleanup"
    bl_label = "Mixamo Cleanup"
    bl_options = {'REGISTER', 'UNDO'}

    Remove_Prefix: bpy.props.BoolProperty(default=False)
    Small_Bone_Length_Threshold: bpy.props.FloatProperty(default=0.5)
    Elbow_Bend: bpy.props.FloatProperty(default=1.0)
    Small_Bone_Length_Set: bpy.props.FloatProperty(default=2.0)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "Remove_Prefix", text="Remove Prefix")
        layout.prop(self, "Small_Bone_Length_Threshold",  text="Small Bone Threshold")
        layout.prop(self, "Small_Bone_Length_Set",  text="Set Small Bone Length")
        layout.separator()
        layout.prop(self, "Elbow_Bend",  text="Elbow Bend Amount")


    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        object = context.object
        context.view_layer.update()

        if object.type == "ARMATURE":

            bpy.ops.object.mode_set(mode='EDIT')
            bones = object.data.edit_bones

            pref = ''
            #detecting the prefix (all prefixes are followed by a semicolon)
            semicolon = bones[0].name.find(":")
            if semicolon != -1:
                pref = bones[0].name[0:semicolon+1]

            #removes the prefix. In the final tool this could be optional
            #although I think removing it doesn't have any downsides
            #Some characters only work if the prefix is removed

            if self.Remove_Prefix:
                for bone in bones:
                    bone.name = bone.name[semicolon+1:]
                    pref = ''

            #left leg
            snap_tail(object, pref + 'LeftUpLeg', pref + 'LeftLeg')
            snap_tail(object, pref + 'LeftLeg', pref + 'LeftFoot')
            snap_tail(object, pref + 'LeftFoot', pref + 'LeftToeBase')
            snap_tail(object, pref + 'LeftToeBase', pref + 'LeftToe_End')

            snap_tail(object, pref + 'LeftToeBase', pref + 'LeftFootToeBase_End')

            #right leg
            snap_tail(object, pref + 'RightUpLeg', pref + 'RightLeg')
            snap_tail(object, pref + 'RightLeg', pref + 'RightFoot')
            snap_tail(object, pref + 'RightFoot', pref + 'RightToeBase')
            snap_tail(object, pref + 'RightToeBase', pref + 'RightToe_End')

            snap_tail(object, pref + 'RightToeBase', pref + 'RightFootToeBase_End')

            #fix hips bone to point up
            Hip_Bone = bones.get(pref + "Hips")

            if Hip_Bone:

                Spine_Bone = bones.get(pref + "Spine")

                if Spine_Bone:
                    Hip_Bone.tail.y = Spine_Bone.head.y

                Hip_Bone.tail.z = Hip_Bone.head.z
                Hip_Bone.tail.x = 0

            #spine
            snap_tail(object, pref + 'Spine', pref + 'Spine1')
            snap_tail(object, pref + 'Spine1', pref + 'Spine2')
            #some rigs have a second neck bone 'Neck1' and some don't
            if bones.find('Neck1') != -1:
                snap_tail(object, pref + 'Neck', pref + 'Neck1')
                snap_tail(object, pref + 'Neck1', pref + 'Head')
            else:
                snap_tail(object, pref + 'Neck', pref + 'Head')
            snap_tail(object, pref + 'Head', pref + 'HeadTop_End')

            #left arm
            snap_tail(object, pref + 'LeftShoulder', pref + 'LeftArm')
            snap_tail(object, pref + 'LeftArm', pref + 'LeftForeArm')
            snap_tail(object, pref + 'LeftForeArm', pref + 'LeftHand')

            #Right arm
            snap_tail(object, pref + 'RightShoulder', pref + 'RightArm')
            snap_tail(object, pref + 'RightArm', pref + 'RightForeArm')
            snap_tail(object, pref + 'RightForeArm', pref + 'RightHand')

            #left arm finers
            snap_tail(object, pref + 'LeftHandPinky1', pref + 'LeftHandPinky2')
            snap_tail(object, pref + 'LeftHandPinky2', pref + 'LeftHandPinky3')
            snap_tail(object, pref + 'LeftHandPinky3', pref + 'LeftHandPinky4')

            snap_tail(object, pref + 'LeftHandRing1', pref + 'LeftHandRing2')
            snap_tail(object, pref + 'LeftHandRing2', pref + 'LeftHandRing3')
            snap_tail(object, pref + 'LeftHandRing3', pref + 'LeftHandRing4')

            snap_tail(object, pref + 'LeftHandMiddle1', pref + 'LeftHandMiddle2')
            snap_tail(object, pref + 'LeftHandMiddle2', pref + 'LeftHandMiddle3')
            snap_tail(object, pref + 'LeftHandMiddle3', pref + 'LeftHandMiddle4')

            snap_tail(object, pref + 'LeftHandIndex1', pref + 'LeftHandIndex2')
            snap_tail(object, pref + 'LeftHandIndex2', pref + 'LeftHandIndex3')
            snap_tail(object, pref + 'LeftHandIndex3', pref + 'LeftHandIndex4')

            snap_tail(object, pref + 'LeftHandThumb1', pref + 'LeftHandThumb2')
            snap_tail(object, pref + 'LeftHandThumb2', pref + 'LeftHandThumb3')
            snap_tail(object, pref + 'LeftHandThumb3', pref + 'LeftHandThumb4')

            #Right arm finers
            snap_tail(object, pref + 'RightHandPinky1', pref + 'RightHandPinky2')
            snap_tail(object, pref + 'RightHandPinky2', pref + 'RightHandPinky3')
            snap_tail(object, pref + 'RightHandPinky3', pref + 'RightHandPinky4')

            snap_tail(object, pref + 'RightHandRing1', pref + 'RightHandRing2')
            snap_tail(object, pref + 'RightHandRing2', pref + 'RightHandRing3')
            snap_tail(object, pref + 'RightHandRing3', pref + 'RightHandRing4')

            snap_tail(object, pref + 'RightHandMiddle1', pref + 'RightHandMiddle2')
            snap_tail(object, pref + 'RightHandMiddle2', pref + 'RightHandMiddle3')
            snap_tail(object, pref + 'RightHandMiddle3', pref + 'RightHandMiddle4')

            snap_tail(object, pref + 'RightHandIndex1', pref + 'RightHandIndex2')
            snap_tail(object, pref + 'RightHandIndex2', pref + 'RightHandIndex3')
            snap_tail(object, pref + 'RightHandIndex3', pref + 'RightHandIndex4')

            snap_tail(object, pref + 'RightHandThumb1', pref + 'RightHandThumb2')
            snap_tail(object, pref + 'RightHandThumb2', pref + 'RightHandThumb3')
            snap_tail(object, pref + 'RightHandThumb3', pref + 'RightHandThumb4')



            #FIX ROLL LEGS
            fix_roll(bones, pref + 'LeftUpLeg', [0,0,1])
            fix_roll(bones, pref + 'LeftLeg', [0,0,1])
            fix_roll(bones, pref + 'LeftFoot', [0,0,1])
            fix_roll(bones, pref + 'LeftToeBase', [0,1,0])
            fix_roll(bones, pref + 'LeftToe_End', [0,1,0])

            fix_roll(bones, pref + 'RightUpLeg', [0,0,1])
            fix_roll(bones, pref + 'RightLeg', [0,0,1])
            fix_roll(bones, pref + 'RightFoot', [0,0,1])
            fix_roll(bones, pref + 'RightToeBase', [0,1,0])
            fix_roll(bones, pref + 'RightToe_End', [0,1,0])

            fix_roll(bones, pref + 'LeftShoulder', [0,-1,0])
            fix_roll(bones, pref + 'LeftArm', [0,-1,0])
            fix_roll(bones, pref + 'LeftForeArm', [0,-1,0])
            fix_roll(bones, pref + 'LeftHand', [0,-1,0])

            fix_roll(bones, pref + 'RightShoulder', [0,-1,0])
            fix_roll(bones, pref + 'RightArm', [0,-1,0])
            fix_roll(bones, pref + 'RightForeArm', [0,-1,0])
            fix_roll(bones, pref + 'RightHand', [0,-1,0])

            #FIX ROLL FINGERS
            #Left
            fix_roll(bones, pref + 'LeftHandPinky1', [0,-1,0])
            fix_roll(bones, pref + 'LeftHandPinky2', [0,-1,0])
            fix_roll(bones, pref + 'LeftHandPinky3', [0,-1,0])
            fix_roll(bones, pref + 'LeftHandPinky4', [0,-1,0])

            fix_roll(bones, pref + 'LeftHandRing1', [0,-1,0])
            fix_roll(bones, pref + 'LeftHandRing2', [0,-1,0])
            fix_roll(bones, pref + 'LeftHandRing3', [0,-1,0])
            fix_roll(bones, pref + 'LeftHandRing4', [0,-1,0])

            fix_roll(bones, pref + 'LeftHandMiddle1', [0,-1,0])
            fix_roll(bones, pref + 'LeftHandMiddle2', [0,-1,0])
            fix_roll(bones, pref + 'LeftHandMiddle3', [0,-1,0])
            fix_roll(bones, pref + 'LeftHandMiddle4', [0,-1,0])

            fix_roll(bones, pref + 'LeftHandIndex1', [0,-1,0])
            fix_roll(bones, pref + 'LeftHandIndex2', [0,-1,0])
            fix_roll(bones, pref + 'LeftHandIndex3', [0,-1,0])
            fix_roll(bones, pref + 'LeftHandIndex4', [0,-1,0])

            fix_roll(bones, pref + 'LeftHandThumb1', [0,-1,0])
            fix_roll(bones, pref + 'LeftHandThumb2', [0,-1,0])
            fix_roll(bones, pref + 'LeftHandThumb3', [0,-1,0])
            fix_roll(bones, pref + 'LeftHandThumb4', [0,-1,0])

            #Right
            fix_roll(bones, pref + 'RightHandPinky1', [0,-1,0])
            fix_roll(bones, pref + 'RightHandPinky2', [0,-1,0])
            fix_roll(bones, pref + 'RightHandPinky3', [0,-1,0])
            fix_roll(bones, pref + 'RightHandPinky4', [0,-1,0])

            fix_roll(bones, pref + 'RightHandRing1', [0,-1,0])
            fix_roll(bones, pref + 'RightHandRing2', [0,-1,0])
            fix_roll(bones, pref + 'RightHandRing3', [0,-1,0])
            fix_roll(bones, pref + 'RightHandRing4', [0,-1,0])

            fix_roll(bones, pref + 'RightHandMiddle1', [0,-1,0])
            fix_roll(bones, pref + 'RightHandMiddle2', [0,-1,0])
            fix_roll(bones, pref + 'RightHandMiddle3', [0,-1,0])
            fix_roll(bones, pref + 'RightHandMiddle4', [0,-1,0])

            fix_roll(bones, pref + 'RightHandIndex1', [0,-1,0])
            fix_roll(bones, pref + 'RightHandIndex2', [0,-1,0])
            fix_roll(bones, pref + 'RightHandIndex3', [0,-1,0])
            fix_roll(bones, pref + 'RightHandIndex4', [0,-1,0])

            fix_roll(bones, pref + 'RightHandThumb1', [0,-1,0])
            fix_roll(bones, pref + 'RightHandThumb2', [0,-1,0])
            fix_roll(bones, pref + 'RightHandThumb3', [0,-1,0])
            fix_roll(bones, pref + 'RightHandThumb4', [0,-1,0])

            fix_roll(bones, pref + 'Hips', [0,0,1])

            #bend the elbows
            #the same could be included for the knees but all rigs
            #seem to generate fine without it
            LeftArm_Bone = bones.get(pref + "LeftArm")
            if LeftArm_Bone:
                LeftArm_Bone.tail.z -= self.Elbow_Bend

            LeftForeArm_Bone = bones.get(pref + "LeftForeArm")
            if LeftForeArm_Bone:
                LeftForeArm_Bone.head.z -= self.Elbow_Bend

            RightArm_Bone = bones.get(pref + "RightArm")
            if RightArm_Bone:
                RightArm_Bone.tail.z -= self.Elbow_Bend

            RightForeArm_Bone = bones.get(pref + "RightForeArm")
            if RightForeArm_Bone:
                RightForeArm_Bone.head.z -= self.Elbow_Bend

            #some rigs feature zero length bones so I tried to fix it :)
            for bone in bones:
                if bone.length < self.Small_Bone_Length_Threshold:
                    bone.length = self.Small_Bone_Length_Set



        return {'FINISHED'}



classes = [RetargetHelper_OT_Mixamo_Cleanup]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
