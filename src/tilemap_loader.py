"""
A tilemap loader for the level editor.
"""
import json
import os
from typing import Union
from UnicodeEngine_RPG import Char
from colorama import init, Back; init()


def load_tilemap(path: Union[str, dict]) -> tuple[dict, list[list[Char]]]:
	"""
	Loads the given tilemap and returns a dictionnary containing all the characters used and a
	tilemap ready to be used.
	:param path: The path to the tilemap file to load, or a valid dict already imported from a tilemap.
	"""
	# If the path is an actual path, we load from the file
	if isinstance(path, str):
		if os.path.exists(path):
			try:
				with open(path, "r") as f:
					path = json.load(f)
			except Exception as e:
				raise Exception(f"An error occurred while parsing :\n{e}")
		else:
			raise FileNotFoundError(f"File at {path} doesn't seem to exist.")

	# After that, we treat path as a dictionary anyway
	chars_used = path["chars"]
	tilemap = path["layout"]

	# We load the chars as Char instances
	for name, char in chars_used.items():
		COLOR_NAME = char["color"]
		char["color"] = getattr(Back, char["color"])
		chars_used[name] = Char(**char)
		chars_used[name].COLOR_NAME = COLOR_NAME

	# We turn the tilemap into instances of the chars_used dictionary
	for row_id in range(len(tilemap)):
		for column_id in range(len(tilemap[row_id])):
			tilemap[row_id][column_id] = chars_used[tilemap[row_id][column_id]]

	# We can finally return both the chars_used and the tilemap
	return chars_used, tilemap




