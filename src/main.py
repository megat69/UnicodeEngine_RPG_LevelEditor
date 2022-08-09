from UnicodeEngine_RPG import UnicodeEngine_RPG, Char, Player, getch, InventoryItem
from typing import Union
import colorama; colorama.init()
from colorama import Fore, Back, Style
import os
import json

from utilities import input_tuple
from tilemap_loader import load_tilemap


class LevelEditor:
	def __init__(self, tilemap_size : tuple[int, int]):
		default_char = Char("-")
		default_char.COLOR_NAME = "BLACK"
		self.tilemap = [[default_char for _ in range(tilemap_size[0])] for _ in range(tilemap_size[1])]
		self.app = UnicodeEngine_RPG(
			tilemap=self.tilemap,
			player=Player([0, 0], "▓▓▓▓"),
			noclip=True
		)
		self.app.inventory = {
			"position": InventoryItem("Position", self.app.player.position, lambda e: e),
			"replace_key": InventoryItem("Replace a tile", "'r'", lambda e: 'r'),
			"save_key": InventoryItem("Save a configuration", "'e'", lambda e: 'e'),
			"load_key": InventoryItem("Load an existing configuration", "'l'", lambda e: 'l')
		}
		self.existing_chars = {
			"--default--": default_char
		}
		self.run()

	def update(self, dt: float):
		"""
		Runs every frame.
		"""
		# New char
		if self.app.keystroke == "r":
			self.replace_char()
		# Save the tilemap
		elif self.app.keystroke == "e":
			self.save_tilemap()
		# Load an existing tilemap
		elif self.app.keystroke == "l":
			self.load_tilemap()


	def replace_char(self):
		"""
		Replaces a new character on the tilemap from an existing one.
		"""
		# Prints the list of existing characters
		print(Style.BRIGHT + "EXISTING CHARACTERS" + Style.RESET_ALL)
		print("\n".join(self.existing_chars.keys()))
		print(f"{Fore.GREEN}--new--\n{Fore.YELLOW}--modify--\n{Fore.RED}--cancel--{Style.RESET_ALL}")
		# Requests the name of the character to insert
		char_name = input("Input the character name from the list of already created characters : ")

		# If the user wants to create a new character, we call the corresponding function
		if char_name == "--new--":
			char_name = self.create_char()
		elif char_name == "--modify--":
			char_name = self.modify_char()
			return None
		elif char_name == "--cancel--":
			return None

		# We replace the character the user is on with the corresponding character
		try:
			self.tilemap[self.app.player.position[0]][self.app.player.position[1]] = self.existing_chars[char_name]
		except KeyError:
			print("This character name doesn't exist.")
			self.replace_char()


	def create_char(self):
		"""
		Creates a new character.
		"""
		# Getting the information for the character
		char_name = input("How do you want to name this character ? ")
		if char_name in ("--new--", "--cancel--", "--modify--"):
			print("This name is a reserved name !")
			return self.create_char()
		print("Please paste the character you want to set : ")
		char_value = input()
		char_position = -1
		while char_position < 0 or char_position > 3:
			try:
				char_position = int(input("What is the position of the character ? (Leave blank for 0) "))
			except ValueError:
				char_position = 0
		char_collider = input("Do you collide with this character ? (y/n) ").lower() == "y"
		char_color = input("Input a color name from the Colorama 'Back' class (Black by default) : ")
		char_color_str = char_color.upper() if char_color != "" else "BLACK"
		if char_color == "":
			char_color = Back.BLACK
		else:
			char_color = getattr(Back, char_color.upper())

		# TODO : Char action and walk action !

		# Saves the character in the database
		self.existing_chars[char_name] = Char(char_value, char_position, char_color, char_collider)
		self.existing_chars[char_name].COLOR_NAME = char_color_str  # Remembering the color NAME for the save
		# Returns the name of the character to end the procedure
		return char_name


	def modify_char(self):
		"""
		Creates a new character.
		"""
		# Getting the information for the character
		char_name = input("Which character do you want to modify ? ")
		if char_name in ("--new--", "--cancel--", "--modify--"):
			print("This name is a reserved name !")
			return self.modify_char()
		print("Please paste the character you want to set it to (or leave blank to keep the same) : ")
		char_value = input()
		if char_value == "":
			char_value = self.existing_chars[char_name].name
		char_position = -1
		while char_position < 0 or char_position > 3:
			try:
				char_position = input("What is the position of the character ? (Leave blank for the same) ")
				if char_position == "":
					char_position = self.existing_chars[char_name].position
				else:
					char_position = int(char_position)
			except ValueError:
				char_position = 0
		char_collider = input("Do you collide with this character ? (y/n) ").lower() == "y"
		char_color = input("Input a color name from the Colorama 'Back' class (Leave blank to keep the same) : ")
		char_color_str = char_color.upper() if char_color != "" else self.existing_chars[char_name].COLOR_NAME
		char_color = getattr(Back, char_color_str.upper())

		# Saves the character in the database
		self.existing_chars[char_name].name = char_value
		self.existing_chars[char_name].position = char_position
		self.existing_chars[char_name].collision = char_collider
		self.existing_chars[char_name].color = char_color
		self.existing_chars[char_name].COLOR_NAME = char_color_str  # Remembering the color NAME for the save
		# Returns the name of the character to end the procedure
		return char_name


	def save_tilemap(self):
		"""
		Saves the tilemap into a file.
		"""
		print(f"{Style.BRIGHT}-- FILE SAVING --{Style.RESET_ALL}")
		path = input("Please input the absolute path to the FILE you want to save the tilemap into.\n"
		             "This will overwrite any existing file. You can also type 'cancel' to cancel.\n")
		# If the user chooses to cancel, we stop the function here
		if path == "cancel":
			return None

		# We check if the folder exists
		if os.path.exists(path) or os.path.exists("/".join(path.split("/")[:-1])):
			# If the user didn't specify a filename, then we add a default one'
			if os.path.isdir(path):
				path = os.path.join(path, "tilemap.json")

			# We define a function to return the name of the character
			def tilemap_find_correct_char_name(char: Char):
				for name, element in self.existing_chars.items():
					if char is element:
						return name

			# We create the dictionnary that will be used for the file
			final_dict = {
				"chars": {
					name: {
						"name": contents.name,
						"position": contents.position,
						"color": contents.COLOR_NAME,
						"collision": contents.collision
					} for name, contents in self.existing_chars.items()
				},
				"layout": [
					[
						tilemap_find_correct_char_name(column) for column in row
					] for row in self.tilemap
				]
			}

			# Saving it to a file
			with open(path, 'w') as f:
				json.dump(final_dict, f, indent=4)

			# End message
			print(f"{Fore.GREEN}The tilemap was correctly saved !{Fore.RESET}")
			getch()

		else:
			print(f"Something went wrong. '{path}' is not a valid path.")
			getch()


	def load_tilemap(self):
		"""
		Loads an existing tilemap file given by the user
		"""
		print(f"{Style.BRIGHT}-- TILEMAP LOADING --{Style.RESET_ALL}")
		path = input("Please input the absolute path to the FILE you want to open the tilemap form.\n"
		             "This will overwrite the currently loaded tilemap. You can also type 'cancel' to cancel.\n")
		# If the user chooses to cancel, we stop the function here
		if path == "cancel":
			return None

		# Checking if the file exists
		if os.path.exists(path):
			# Trying to open the file
			try:
				with open(path, "r") as f:
					json_file_contents = json.load(f)
			except Exception as e:
				print(f"An error occurred while parsing :\n{e}")
				getch()
				return None

			# Fetching the return from the tilemap loader
			chars_used, tilemap = load_tilemap(json_file_contents)

			# Saving the tilemap contents and the chars used
			self.existing_chars = chars_used
			self.tilemap = tilemap
			self.app.tilemap = tilemap

			# End message
			print("Tilemap imported successfully !")
			getch()

		# Otherwise throwing an error
		else:
			print(f"Something went wrong. '{path}' does not exist.")
			getch()


	def run(self):
		self.app.run(self.update)


if __name__ == "__main__":
	# Requesting a tilemap size from the user
	tilemap_size = input_tuple(prompt="Input a tilemap size :")
	level_editor = LevelEditor(tilemap_size)
	level_editor.run()
