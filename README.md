# Root Builder
## Description
Have you ever wanted to have control over your game's root folder and switch files like ENBs, Script Extenders and other DLLs on the fly? Well, You have come to the Right place! With Root Builder, you can control the contents of the root game folder through Mod Organizer's Interface!
## Features
* Prioritised Loading through Mod Priority.
* Two Different Systems for loading Root-Level Mods.
* Support for Modded DLLs & Script Extenders.
  * Needs Symlink Enabled through plugin settings.
* Support for Overwrite Folder.
## How to Install
Just Copy and Paste into (Mod Organizer 2)/Plugins
## How to Use
  1. Create a new (empty) or use an existing mod.
  2. Navigate to the new mod's folder.
  3. Create a folder named "Root"(without quote marks) inside the mod's folder.
  4. place all desired content inside that folder
      * Please Note that no Data folder is allowed inside the Root folder. Any Root folder containing a Data folder will be ignored!
  5. Enjoy!
###### Please note for DLLs and Script Extenders to work on new games, you will need the symlink option in the plugin's settings set to TRUE. This does not concern stuff like ENB Presets which are not affected by having this option set to true or false.
###### Please note that symlink is not as reliable as the primary loading system and it is recommended to backup the game root folder, in exception of the Data folder, as a precautionary measure in case the internal backup system fails.
