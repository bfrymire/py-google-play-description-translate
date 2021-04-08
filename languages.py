import json


class Language:
	
	def __init__(self, name, code):
		self.name = name
		self.names = []
		self.code = code.strip()
		self.create_names()

	def __repr__(self):
		return f'<Language: {self.name} - {self.code}>'

	def create_names(self):
		self.names = [n.lower() for n in self.name.split(' ')]
		if self.name.lower() not in self.names:
			self.names.append(self.name.lower())

def filter_languages(names, languages):
	filtered = []
	for name in names:
		for i, l in enumerate(languages, start=1):
			if name.lower() in l.names:
				filtered.append(l)
				break
			if i == len(languages):
				print(f'Could not find an associated language for \"{name}\".')
	return filtered

def open_json_language_file(path):
	with open(path) as f:
		return json.load(f)
	
def create_languages_from_json_data(path):
	data = open_json_language_file(path)
	return [Language(l['language'], l['code']) for l in data['languages']]

def get_google_translate_languages():
	return create_languages_from_json_data('./data/google_translate_languages.json')

def get_google_play_languages():
	return create_languages_from_json_data('./data/google_play_languages.json')
