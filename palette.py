import json

filename = "palettes.json"


class CustomEncoder(json.JSONEncoder): # Chatgpt code to make the json files easier to read
	def encode(self, obj):
		json_str = super().encode(obj)
		# Post-process to reduce list indentation
		json_str = json_str.replace('[\n            ', '[')
		json_str = json_str.replace('\n            ', ' ')
		json_str = json_str.replace('\n        ]', ']')
		return json_str


def load():
	with open(filename, "r") as file:
		palettes = json.load(file)
	
	# Nested for loop to get each color in each palette and convert the color to a tuple
	return {palette: {color: tuple(palettes[palette][color]) for color in palettes[palette]} for palette in palettes}


def load_palette(name: str):
	return load()[name]


def save_palette(name: str, colors: dict[str, tuple]):
	# Converts tuples to lists
	colors = {color: list(colors[color]) for color in colors}
	saved = load()
	saved[name] = colors
	json_data = json.dumps(saved, cls = CustomEncoder, indent = 4)
	with open(filename, "w") as file:
		file.write(json_data)
