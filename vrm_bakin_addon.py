bl_info = {
    "name": "Bakin VRM",
    "author": "ingenoire",
    "version": (3, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf > Run Script Button",
    "description": "Adds buttons that create itemhook bones and shape keys for both eye and head movement for VRoid VRM characters, for use with RPG Developer Bakin.",
    "category": "Development",
}

import bpy
import os
import math
import mathutils
import textwrap

class AddItemHooksButton(bpy.types.Operator):
    bl_idname = "object.add_item_hooks"
    bl_label = "Add Item Hooks"
    bl_description = "Adds Item Hook bones to the left and right hand of the VRM model. This will let you hold items in either hand using the 'Attach Model to Cast' event in Bakin."


    def execute(self, context):
        # Your script for adding item hooks goes here
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

        # Add item hook bones to both hands
        for hand_bone_name in ['J_Bip_L_Hand', 'J_Bip_R_Hand']:
            bpy.ops.armature.select_all(action='DESELECT')
            hand_bone = bpy.data.armatures['Armature'].edit_bones[hand_bone_name]
            hand_bone.select = True

            # Add a new bone called itemhook at the same position as the hand bone
            new_bone = bpy.data.armatures['Armature'].edit_bones.new(f'{hand_bone_name[:7]}_itemhook')
            offset = mathutils.Vector((0.06, 0.04, -0.02)) if 'L_' in hand_bone_name else mathutils.Vector((-0.06, 0.04, -0.02))
            new_bone.head = hand_bone.head + offset
            new_bone.tail = hand_bone.head + mathutils.Vector((hand_bone.tail.y - hand_bone.head.y, -hand_bone.tail.x + hand_bone.head.x, 0)) + offset if 'L_' in hand_bone_name else hand_bone.head + mathutils.Vector((hand_bone.tail.y - hand_bone.head.y, hand_bone.tail.x - hand_bone.head.x, 0)) + offset
            new_bone.parent = hand_bone
            new_bone.use_connect = False  # This keeps the offset when parenting

        # Switch back to object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        return {'FINISHED'}

class AddHeadEyeShapeKeysButton(bpy.types.Operator):
    bl_idname = "object.add_head_eye_shape_keys"
    bl_label = "Add Head + Eye Shape Keys"
    bl_description = "Adds Shape Keys for both eye positioning and head tilt / rotation. This will let you pose the eyes / head in real time using BAKIN's Blend Shapes. Mix & match in bakin for best results."


    def execute(self, context):
        # Your script for adding head and eye shape keys goes here
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

        # Find the hair mesh
        hair_mesh = None
        for obj in bpy.data.objects:
            if "Hair" in obj.name:
                hair_mesh = obj
                break

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

            # Check if the hair mesh exists
            if "HAIR" in shape_key_name:
                if hair_mesh is not None:
                    hair_mesh.select_set(True)
                    bpy.context.view_layer.objects.active = hair_mesh
                else:
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


class ExportFBXUnifiedButton(bpy.types.Operator):
    bl_idname = "object.export_fbx_unified"
    bl_label = "Export FBX + DEF (Unified)"
    bl_description = "Exports the FBX model, textures, and DEF file for RPG Developer BAKIN. Choose material type for export based on the 'Materials Reduced' setting you've exported the model from VRoid Studio: 8 or 2 materials, or without Materials Reduced."

    material_count: bpy.props.EnumProperty(
        name="Material Type",
        items=[
            ('8', "8 Materials", "Export FBX and DEF with 8 materials"),
            ('2', "2 Materials", "Export FBX and DEF with 2 materials"),
            ('unrestricted', "Unlimited", "Export FBX and DEF with all materials (unrestricted)")
        ],
        default='8'
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "material_count", expand=True)
        layout.label(text="Configure the export settings and click OK to proceed.")

    def execute(self, context):
        try:
            material_count = self.material_count
            self.export_fbx(context, material_count)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export FBX: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}

    def export_fbx(self, context, material_count):
        vrm_model_name = bpy.data.objects['Armature'].data.vrm_addon_extension.vrm1.meta['vrm_name'].replace(' ', '_')
        dirpath = bpy.path.abspath("//" + vrm_model_name + " (Bakin Export)")
        os.makedirs(dirpath, exist_ok=True)

        for image in bpy.data.images:
            if not image.has_data or image.type != 'IMAGE':
                continue
            new_image_name = vrm_model_name + "_" + image.name
            image.save_render(os.path.join(dirpath, new_image_name + ".png"))

        filepath = os.path.join(dirpath, vrm_model_name + ".fbx")
        bpy.ops.export_scene.fbx(
            filepath=filepath,
            use_selection=False,
            global_scale=0.01,
            use_mesh_modifiers=False,
            add_leaf_bones=False,
            use_tspace=True
        )

        with open(os.path.join(dirpath, vrm_model_name + ".def"), 'w') as f:
            meshes_of_interest = {'Face', 'Body', 'Hair'}
            materials_in_use = set()
            mesh_materials = {'Face': set(), 'Body': set(), 'Hair': set()}

            for obj in bpy.data.objects:
                if obj.type == 'MESH' and obj.name in meshes_of_interest:
                    for mat_slot in obj.material_slots:
                        if mat_slot.material:
                            materials_in_use.add(mat_slot.material)
                            mesh_materials[obj.name].add(mat_slot.material)

            for mat in materials_in_use:
                f.write(f'mtl {mat.name}\n')
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

                if material_count == '8':
                    if "EYE" in mat.name or "CLOTH" in mat.name:
                        f.write('RenderingType TranslucentWithDepth\n')
                        f.write('cutOffThreshold 0.005000\n')
                    else:
                        f.write('RenderingType Cutoff\n')
                        f.write('cutOffThreshold 0.600000\n')

                    if mat in mesh_materials['Hair'] or mat in mesh_materials['Body']:
                        f.write(f'LitMap {vrm_model_name}_Image_3.png\n')
                        f.write(f'ShadeMap {vrm_model_name}_Image_10.png\n')
                        f.write(f'NormalMap {vrm_model_name}_Image_5.png\n')
                        f.write(f'EmiMap {vrm_model_name}_Image_4.png\n')
                        f.write(f'outlineWeight {vrm_model_name}_Image_11.png\n')
                    elif mat in mesh_materials['Face']:
                        f.write(f'LitMap {vrm_model_name}_Image_0.png\n')
                        f.write(f'ShadeMap {vrm_model_name}_Image_7.png\n')
                        f.write(f'NormalMap {vrm_model_name}_Image_2.png\n')
                        f.write(f'EmiMap {vrm_model_name}_Image_1.png\n')
                        f.write(f'outlineWeight {vrm_model_name}_Image_9.png\n')

                elif material_count == '2':
                    f.write('RenderingType Cutoff\n')
                    f.write('cutOffThreshold 0.600000\n')

                    if mat in mesh_materials['Hair'] or mat in mesh_materials['Body']:
                        f.write(f'LitMap {vrm_model_name}_Image_3.png\n')
                        f.write(f'ShadeMap {vrm_model_name}_Image_10.png\n')
                        f.write(f'NormalMap {vrm_model_name}_Image_5.png\n')
                        f.write(f'EmiMap {vrm_model_name}_Image_4.png\n')
                        f.write(f'outlineWeight {vrm_model_name}_Image_11.png\n')
                    elif mat in mesh_materials['Face']:
                        f.write(f'LitMap {vrm_model_name}_Image_0.png\n')
                        f.write(f'ShadeMap {vrm_model_name}_Image_7.png\n')
                        f.write(f'NormalMap {vrm_model_name}_Image_2.png\n')
                        f.write(f'EmiMap {vrm_model_name}_Image_1.png\n')
                        f.write(f'outlineWeight {vrm_model_name}_Image_9.png\n')

                elif material_count == 'unrestricted':
                    if "EYE" in mat.name or "CLOTH" in mat.name or "FACE" in mat.name:
                        f.write('RenderingType TranslucentWithDepth\n')
                        f.write('cutOffThreshold 0.005000\n')
                    else:
                        f.write('RenderingType Cutoff\n')
                        f.write('cutOffThreshold 0.600000\n')

                    lit_map = vrm_model_name + "_" + self.get_litmap_name(mat) + ".png"
                    shade_map = vrm_model_name + "_" + self.get_shademap_name(mat) + ".png"
                    normal_map = vrm_model_name + "_" + self.get_normalmap_name(mat) + ".png"
                    emi_map = vrm_model_name + "_" + self.get_emimap_name(mat) + ".png"

                    f.write(f'LitMap {lit_map}\n')
                    f.write(f'ShadeMap {shade_map}\n')
                    f.write(f'NormalMap {normal_map}\n')
                    f.write(f'EmiMap {emi_map}\n')

                f.write('LitColor 1.000000 1.000000 1.000000 1.000000\n')
                f.write('ShadeColor 0.600000 0.600000 0.600000 1.000000\n')
                f.write('normalscl 1.000000\n')
                f.write('toony 0.900000\n')
                f.write('shift 0.000000\n')
                f.write('LitShaderMixTexMult 0.000000\n')
                f.write('lightColorAtt 0.000000\n')
                f.write('Emission 1.000000 1.000000 1.000000\n')
                f.write('EmissionInt 1.000000\n')
                f.write('MCMap MatcapWarp.png\n')
                f.write('matCapScale 1.000000\n')
                f.write('Rim 0.000000 0.000000 0.000000\n')
                f.write('RimInt 1.000000\n')
                f.write('RimLightingMix 0.000000\n')
                f.write('RimFresnelPow 0.000000\n')
                f.write('RimLift 0.000000\n')
                f.write('outlineType World\n')
                f.write('outlineMaxScale 1.000000\n')
                f.write('outlineMixLighting 0.000000\n')
                f.write('UVRotateAnimation 0.000000\n')
                f.write('\n')

    def get_litmap_name(self, mat):
        gltf = mat.vrm_addon_extension.mtoon1
        return gltf.pbr_metallic_roughness.base_color_texture.index.source.name
    
    def get_shademap_name(self, mat):
        gltf = mat.vrm_addon_extension.mtoon1
        mtoon = gltf.extensions.vrmc_materials_mtoon
        return mtoon.shade_multiply_texture.index.source.name
    
    def get_normalmap_name(self, mat):
        gltf = mat.vrm_addon_extension.mtoon1
        return gltf.normal_texture.index.source.name
    
    def get_emimap_name(self, mat):
        gltf = mat.vrm_addon_extension.mtoon1
        return gltf.emissive_texture.index.source.name

class ImportVRMButton(bpy.types.Operator):
    bl_idname = "object.import_vrm"
    bl_label = "Import VRM"
    bl_description = "Import the VRM model into Blender. You need to have the VRM addon for Blender for this to work. This is the same as doing the Import from the File menu. There is no need to enable Texture export, as the export on this addon will handle everything."
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
    

class FusionAndAddBonusesButton(bpy.types.Operator):
    bl_idname = "object.fusion_and_add_bonuses"
    bl_label = "Fusion Meshes and Hair/Head Keys"
    bl_description = "Strongly recommended (8 materials / unlimited materials only). Merges all the meshes together and merges both head and hair shape keys into a new Head shapekey that handles both at once!"

    def execute(self, context):
        # Ensure the objects exist
        if "Hair" not in bpy.data.objects or "Face" not in bpy.data.objects or "Body" not in bpy.data.objects:
            self.report({'ERROR'}, "Required objects are missing (Hair, Face, Body).")
            return {'CANCELLED'}
        
        # Join Hair into Face
        hair = bpy.data.objects["Hair"]
        face = bpy.data.objects["Face"]
        bpy.ops.object.select_all(action='DESELECT')
        face.select_set(True)
        bpy.context.view_layer.objects.active = face
        bpy.ops.object.mode_set(mode='OBJECT')
        hair.select_set(True)
        bpy.ops.object.join()
        
        # Join Face into Body
        face = bpy.data.objects["Face"]  # Now Face includes Hair
        body = bpy.data.objects["Body"]
        bpy.ops.object.select_all(action='DESELECT')
        body.select_set(True)
        bpy.context.view_layer.objects.active = body
        bpy.ops.object.mode_set(mode='OBJECT')
        face.select_set(True)
        bpy.ops.object.join()

        # Get the newly joined object (which is now the Body with Face and Hair)
        merged_obj = bpy.context.active_object

        # Push the current state to the undo stack
        bpy.ops.ed.undo_push(message="Fusion Meshes and Hair/Head Keys")

        # Ensure the shape keys exist
        if merged_obj.data.shape_keys is None:
            # Add a base shape key if none exist
            bpy.ops.object.shape_key_add()
        
        shape_keys = merged_obj.data.shape_keys
        if shape_keys is None:
            self.report({'ERROR'}, "Shape keys not found in the merged object.")
            return {'CANCELLED'}

        # Find pairs of HEAD_ and HAIR_ shape keys
        head_keys = {key.name: key for key in shape_keys.key_blocks if key.name.startswith("HEAD_")}
        hair_keys = {key.name: key for key in shape_keys.key_blocks if key.name.startswith("HAIR_")}
        
        for head_key_name, head_key in head_keys.items():
            corresponding_hair_key_name = head_key_name.replace("HEAD_", "HAIR_")
            if corresponding_hair_key_name in hair_keys:
                itemlook_name = "HEAD_" + head_key_name.replace("HEAD_", "")
                # Create a new shape key for ITEMLOOK
                bpy.ops.object.shape_key_add()
                new_key = shape_keys.key_blocks[-1]
                new_key.name = itemlook_name
                
                # Apply both head and hair changes to the ITEMLOOK key
                for vertex_index in range(len(merged_obj.data.vertices)):
                    base_vertex = shape_keys.key_blocks[0].data[vertex_index].co
                    head_vertex = head_key.data[vertex_index].co
                    hair_vertex = hair_keys[corresponding_hair_key_name].data[vertex_index].co
                    new_key.data[vertex_index].co = base_vertex + (head_vertex - base_vertex) + (hair_vertex - base_vertex)

                # Ensure the new shape key is within the 0.0 to 1.0 range
                new_key.value = min(new_key.value, 1.0)

        # Delete the original HEAD_ and HAIR_ shape keys
        for head_key_name in list(head_keys.keys()):
            bpy.context.object.active_shape_key_index = bpy.context.object.data.shape_keys.key_blocks.keys().index(head_key_name)
            bpy.ops.object.shape_key_remove()

        for hair_key_name in list(hair_keys.keys()):
            bpy.context.object.active_shape_key_index = bpy.context.object.data.shape_keys.key_blocks.keys().index(hair_key_name)
            bpy.ops.object.shape_key_remove()
            
        # Remove ".001" suffix from HEAD_ shape key names
        for key in shape_keys.key_blocks:
            if key.name.startswith("HEAD_") and ".001" in key.name:
                new_name = key.name.replace(".001", "")
                key.name = new_name

        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}
    
    
class ExtractGlassesButton(bpy.types.Operator):
    bl_idname = "object.extract_glasses"
    bl_label = "Extract Glasses BETA"
    bl_description = "Isolates any glasses on your VRM model so that you can load them separately through BAKIN's Subgraphics. At present, you'll need to export this separately through the Blender FBX exporter, select the glasses alone, limit export to selected only, then delete it and export the rest of the model through the addon."

    def execute(self, context):
        obj = bpy.context.object
        
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected.")
            return {'CANCELLED'}

        # Ensure we're in Object mode to perform operations
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get vertex groups containing 'glasses'
        glasses_groups = [vgroup for vgroup in obj.vertex_groups if 'glasses' in vgroup.name.lower()]
        
        if not glasses_groups:
            self.report({'WARNING'}, "No vertex groups containing 'glasses' found.")
            return {'CANCELLED'}

        # Switch to Edit mode to perform mesh operations
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        
        # Iterate over each glasses vertex group and select vertices
        for vgroup in glasses_groups:
            obj.vertex_groups.active = vgroup  # Set the active vertex group
            bpy.ops.object.vertex_group_select()

        # Separate selected vertices into a new object
        bpy.ops.mesh.separate(type='SELECTED')

        # Switch back to Object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Rename the newly created object
        # The newly created object will be the active object after separation
        new_obj = bpy.context.selected_objects[-1]
        new_obj.name = "Glasses"

        return {'FINISHED'}

class ExtractCatEarsButton(bpy.types.Operator):
    bl_idname = "object.extract_cat_ears"
    bl_label = "Extract Cat Ears BETA"
    bl_description = "Isolates any cat ears on your VRM model so that you can load them separately through BAKIN's Subgraphics. At present, you'll need to export this separately through the Blender FBX exporter, select the ears alone, limit export to selected only, then delete it and export the rest of the model through the addon."

    def execute(self, context):
        obj = bpy.context.object
        
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected.")
            return {'CANCELLED'}

        # Ensure we're in Object mode to perform operations
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get vertex groups containing 'cat' (adjust keyword as needed)
        cat_groups = [vgroup for vgroup in obj.vertex_groups if 'cat' in vgroup.name.lower() in vgroup.name.lower() and 'tail' not in vgroup.name.lower()]
        
        if not cat_groups:
            self.report({'WARNING'}, "No vertex groups containing 'cat' found.")
            return {'CANCELLED'}

        # Switch to Edit mode to perform mesh operations
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        
        # Iterate over each cat vertex group and select vertices
        for vgroup in cat_groups:
            obj.vertex_groups.active = vgroup  # Set the active vertex group
            bpy.ops.object.vertex_group_select()

        # Separate selected vertices into a new object
        bpy.ops.mesh.separate(type='SELECTED')

        # Switch back to Object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Rename the newly created object
        # The newly created object will be the active object after separation
        new_obj = bpy.context.selected_objects[-1]
        new_obj.name = "Cat Ears"

        return {'FINISHED'}

class ExtractRabbitEarsButton(bpy.types.Operator):
    bl_idname = "object.extract_rabbit_ears"
    bl_label = "Extract Rabbit Ears BETA"
    bl_description = "Isolates any rabbit ears on your VRM model so that you can load them separately through BAKIN's Subgraphics. At present, you'll need to export this separately through the Blender FBX exporter, select the ears alone, limit export to selected only, then delete it and export the rest of the model through the addon."

    def execute(self, context):
        obj = bpy.context.object
        
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected.")
            return {'CANCELLED'}

        # Ensure we're in Object mode to perform operations
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get vertex groups containing 'rabbit' and not containing 'tail'
        rabbit_groups = [vgroup for vgroup in obj.vertex_groups if 'rabbit' in vgroup.name.lower() and 'tail' not in vgroup.name.lower()]
        
        if not rabbit_groups:
            self.report({'WARNING'}, "No suitable vertex groups containing 'rabbit' found.")
            return {'CANCELLED'}

        # Switch to Edit mode to perform mesh operations
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        
        # Iterate over each rabbit vertex group and select vertices
        for vgroup in rabbit_groups:
            obj.vertex_groups.active = vgroup  # Set the active vertex group
            bpy.ops.object.vertex_group_select()

        # Separate selected vertices into a new object
        bpy.ops.mesh.separate(type='SELECTED')

        # Switch back to Object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Rename the newly created object
        # The newly created object will be the active object after separation
        new_obj = bpy.context.selected_objects[-1]
        new_obj.name = "Bunny Ears"

        return {'FINISHED'}

class RunScriptButtonPanel(bpy.types.Panel):
    bl_label = "VRoid for Bakin"
    bl_idname = "OBJECT_PT_run_script"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VRoid for Bakin"

    def draw(self, context):
        layout = self.layout

        # Check if the current .blend file is saved
        blend_file_saved = bpy.data.filepath != ""

        # Import section
        layout.label(text="Import", icon='IMPORT')
        layout.operator("object.import_vrm")
        
        # Bakin Enhancements section
        layout.label(text="Bakin Enhancements", icon='OUTLINER_OB_ARMATURE')
        layout.operator("object.add_item_hooks", icon='EVENT_ONEKEY')
        layout.operator("object.add_head_eye_shape_keys", icon='EVENT_TWOKEY')
        layout.operator("object.fusion_and_add_bonuses", icon='EVENT_THREEKEY')
        
        
        layout.label(text="Optionals BETA", icon='MATCLOTH')
        layout.operator("object.extract_glasses", icon='LAYER_USED')
        layout.operator("object.extract_rabbit_ears", icon='LAYER_USED')
        layout.operator("object.extract_cat_ears", icon='LAYER_USED')
        
        # Export section
        layout.label(text="Export", icon='EXPORT')

        # Display warning if blend file is not saved
        if not blend_file_saved:
            layout.label(text="Warning: Blend file not saved!", icon='ERROR')

        # Export buttons
        export_button = layout.row()
        export_button.enabled = blend_file_saved
        export_button.operator("object.export_fbx_unified", text="Export FBX + DEF", icon='EXPORT')


        # Wrapped export description labels
        export_descriptions = [
            "Hover over the buttons to read a detailed description on the functionality of each button."
        ]
        for export_desc in export_descriptions:
            for line in textwrap.wrap(export_desc, width=40):
                layout.label(text=line, icon='BLANK1')

def register():
    bpy.utils.register_class(ImportVRMButton)
    bpy.utils.register_class(AddItemHooksButton)
    bpy.utils.register_class(AddHeadEyeShapeKeysButton)
    bpy.utils.register_class(FusionAndAddBonusesButton)
    bpy.utils.register_class(ExtractGlassesButton)
    bpy.utils.register_class(ExtractRabbitEarsButton)
    bpy.utils.register_class(ExtractCatEarsButton)
    bpy.utils.register_class(ExportFBXUnifiedButton)
    bpy.utils.register_class(RunScriptButtonPanel)

def unregister():
    bpy.utils.unregister_class(ImportVRMButton)
    bpy.utils.unregister_class(AddItemHooksButton)
    bpy.utils.unregister_class(AddHeadEyeShapeKeysButton)
    bpy.utils.unregister_class(FusionAndAddBonusesButton)
    bpy.utils.unregister_class(ExportFBXUnifiedButton)
    bpy.utils.unregister_class(ExtractGlassesButton)
    bpy.utils.unregister_class(ExtractRabbitEarsButton)
    bpy.utils.unregister_class(ExtractCatEarsButton)
    bpy.utils.unregister_class(RunScriptButtonPanel)

if __name__ == "__main__":
    register()
