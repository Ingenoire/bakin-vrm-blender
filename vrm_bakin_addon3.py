bl_info = {
    "name": "Bakin VRM",
    "author": "ingenoire",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf > Run Script Button",
    "description": "Adds a button that creates itemhook bones and shape keys for both eye and head movement for VRoid VRM characters, for use with RPG Developer Bakin.",
    "category": "Development",
}

import bpy

class RunScriptButton(bpy.types.Operator):
    bl_idname = "object.run_script"
    bl_label = "Add Item Hooks & Shape Keys"
    

    def execute(self, context):
        # Your script goes here
        import math
        import mathutils
        
        # Push the current state to the undo stack
        bpy.ops.ed.undo_push(message="Run VRM Bakin Utils")

        # Check and delete the "glTF_not_exported" collection if it exists
        if "glTF_not_exported" in bpy.data.collections:
            bpy.data.collections.remove(bpy.data.collections["glTF_not_exported"])

        # Check and delete the "Icosphere" mesh if it exists
        if "Icosphere" in bpy.data.meshes:
            bpy.data.meshes.remove(bpy.data.meshes["Icosphere"])
            
        # Select the armature and enter edit mode
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['Armature'].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['Armature']
        bpy.ops.object.mode_set(mode='EDIT')

        # Select the J_Bip_L_Hand bone
        bpy.ops.armature.select_all(action='DESELECT')
        hand_bone = bpy.data.armatures['Armature'].edit_bones['J_Bip_L_Hand']
        hand_bone.select = True

        # Add a new bone called L_itemhook at the same position as J_Bip_L_Hand
        new_bone = bpy.data.armatures['Armature'].edit_bones.new('L_itemhook')

        # Position the head and tail of the new bone to simulate a rotation by -90° on the Z axis
        new_bone.head = hand_bone.head + mathutils.Vector((0.06, 0.04, -0.02))
        new_bone.tail = hand_bone.head + mathutils.Vector((hand_bone.tail.y - hand_bone.head.y, -hand_bone.tail.x + hand_bone.head.x, 0)) + mathutils.Vector((0.06, 0.04, -0.02))

        # Parent the L_itemhook bone to the J_Bip_L_Hand bone
        new_bone.parent = hand_bone
        new_bone.use_connect = False  # This keeps the offset when parenting

        bpy.ops.armature.select_all(action='DESELECT')
        hand_bone = bpy.data.armatures['Armature'].edit_bones['J_Bip_R_Hand']
        hand_bone.select = True

        # Add a new bone called R_itemhook at the same position as J_Bip_R_Hand
        new_bone = bpy.data.armatures['Armature'].edit_bones.new('R_itemhook')

        # Position the head and tail of the new bone to simulate a rotation by 90° on the Z axis
        new_bone.head = hand_bone.head + mathutils.Vector((-0.06, 0.04, -0.02))
        new_bone.tail = hand_bone.head + mathutils.Vector((hand_bone.tail.y - hand_bone.head.y, hand_bone.tail.x - hand_bone.head.x, 0)) + mathutils.Vector((-0.06, 0.04, -0.02))

        # Parent the R_itemhook bone to the J_Bip_R_Hand bone
        new_bone.parent = hand_bone
        new_bone.use_connect = False  # This keeps the offset when parenting

        # Switch back to object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Define the rotations for each shape key
        rotations = {
            "EYE_LR_RIGHT": ('Z', math.radians(-8), 'J_Adj_L_FaceEye', 'J_Adj_R_FaceEye'),
            "EYE_LR_LEFT": ('Z', math.radians(12), 'J_Adj_L_FaceEye', 'J_Adj_R_FaceEye'),
            "EYE_LR_UP": ('X', math.radians(-10), 'J_Adj_L_FaceEye', 'J_Adj_R_FaceEye'),
            "EYE_LR_DOWN": ('X', math.radians(10), 'J_Adj_L_FaceEye', 'J_Adj_R_FaceEye'),
            "EYE_R_INNER": ('Z', math.radians(-8), 'J_Adj_R_FaceEye'),
            "EYE_R_OUTER": ('Z', math.radians(12), 'J_Adj_R_FaceEye'),
            "EYE_R_UP": ('X', math.radians(-10), 'J_Adj_R_FaceEye'),
            "EYE_R_DOWN": ('X', math.radians(10), 'J_Adj_R_FaceEye'),
            "EYE_L_INNER": ('Z', math.radians(8), 'J_Adj_L_FaceEye'),
            "EYE_L_OUTER": ('Z', math.radians(-12), 'J_Adj_L_FaceEye'),
            "EYE_L_UP": ('X', math.radians(-10), 'J_Adj_L_FaceEye'),
            "EYE_L_DOWN": ('X', math.radians(10), 'J_Adj_L_FaceEye'),
            "HAIR_UP": ('X', math.radians(-30), 'J_Bip_C_Head'),
            "HAIR_DOWN": ('X', math.radians(30), 'J_Bip_C_Head'),
            "HAIR_LEFT": ('Y', math.radians(-30), 'J_Bip_C_Head'),
            "HAIR_RIGHT": ('Y', math.radians(30), 'J_Bip_C_Head'),
            "HAIR_TILT_LEFT": ('Z', math.radians(30), 'J_Bip_C_Head'),
            "HAIR_TILT_RIGHT": ('Z', math.radians(-30), 'J_Bip_C_Head'),
            "HEAD_UP": ('X', math.radians(-30), 'J_Bip_C_Head'),
            "HEAD_DOWN": ('X', math.radians(30), 'J_Bip_C_Head'),
            "HEAD_LEFT": ('Y', math.radians(-30), 'J_Bip_C_Head'),
            "HEAD_RIGHT": ('Y', math.radians(30), 'J_Bip_C_Head'),
            "HEAD_TILT_LEFT": ('Z', math.radians(30), 'J_Bip_C_Head'),
            "HEAD_TILT_RIGHT": ('Z', math.radians(-30), 'J_Bip_C_Head'),
        }

        # Select the armature and enter pose mode
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['Armature'].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['Armature']
        bpy.ops.object.mode_set(mode='POSE')

        # Store the initial pose
        initial_pose = {bone: bone.rotation_euler.copy() for bone in bpy.data.objects['Armature'].pose.bones}

        for shape_key_name, rotation_data in rotations.items():
            axis, angle, *bones = rotation_data

            for bone_name in bones:
                # Select the bone and rotate it
                bpy.data.objects['Armature'].pose.bones[bone_name].rotation_mode = 'XYZ'
                if axis == 'Z':
                    bpy.data.objects['Armature'].pose.bones[bone_name].rotation_euler[2] += angle
                elif axis == 'X':
                    bpy.data.objects['Armature'].pose.bones[bone_name].rotation_euler[0] += angle
                elif axis == 'Y':
                    bpy.data.objects['Armature'].pose.bones[bone_name].rotation_euler[1] += angle

            # Apply the pose as a shape key
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            
            # Choose the correct mesh for the shape key
            if "HAIR" in shape_key_name:
                bpy.data.objects['Body'].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects['Body']
            else:
                bpy.data.objects['Face'].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects['Face']

            # Apply the armature modifier as a shape key
            bpy.ops.object.modifier_apply_as_shapekey(modifier="Armature")

            # Rename the shape key
            bpy.context.object.data.shape_keys.key_blocks[-1].name = shape_key_name

            # Re-add the armature modifier
            bpy.ops.object.modifier_add(type='ARMATURE')
            bpy.context.object.modifiers["Armature"].object = bpy.data.objects["Armature"]

            # Reset the bone rotation to the initial pose
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects['Armature'].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects['Armature']
            bpy.ops.object.mode_set(mode='POSE')
            for bone in bpy.data.objects['Armature'].pose.bones:
                bone.rotation_euler = initial_pose[bone]

        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}

import os

class ExportFBXButton(bpy.types.Operator):
    bl_idname = "object.export_fbx"
    bl_label = "Export FBX + DEF"

    def invoke(self, context, event):
        # Check if the current file has been saved
        if bpy.data.is_saved == False:
            # Display a pop-up dialog
            return context.window_manager.invoke_props_dialog(self)
        else:
            # If the file has been saved, proceed with the export
            return self.execute(context)

    def draw(self, context):
        layout = self.layout
        layout.label(text="You need to save a blend file of this scene first before we can export the FBX and DEF files!")
        

    def execute(self, context):
        try:
            # Prompt the user to save the file
            result = bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')

            # If the user cancels the save operation, stop the export process
            if 'CANCELLED' in result:
                return {'CANCELLED'}
                
            # Get the name of the VRM model and replace spaces with underscores
            vrm_model_name = bpy.data.objects['Armature'].data.vrm_addon_extension.vrm1.meta['vrm_name'].replace(' ', '_')
            
            # Define the directory for the exported textures
            dirpath = bpy.path.abspath("//" + vrm_model_name + " (Bakin Export)")

            # Create the directory if it doesn't exist
            os.makedirs(dirpath, exist_ok=True)
            
            # Save all the images as PNGs and rename them
            for image in bpy.data.images:
                if not image.has_data or image.type != 'IMAGE':
                    continue
                new_image_name = vrm_model_name + "_" + image.name
                image.save_render(os.path.join(dirpath, new_image_name + ".png"))

            # Define the filepath for the exported FBX file
            filepath = os.path.join(dirpath, vrm_model_name + ".fbx")

            # Export the entire scene as an FBX with the specified parameters
            bpy.ops.export_scene.fbx(
                filepath=filepath,
                use_selection=False,
                global_scale=0.01,
                use_mesh_modifiers=False,
                add_leaf_bones=False,
                use_tspace=True  # Enable Tangent Space
            )

            # Create a .def file with the same name as the VRM model
            with open(os.path.join(dirpath, vrm_model_name + ".def"), 'w') as f:
                f.write('mtl N00_000_00_FaceMouth_00_FACE (Instance)\n')
                f.write('shader toon c3a93e68844545618e04eb31f52898c8\n')
                f.write('emissiveBlink false\n')
                f.write('emissiveBlinkSpeed 0.000000\n')
                f.write('emissiveLinkBuildingLight false\n')
                f.write('uscrollanim false\n')
                f.write('vscrollanim false\n')
                f.write('scrollanimspeed 0.000000 0.000000\n')
                f.write('uvstepanim false\n')
                f.write('uvstepanimparam 1 1 0 1.000000\n')
                f.write('sortindex 0\n')
                f.write('castshadow true\n')
                f.write('cull back\n')
                f.write('drawOutline false\n')
                f.write('outlineWidth 1.000000\n')
                f.write('outlineColor 0.000000 0.000000 0.000000 1.000000\n')
                f.write('overrideOutlineSetting false\n')
                f.write('distanceFade false\n')
                f.write('uvofs 0.000000 0.000000\n')
                f.write('uvscl 1.000000 1.000000\n')
                f.write('RenderingType Cutoff\n')
                f.write('LitMap ' + vrm_model_name + '_Image_0.png\n')
                f.write('LitColor 1.000000 1.000000 1.000000 1.000000\n')
                f.write('ShadeMap ' + vrm_model_name + '_Image_7.png\n')
                f.write('ShadeColor 0.600000 0.600000 0.600000 1.000000\n')
                f.write('NormalMap ' + vrm_model_name + '_Image_2.png\n')
                f.write('normalscl 1.000000\n')
                f.write('toony 0.900000\n')
                f.write('shift 0.000000\n')
                f.write('LitShaderMixTexMult 0.000000\n')
                f.write('lightColorAtt 0.000000\n')
                f.write('EmiMap ' + vrm_model_name + '_Image_1.png\n')
                f.write('Emission 1.000000 1.000000 1.000000\n')
                f.write('EmissionInt 1.000000\n')
                f.write('MCMap MatcapWarp.png\n')
                f.write('matCapScale 1.000000\n')
                f.write('Rim 0.000000 0.000000 0.000000\n')
                f.write('RimInt 1.000000\n')
                f.write('RimLightingMix 0.000000\n')
                f.write('RimFresnelPow 0.000000\n')
                f.write('RimLift 0.000000\n')
                f.write('cutOffThreshold 0.600000\n')
                f.write('outlineType World\n')
                f.write('outlineWeight ' + vrm_model_name + '_Image_9.png\n')
                f.write('outlineMaxScale 1.000000\n')
                f.write('outlineMixLighting 0.000000\n')
                f.write('UVRotateAnimation 0.000000\n')
                f.write('\n')
                f.write('mtl N00_000_00_Body_00_SKIN (Instance)\n')
                f.write('shader toon c3a93e68844545618e04eb31f52898c8\n')
                f.write('emissiveBlink false\n')
                f.write('emissiveBlinkSpeed 0.000000\n')
                f.write('emissiveLinkBuildingLight false\n')
                f.write('uscrollanim false\n')
                f.write('vscrollanim false\n')
                f.write('scrollanimspeed 0.000000 0.000000\n')
                f.write('uvstepanim false\n')
                f.write('uvstepanimparam 1 1 0 1.000000\n')
                f.write('sortindex 0\n')
                f.write('castshadow true\n')
                f.write('cull none\n')
                f.write('drawOutline false\n')
                f.write('outlineWidth 1.000000\n')
                f.write('outlineColor 0.000000 0.000000 0.000000 1.000000\n')
                f.write('overrideOutlineSetting false\n')
                f.write('distanceFade false\n')
                f.write('uvofs 0.000000 0.000000\n')
                f.write('uvscl 1.000000 1.000000\n')
                f.write('RenderingType Cutoff\n')
                f.write('LitMap ' + vrm_model_name + '_Image_3.png\n')
                f.write('LitColor 1.000000 1.000000 1.000000 1.000000\n')
                f.write('ShadeMap ' + vrm_model_name + '_Image_10.png\n')
                f.write('ShadeColor 0.600000 0.600000 0.600000 1.000000\n')
                f.write('NormalMap ' + vrm_model_name + '_Image_5.png\n')
                f.write('normalscl 1.000000\n')
                f.write('toony 0.900000\n')
                f.write('shift 0.000000\n')
                f.write('LitShaderMixTexMult 0.000000\n')
                f.write('lightColorAtt 0.000000\n')
                f.write('EmiMap ' + vrm_model_name + '_Image_4.png\n')
                f.write('Emission 1.000000 1.000000 1.000000\n')
                f.write('EmissionInt 0.300000\n')
                f.write('MCMap MatcapWarp.png\n')
                f.write('matCapScale 1.000000\n')
                f.write('Rim 0.000000 0.000000 0.000000\n')
                f.write('RimInt 1.000000\n')
                f.write('RimLightingMix 0.000000\n')
                f.write('RimFresnelPow 0.000000\n')
                f.write('RimLift 0.000000\n')
                f.write('cutOffThreshold 0.900000\n')
                f.write('outlineType World\n')
                f.write('outlineWeight ' + vrm_model_name + '_Image_11.png\n')
                f.write('outlineMaxScale 1.000000\n')
                f.write('outlineMixLighting 0.000000\n')
                f.write('UVRotateAnimation 0.000000\n')


        except Exception as e:
            print("Failed to export FBX: ", e)

        return {'FINISHED'}


import os
import bpy

class ImportVRMButton(bpy.types.Operator):
    bl_idname = "object.import_vrm"
    bl_label = "Import VRM"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")  # Add this line

    def execute(self, context):
        try:
            bpy.ops.import_scene.vrm('INVOKE_DEFAULT')
            print("Imported VRM file from: ", self.filepath)  # Print the filepath

            # Delete any image from the scene that doesn't start with either "Image_", "Matcap" or "Thumbnail"
            for image in bpy.data.images:
                if not image.name.startswith(("Image_", "Matcap", "Thumbnail")):
                    bpy.data.images.remove(image)

        except Exception as e:
            print("Failed to import VRM: ", e)

        return {'FINISHED'}

class RunScriptButtonPanel(bpy.types.Panel):
    bl_label = "VRoid for Bakin"
    bl_idname = "OBJECT_PT_run_script"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout

        # Add a button to the panel that calls the ImportVRMButton operator
        layout.operator("object.import_vrm")

        # Add a button to the panel that calls the RunScriptButton operator
        layout.operator("object.run_script")

        # Add a button to the panel that calls the ExportFBXButton operator
        layout.operator("object.export_fbx")


def register():
    bpy.utils.register_class(ImportVRMButton)
    bpy.utils.register_class(RunScriptButton)
    bpy.utils.register_class(ExportFBXButton)
    bpy.utils.register_class(RunScriptButtonPanel)

def unregister():
    bpy.utils.unregister_class(ImportVRMButton)
    bpy.utils.unregister_class(RunScriptButton)
    bpy.utils.unregister_class(ExportFBXButton)
    bpy.utils.unregister_class(RunScriptButtonPanel)

if __name__ == "__main__":
    register()