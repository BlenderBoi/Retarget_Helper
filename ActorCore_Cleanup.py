import bpy

class RetargetHelper_OT_Actorcore_Cleanup(bpy.types.Operator):
    """Actorcore Cleanup"""
    bl_idname = "retarget_helper.actorcore_cleanup"
    bl_label = "Actorcore Cleanup"
    bl_options = {'REGISTER', 'UNDO'}

    finger_bones_layer: bpy.props.IntProperty(name= "Finger Bones", default=1, min=0, max=31)
    toe_bones_layer: bpy.props.IntProperty(name="Toe Bones", default=2, min=0, max=31)
    face_bones_layer: bpy.props.IntProperty(name="Face Bones", default=3, min=0, max=31)
    twist_bones_layer: bpy.props.IntProperty(name="Twist Bones", default=4, min=0, max=31)
    other_bones_layer: bpy.props.IntProperty(name="Other Bones", default=5, min=0, max=31)
    root_bones_layer: bpy.props.IntProperty(name="Root Bones", default=6, min=0, max=31)

    SHOW_LENGTH: bpy.props.BoolProperty(default=True)

    length_upper_arm: bpy.props.FloatProperty(name="Upper Arm", default=25)
    length_forearm: bpy.props.FloatProperty(name="Forearm", default=24)
    length_hip: bpy.props.FloatProperty(name="Hip", default=10)
    length_thigh: bpy.props.FloatProperty(name="Thigh", default=47)
    length_calf: bpy.props.FloatProperty(name="Calf", default=48)
    length_head: bpy.props.FloatProperty(name="Head", default=20)
    length_toe: bpy.props.FloatProperty(name="Toe", default=10)

    @classmethod
    def poll(cls, context):
        if context.mode == "OBJECT":
            return True

    def draw(self, context):

        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Layers")
        col.prop(self, "finger_bones_layer")
        col.prop(self, "toe_bones_layer")
        col.prop(self, "face_bones_layer")
        col.prop(self, "twist_bones_layer")
        col.prop(self, "other_bones_layer")
        col.prop(self, "root_bones_layer")

        if self.SHOW_LENGTH:
            col.separator()
            col.label(text="Length")
            col.prop(self, "length_upper_arm")
            col.prop(self, "length_forearm")
            col.prop(self, "length_hip")
            col.prop(self, "length_thigh")
            col.prop(self, "length_calf")
            col.prop(self, "length_head")
            col.prop(self, "length_toe")

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        object = context.object

        if object:
            if object.type == "ARMATURE":
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

                finger_bones = ['CC_Base_L_Mid1', 'CC_Base_L_Mid2', 'CC_Base_L_Mid3', 'CC_Base_L_Index1', 'CC_Base_L_Index2', 'CC_Base_L_Index3', 'CC_Base_L_Ring1', 'CC_Base_L_Ring2', 'CC_Base_L_Ring3', 'CC_Base_L_Pinky1', 'CC_Base_L_Pinky2', 'CC_Base_L_Pinky3', 'CC_Base_L_Thumb1', 'CC_Base_L_Thumb2', 'CC_Base_L_Thumb3', 'CC_Base_R_Mid1', 'CC_Base_R_Mid2', 'CC_Base_R_Mid3', 'CC_Base_R_Ring1', 'CC_Base_R_Ring2', 'CC_Base_R_Ring3', 'CC_Base_R_Thumb1', 'CC_Base_R_Thumb2', 'CC_Base_R_Thumb3', 'CC_Base_R_Index1', 'CC_Base_R_Index2', 'CC_Base_R_Index3', 'CC_Base_R_Pinky1', 'CC_Base_R_Pinky2', 'CC_Base_R_Pinky3']

                toe_bones = ['CC_Base_L_PinkyToe1', 'CC_Base_L_RingToe1', 'CC_Base_L_MidToe1', 'CC_Base_L_IndexToe1', 'CC_Base_L_BigToe1', 'CC_Base_R_PinkyToe1', 'CC_Base_R_BigToe1', 'CC_Base_R_IndexToe1', 'CC_Base_R_MidToe1', 'CC_Base_R_RingToe1']

                face_bones = ['CC_Base_FacialBone', 'CC_Base_JawRoot', 'CC_Base_Tongue01', 'CC_Base_Tongue02', 'CC_Base_Tongue03', 'CC_Base_Teeth02', 'CC_Base_R_Eye', 'CC_Base_L_Eye', 'CC_Base_UpperJaw', 'CC_Base_Teeth01']

                twist_bones = ['CC_Base_L_CalfTwist01', 'CC_Base_L_CalfTwist02', 'CC_Base_L_ThighTwist01', 'CC_Base_L_ThighTwist02', 'CC_Base_R_ThighTwist01', 'CC_Base_R_ThighTwist02', 'CC_Base_R_CalfTwist01', 'CC_Base_R_CalfTwist02', 'CC_Base_L_ForearmTwist01', 'CC_Base_L_ForearmTwist02', 'CC_Base_L_UpperarmTwist01', 'CC_Base_L_UpperarmTwist02', 'CC_Base_R_UpperarmTwist01', 'CC_Base_R_UpperarmTwist02', 'CC_Base_R_ForearmTwist01', 'CC_Base_R_ForearmTwist02']

                other_bones = ['CC_Base_Pelvis', 'CC_Base_L_ToeBaseShareBone', 'CC_Base_L_KneeShareBone', 'CC_Base_R_ToeBaseShareBone', 'CC_Base_R_KneeShareBone', 'CC_Base_L_ElbowShareBone', 'CC_Base_R_ElbowShareBone', 'CC_Base_R_RibsTwist', 'CC_Base_R_Breast', 'CC_Base_L_RibsTwist', 'CC_Base_L_Breast']










                #move finger bones to layer 1
                for name in finger_bones:

                    bone = object.data.bones.get(name)

                    if bone:
                        bone.layers[self.finger_bones_layer] = True
                        bone.layers[0] = False

                #move toe bones to layer 2
                for name in toe_bones:

                    bone = object.data.bones.get(name)
                    if bone:
                        bone.layers[self.toe_bones_layer] = True
                        bone.layers[0] = False

                #move face bones to layer 3
                for name in face_bones:

                    bone = object.data.bones.get(name)
                    if bone:

                        bone.layers[self.face_bones_layer] = True
                        bone.layers[0] = False

                #move twist bones to layer 4
                for name in twist_bones:

                    bone = object.data.bones.get(name)
                    if bone:

                        bone.layers[self.twist_bones_layer] = True
                        bone.layers[0] = False

                #move other bones to layer 5
                for name in other_bones:

                    bone = object.data.bones.get(name)
                    if bone:
                        bone.layers[self.other_bones_layer] = True
                        bone.layers[0] = False

                #move root bone to layer 6
                bone = object.data.bones.get('CC_Base_BoneRoot')
                bone.layers[self.root_bones_layer] = True
                bone.layers[0] = False

                bpy.ops.object.mode_set(mode='EDIT', toggle=False)

                #resize a bunch of bones that are always imported too small

                length_bone_pair = [
                ("CC_Base_L_Upperarm", self.length_upper_arm),
                ("CC_Base_R_Upperarm", self.length_upper_arm),
                ("CC_Base_L_Forearm", self.length_forearm),
                ("CC_Base_R_Forearm", self.length_forearm),
                ("CC_Base_Hip", self.length_hip),
                ("CC_Base_L_Thigh", self.length_thigh),
                ("CC_Base_R_Thigh", self.length_thigh),
                ("CC_Base_L_Calf", self.length_calf),
                ("CC_Base_R_Calf", self.length_calf),
                ("CC_Base_Head", self.length_head),
                ("CC_Base_L_ToeBase", self.length_toe),
                ("CC_Base_R_ToeBase", self.length_toe),
                ]

                for pair in length_bone_pair:
                    bone = object.data.edit_bones.get(pair[0])
                    if bone:
                        bone.length = pair[1]

                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        return {'FINISHED'}


classes = [RetargetHelper_OT_Actorcore_Cleanup]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
