# UnicodeEngine_RPG_LevelEditor
A level editor for my [UnicodeEngine_RPG](https://github.com/megat69/UnicodeEngine_RPG)

## Download
Simply clone this repo or download it.

# Usage
Go into the `src` folder and run the `main.py` script.

You will be prompted to input a tilemap size. It will be used to automatically generate a temporary tilemap for the level editor.

Once you have entered this information, the window will prompt you to resize your console to a specific height.

One this is done, you can press Enter or any other key to move into the editor.

You will see your position on the screen with this character : `▓`<br/>
It represents the tile currently selected.

You can also see your position at the right of the screen.

To move, just use the WASD keys.

## Replacing tiles
To replacce the tile you are currently on, press the `r` key.

It will open display a list of all the characters you've precedently created, along with three other options : `--new--`, `--modify--`, and `--cancel--`.

From this list, you can type the name of the character you want to turn the selected tile into, or one of the three other options detailed below.

### --new--
This will allow you to create a brand-new character.

Typing this will open the character creation process, which will consist of multiple prompts to setup the character.

At the end of this process, the currently selected tile will be replaced by this new character.

### --modify--
This options works pretty much like the --new-- option, except that it allows you to modify the settings for an existing character.

At the end of this process, all the characters using the modified character will be updated. The selected character will NOT be replaced by this updated character, unless it is already using the updated character.

### --cancel--
This options speaks for itself, it will cancel the operation, just like a regular `cancel` button.

## Saving a tilemap
Using the `e` key, you can save a tilemap into a file.

When using that key, a prompt will open, asking you to input the ABSOLUTE path to the file that the tilemap will be saved into.

**WARNING : Doing so will overwrite any existing file without warning !**

You can also type `cancel` to... Well, cancel the save.

If you input a folder path, the name `tilemap.json` will be given to the file.

## Loading a tilemap
Using the `l` key, you can load a tilemap from a file.

**WARNING : Loading a tilemap will overwrite the tilemap you are currently using without warning !**

You can also cancel this action by typing `cancel`.

# Examples
You can find this example in the [example folder](https://github.com/megat69/UnicodeEngine_RPG_LevelEditor/tree/main/example).

This example also shows how to use the `load_tilemap` function from the `tilemap_loader` of the level editor.


