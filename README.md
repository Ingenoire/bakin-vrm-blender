# bakin-vrm-blender
![alt text](https://i.imgur.com/T6TnJll.png)

**A Blender Addon that allows you to quickly rig and export VRM models for use with RPG Developer Bakin with item hooks, new shape keys for head tilting and eye looking, automatic material imports, and other fixes.
Works for both VRM 0.0 models and VRM 1.0 models.**

>⚠️ You'll need the VRM Addon for Blender. https://vrm-addon-for-blender.info/en/

- *If you wish to import general models for BAKIN using PBR, use this Blender add-on instead: https://github.com/Ingenoire/bakin-blender-exporter*

### V4.0: Multiple Irises through Blend Shapes added!
A pretty major feature, you can now load in a new texture that holds up to 4 different irises, and you'll be able to swap the iris textures in Bakin on the fly! This is great for creating more expressive characters through the use of things like heart-shaped eyes, soulless eyes, etc...
>⚠️ It might not work on some models.

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

### Tip
![alt text](https://i.imgur.com/XAvD2cv.png)
- To improve details on the eyes and other parts even more, turn off Vertex Compression for the model in the Model explorer of Bakin (not in the 3D Stamps explorer)

### Credits
The addon was made through Microsoft Copilot and ChatGPT (using the Blender scripting GPT), after a lot of trial and error and a few tweaks.
