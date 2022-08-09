"""
Utility functions.
"""
from UnicodeEngine_RPG.getch import getch


def input_tuple(nb_elements: int = 2, prompt: str = None):
	"""
	Asks the user to input a tuple of nb_elements integers.
	:param nb_elements: The amount of elements the tuple should contain.
	:param prompt: The string to be displayed first.
	:return: Returns said tuple.
	"""
	# Printing the prompt if given
	if prompt is not None: print(prompt)

	# Initializing a list of elements, for now empty strings
	lst = ["" for i in range(nb_elements)]

	# Displaying the current state of the tuple
	print('\n'*20, "(", ", ".join(lst), ")", sep="")

	# Fetching every element in the list
	for i in range(nb_elements):
		# Initializing a character
		character = None
		# While the character is not a loop-breaker
		while character not in ("", " ", ",", "\n", "\r"):
			# We fetch the character and add it to the string at the corresponding index in the list
			character = getch()
			lst[i] += character

			# We display the current state of the tuple
			print("\n"*20)
			print("(", ", ".join(lst), ")", sep="")
		# When the loop ends
		else:
			# Converting to integer
			lst[i] = lst[i][:-1]

	# We return the list as a tuple
	try:
		return tuple(int(e) for e in lst)
	except ValueError:
		print("Something went wrong. Please try again.")
		return input_tuple(nb_elements, prompt)
