# bakin-vrm-blender
![alt text](https://i.imgur.com/T6TnJll.png)
A Blender Addon that allows you to quickly rig and export VRM models for use with RPG Developer Bakin with item hooks, new shape keys for head tilting and eye looking, automatic material imports, and other fixes.
Works for both VRM 0.0 models and VRM 1.0 models.

>⚠️ You'll need the VRM Addon for Blender. https://vrm-addon-for-blender.info/en/
>

### V3 Update
- Added the "Fusion Mesh and Hair/Head Shape Keys" function.
  - Only works for 8 and Unlimited materials due to most 2 material meshes being split into only 2 meshes.
  - This merges all three meshes (Hair, Face and Body) into a single mesh.
  - This fusions the HEAD and HAIR shape keys into a new, singular set of HEAD shape keys.
    - **This means HEAD will now affect both the hair and the hair (but only with a fused mesh due to modeling shenanigans).**
- Adjusted the UI to look better and less cluttered.
  - Detailed descriptions have been added, hover your mouse over a button to see them.
- Added a beta feature: extract rabbit ears, cat ears, and glasses, for use with Bakin's Subgraphics (letting you toggle it on/off in engine, etc).
  - Currently, you'll need to export the model on it's own not through the addon, put it in a folder, then delete the isolated mesh from the blender scene, export the model without the ears or glasses through the addon, and then move the glasses/ears model into the exported folder where the body and textures are, and then duplicate the DEF file and rename it to the filename of the ears/glasses.
- Seperated Item Hook and the facial shape key bonuses as seperate functions.

### Features
- Simple and straightforward workflow: no need to touch anything Blender related if you don't want to!
- Automatic item hook bones, so that your character can hold items in engine!
- Creates shape keys for head (tilt head) and eyes (look at), for better emotions in engine!
- Generates a .DEF file through the built-in exporter to automatically import textures into the engine.
- Adjusts the texture names to be easily sorted through in engine.
- Removes VRM 1.0 icosphere.
- Creates a new folder in the same directory as your blender project containing all the exported files.
- Feel free to edit the source code to make any necessary tweaks.

### Installation
- Download the latest release.
- Open Blender, and under "Edit" -> "Preferences", select "Add-ons". Then go to "Install...", find your downloaded zip file. Make sure to tick the addon box for it to activate (Blender 4.2 automatically activates it though).
- The addon is set to the right side panel. Press the N key to open the side panel and find the VRoid for Bakin tab.

### Tip
![alt text](https://i.imgur.com/XAvD2cv.png)
- To improve details on the eyes and other parts even more, turn off Vertex Compression for the model in the Model explorer of Bakin (not in the 3D Stamps explorer)

### Credits
The addon was made through Microsoft Copilot and ChatGPT (using the Blender scripting GPT), after a lot of trial and error and a few tweaks.
