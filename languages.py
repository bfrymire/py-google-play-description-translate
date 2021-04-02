import json


class Language:
	
	def __init__(self, name, code):
		self.name = name
		self.names = []
		self.code = code.strip()
		self.create_names()
		# self.localization = local
		# self.localization_code = local_code

	def __repr__(self):
		return f'<Language: {self.name} - {self.code}>'

	def create_names(self):
		self.names = [n.lower() for n in self.name.split(' ')]
		if self.name.lower() not in self.names:
			self.names.append(self.name.lower())

def filter_languages(name, language):
	if name in language.names:
		return True
	return False

def get_filtered_language(name, languages):
	return filter(filter_languages, name)

def get_google_translate_languages():
	with open('./data/google_translate_languages.json') as f:
		data = json.load(f)
	return [Language(l['language'], l['code']) for l in data['languages']]
	# l = []
	# for language in data.languages:
	# 	l.append(Language(language.language, language.code))
	# return l