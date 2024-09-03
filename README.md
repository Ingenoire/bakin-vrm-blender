# bakin-vrm-blender
![alt text](https://i.imgur.com/T6TnJll.png)

**A Blender Addon that allows you to quickly rig and export VRM models for use with RPG Developer Bakin with item hooks, new shape keys for head tilting and eye looking, automatic material imports, and other fixes.
Works for both VRM 0.0 models and VRM 1.0 models.**

>⚠️ You'll need the VRM Addon for Blender. https://vrm-addon-for-blender.info/en/
>
>⚠️ We strongly recommend you use VRoid VRM 1.0 models exported with materials reduced to 8, as that's the main model type I'm working with. Some features aren't supported for models with materials reduced set to 2.

- *If you wish to import general models for BAKIN using PBR, use this Blender add-on instead: https://github.com/Ingenoire/bakin-blender-exporter*
- *If you wish to animate the VRM models with baked-in hair/bust/outfit physics for your Bakin game, check out this add-on I made: https://github.com/Ingenoire/VRM-Spacing-Animation-Baking*

### V4.0: Multiple Irises through Blend Shapes added!

| Original Iris | Alternate Iris (#2 in this case) |
| --- | --- |
| ![img](https://i.imgur.com/fBlglrl.png) | ![img](https://i.imgur.com/pMgZzgm.png) |

A pretty major (optional) feature, you can now load in a new texture that holds up to 4 different irises, and you'll be able to swap the iris textures in Bakin on the fly! This is great for creating more expressive characters through the use of things like heart-shaped eyes, soulless eyes, etc...
Characters need expressions, and it'd be a shame if your character couldn't show more emotion!

- You'll need to supply a 4096x4096 image texture layed out like the template image here: https://github.com/Ingenoire/bakin-vrm-blender/blob/main/iris_template.png. Best to use textures straight out of VRoid Studio by exporting them from there first (edit iris textures), upscale them if needed, and place both their iris and highlights in the same way. For best results, in your image editor, display a 1024x1024 grid to make things easier.
- If you want to do this step, you'll need to do it before merging the meshes.
- Your model needs to have been exported with a 4096x4096 texture resolution to use (default settings when reducing materials in VRoid Studio). No testing was done with different texture sizes.
- In Bakin, you'll need to enable the ALTERNATE_IRIS 1 to 4 shape key, ideally without resetting other shape keys, for it to show up.

>⚠️ Bug #1: The highlights of the alternate irises are a bit off, so feel free to place the highlight over the iris in your alternate irises.
>
>⚠️ Bug #2: if you manipulate the shape keys of the model before pressing the "Add Alternate Irises" button, it will stack all the irises in the original iris (that's bad). If this happens, make a new blender scene and re-import the VRM, and just press the buttons in order, without fiddling with the shape keys in Blender.

### Features
- Simple and straightforward workflow: no need to touch anything Blender related if you don't want to!
- Automatic item hook bones, so that your character can hold items in engine!
- Creates shape keys for head (tilt head) and eyes (look at), for better emotions in engine!
- Higher quality 8 and unlimited material modes supported (compared to 2 from Bakin tutorials) for more accurate looking models!
- Add optional alternative iris textures (up to 4) to display different emotions, that can be swapped in-engine through the use of Blend Shapes!
- Generates a .DEF file through the built-in exporter to *automatically import textures into the engine.*
- Outlines are (kinda) supported (but honestly it's best to just select all the materials in-engine, and then batch change their outline properties for now)!
- Adjusts the texture names to be easily sorted through in engine.
- Removes VRM 1.0 icosphere.
- Creates a new folder in the same directory as your blender project containing all the exported files.
- Feel free to edit the source code to make any necessary tweaks.

### Installation
- Download the latest release.
- Open Blender, and under "Edit" -> "Preferences", select "Add-ons". Then go to "Install...", find your downloaded zip file. Make sure to tick the addon box for it to activate (Blender 4.2 automatically activates it though).
- The addon is set to the right side panel. Press the N key to open the side panel and find the VRoid for Bakin tab.

## Usage
Assuming you're using a VRoid VRM 1.0 Model with Materials Reduced set to 8, and the texture resolution was left at 4096x4096:
- Open the Bakin VRM panel, and press Import VRM Model.
- Click the four buttons from top to bottom in successive order.
- Save your current blender scene (it's good for animating your model later on too)!
- Press Export FBX + DEF, and select 8 materials, then export.
  - If you want more accurate shadows (AKA: no invisible torso) casted or outlines to work, enable the tick box before exporting.
- Open Bakin, and import the model. The model is located in a new folder created where you saved the blend file.

### Tip
![alt text](https://i.imgur.com/XAvD2cv.png)
- To improve details on the eyes and other parts even more, turn off Vertex Compression for the model in the Model explorer of Bakin (not in the 3D Stamps explorer)

### Credits
The addon was made through Microsoft Copilot and ChatGPT (using the Blender scripting GPT), after a lot of trial and error and a few tweaks.
