import unittest
import os
import json

from languages import Language, filter_languages, open_json_language_file, create_languages_from_json_data, get_google_translate_languages, get_google_play_languages


class LanguageMatcher:
	expected: Language

	def __init__(self, expected):
		self.expected = expected

	def __repr__(self):
		return f'<Language: {self.expected.name} - {self.expected.code}>'

	def __eq__(self, other):
		return self.expected.name == other.name and \
			   self.expected.code == other.code and \
			   self.expected.names == other.names

class LanguageMatcherCase(unittest.TestCase):

	def test_language_matcher(self):
		language = 'Test Language'
		code = 'tl'
		self.assertEqual(LanguageMatcher(Language(language, code)), Language(language, code), "LanguageMatcher and Language do not hold the same values")

class LanguageCase(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls._l = Language('  Test Language  ', '  tl  ')

	def test_language_name(self):
		self.assertEqual('Test Language', self._l.name, "")

	def test_language_code(self):
		self.assertEqual('tl', self._l.code)

	def test_language_names(self):
		self.assertEqual(['test', 'language', 'test language'], self._l.names)

class LanguageJsonHelperCase(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls._test_language = Language('Test Language', 'tl')
		cls._fname = 'test_json_helper_languages.json'
		cls._path = f'./{cls._fname}'
		cls._content = '''
							{
								"languages": [{
									"language": "Test Language",
									"code": "tl"
								}]
							}
					   '''
		with open(cls._path, 'w') as f:
			f.write(cls._content)

	@classmethod
	def tearDownClass(cls):
		os.remove(cls._path)

	def test_open_language_json(self):
		data = open_json_language_file(self._path)
		self.assertEqual(json.loads(self._content), data)

	def test_create_languages_from_json(self):
		data = create_languages_from_json_data(self._path)[0]
		self.assertEqual(LanguageMatcher(self._test_language), data)

	def test_filter_languages(self):
		data = create_languages_from_json_data(self._path)
		filtered = filter_languages(['Test'], data)
		self.assertEqual([LanguageMatcher(self._test_language)], filtered)

	def test_google_play_len(self):
		languages = get_google_play_languages()
		self.assertEqual(49, len(languages))

	def test_google_translate_len(self):
		languages = get_google_translate_languages()
		self.assertEqual(108, len(languages))