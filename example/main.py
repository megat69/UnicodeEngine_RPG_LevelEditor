from UnicodeEngine_RPG import UnicodeEngine_RPG, Player, display_text
from tilemap_loader import load_tilemap
from functools import partial

if __name__ == "__main__":
	chars_used, tilemap = load_tilemap("tilemap.json")
	chars_used["o"].action = partial(display_text, "Greetings from the level editor !")
	chars_used["--default--"].name = "*"
	app = UnicodeEngine_RPG(
		tilemap=tilemap,
		player=Player([0, 0]),
		playable_area=(8, 8)
	)
	app.run()
