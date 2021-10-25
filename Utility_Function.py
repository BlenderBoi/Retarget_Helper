import bpy
import mathutils
import numpy

def midpoint(coordinates, mode):

    if len(coordinates) > 0:

        if mode == "BOUNDING_BOX":

            x= []
            y= []
            z= []

            for coordinate in coordinates:
                x.append(coordinate[0])
                y.append(coordinate[1])
                z.append(coordinate[2])

            range_x = (max(x), min(x))
            range_y = (max(y), min(y))
            range_z = (max(z), min(z))

            bounding_box_coordinate = []

            for a in range_x:
                for b in range_y:
                    for c in range_z:
                        bounding_box_coordinate.append((a, b, c))

            return mathutils.Vector(numpy.array(bounding_box_coordinate).mean(axis=0))

        if mode == "CENTER":
            return mathutils.Vector(numpy.array(coordinates).mean(axis=0))
    else:
        return None


def altitude(A, B, V):

    a = B-A
    b = B-B
    v = B-V

#    a = A
#    b = B
#    v = V

    x1 = a[0]
    y1 = a[1]
    z1 = a[2]

    x2 = b[0]
    y2 = b[1]
    z2 = b[2]

    x3 = v[0]
    y3 = v[1]
    z3 = v[2]

    w = (((x1 - x2) * (x3 - x2)) + ((y1 - y2) * (y3 - y2)) + ((z1 - z2) * (z3 - z2))) / (pow((x1-x2), 2) + pow((y1-y2), 2) + pow((z1-z2), 2))

    x = x2 + (w * (x2 - x1))
    y = y2 + (w * (y2 - y1))
    z = z2 + (w * (z2 - z1))

    a = mathutils.Vector((x, y, z))

    return a + B

def Calculate_Poll_Position(upper_bone, lower_bone, distance):


    up = upper_bone.head
    mid = lower_bone.head
    down = lower_bone.tail

    Altitude_Co = -altitude(up, down, mid)
    Vec = mathutils.Vector(mid) + Altitude_Co
    Mat = mathutils.Matrix.Translation(-Altitude_Co)

    pole_position = Mat @ (Vec*(distance + 1.5))


    return pole_position

def Copy_Rig(object, name):

    copy_rig = object.copy()
    copy_rig.display_type = "SOLID"
    copy_rig.show_in_front = True
    copy_rig.name = name
    copy_rig.data = object.data.copy()
    bpy.context.collection.objects.link(copy_rig)

    return copy_rig

def Extract_Rig(context, object, name ,Extract_Mode = "SELECTED", remove_animation_data=True, move_to_layer_1=True, flatten_hierarchy=False, disconnect_Bone=True, remove_custom_properties=True, remove_bbone = True, set_inherit_rotation = True, set_local_location=True, set_inherit_scale_full=True, remove_bone_shape = True, unlock_transform=True, Clear_Constraints=True):

    copy_rig = Copy_Rig(object, name)

    bpy.ops.object.mode_set(mode = 'OBJECT')

    bpy.ops.object.select_all(action='DESELECT')
    copy_rig.select_set(True)
    context.view_layer.objects.active = copy_rig
    bpy.ops.object.mode_set(mode = 'EDIT')

    Edit_Bones = copy_rig.data.edit_bones

    if remove_animation_data:

        copy_rig.animation_data_clear()
        copy_rig.data.animation_data_clear()

    if move_to_layer_1:

        for i, layer in enumerate(copy_rig.data.layers):
            if i == 0:
                copy_rig.data.layers[i] = True
            else:
                copy_rig.data.layers[i] = False

    for bone in Edit_Bones:

        if flatten_hierarchy:
            bone.parent = None
        if disconnect_Bone:
            bone.use_connect = False

        if remove_custom_properties:
            if bone.get("_RNA_UI"):
                for property in bone["_RNA_UI"]:
                    del bone[property]

        if remove_bbone:
            bone.bbone_segments = 0

        if set_inherit_rotation:
            bone.use_inherit_rotation = True

        if set_local_location:
             bone.use_local_location = True

        if set_inherit_scale_full:
             bone.inherit_scale = "FULL"

        if move_to_layer_1:
            for i, layer in enumerate(bone.layers):
                if i == 0:
                    bone.layers[i] = True
                else:
                    bone.layers[i] = False


        if Extract_Mode == "SELECTED":
            if not bone.select:
                Edit_Bones.remove(bone)

        if Extract_Mode == "DEFORM":
            if not bone.use_deform:
                Edit_Bones.remove(bone)

        if Extract_Mode == "SELECTED_DEFORM":
            if not bone.select:
                if not bone.use_deform:
                    Edit_Bones.remove(bone)

        if Extract_Mode == "DEFORM_AND_SELECTED":
            if not bone.use_deform and not bone.select:
                Edit_Bones.remove(bone)


    bpy.ops.object.mode_set(mode = 'POSE')
    copy_rig.data.bones.update()

    if remove_custom_properties:
        if copy_rig.get("_RNA_UI"):
            for property in copy_rig["_RNA_UI"]:
                del copy_rig[property]

        if copy_rig.data.get("_RNA_UI"):
            for property in copy_rig.data["_RNA_UI"]:
                del copy_rig.data[property]

    Pose_Bones = copy_rig.pose.bones

    for bone in Pose_Bones:

        if remove_custom_properties:
            if bone.get("_RNA_UI"):
                for property in bone["_RNA_UI"]:
                    del bone[property]

        if remove_bone_shape:
            bone.custom_shape = None

        if unlock_transform:
            bone.lock_location[0] = False
            bone.lock_location[1] = False
            bone.lock_location[2] = False

            bone.lock_scale[0] = False
            bone.lock_scale[1] = False
            bone.lock_scale[2] = False

            bone.lock_rotation_w = False
            bone.lock_rotation[0] = False
            bone.lock_rotation[1] = False
            bone.lock_rotation[2] = False

        if Clear_Constraints:
            for constraint in bone.constraints:
                bone.constraints.remove(constraint)

        # if self.Constraint_Type == "TRANSFORM":

    for bone in object.pose.bones:
        if copy_rig:

            if copy_rig.data.bones.get(bone.name):

                constraint = bone.constraints.new("COPY_TRANSFORMS")
                constraint.target = copy_rig
                constraint.subtarget = copy_rig.data.bones.get(bone.name).name

        # if self.Constraint_Type == "LOTROT":
        #     constraint = bone.constraints.new("COPY_LOCATION")
        #     constraint.target = object
        #     constraint.subtarget = object.data.bones.get(bone.name).name
        #
        #     constraint = bone.constraints.new("COPY_ROTATION")
        #     constraint.target = object
        #     constraint.subtarget = object.data.bones.get(bone.name).name
        #
        # if self.Constraint_Type == "NONE":
        #     pass

    bpy.ops.object.mode_set(mode = 'OBJECT')
