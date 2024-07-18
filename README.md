# bakin-vrm-blender

![alt text](https://i.imgur.com/pl18RUw.png)
A Blender Addon that allows you to quickly rig and export VRM models for use with RPG Developer Bakin with item hooks, new shape keys for head tilting and eye looking, automatic material imports, and other fixes.
Works for both VRM 0.0 models and VRM 1.0 models.

>⚠️ You'll need the VRM Addon for Blender. https://vrm-addon-for-blender.info/en/
>
>⚠️ Your VRM model must be exported with either 2 materials or 8 materials (changed through VRoid Studio's "Reduce Materials" export settings).
>
>⚠️ You'll need to save the current scene into a blend file before the export will work. Export generates a new folder in the same location as the blend file.
>

### V2B Update
- Adds an Unrestricted Material Export mode.
 - At the cost of having a ton of materials on a single model, and Bakin having LONG loading lag anytime an editor window loading the model occurs, it offers uncompressed textures on your models in game.
 - Great for higher detailed clothing and body skin textures, and could be great to use for cutscenes.
 - To use this, simply re-export your VRM from VRoid Studio, but this time, don't Reduce Materials (keep default).

### V2 Update
![alt text](https://i.imgur.com/GzvIBj7.png)
- Now supports an 8-Material mode: use the 8 Material Export button instead of the 2 Material Export button when exporting.
  - Your VRM model must be re-exported from VRoid Studio with the Reduce Materials settings set to 8.
  - The main advantage of this mode is that smaller details surrounding the eyes (such as eye shadows, makeup, etc) get properly rendered using the TranslucentWithDepth mode on Bakin's toon shader.
    - You can alter a 2 Material VRM to use TranslucentWithDepth and set the cutoff threshold to 0.005 manually in Bakin: but this will make the model unable to cast shadows among other issues, so the addon doesn't do that (and 2 Materials mean the entire face is fused with the eyes, so they can't be seperated).
- Add-on moved to the right side panel (alongside 90% of other addons) instead of under the 3D tools.

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
