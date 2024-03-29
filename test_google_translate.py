import unittest

from google_translate import replace_bullet, get_bullet_character, create_code, first


class GoogleTranslateCase(unittest.TestCase):

	def test_create_code_len(self):
		s = create_code(code_len=7)
		self.assertEqual(9, len(s), 'code created is not 9 characters in length')

	def test_create_code_is_header_code(self):
		s = create_code(is_header_code=True)
		self.assertEqual('.', s[-1], 'code created does not end in a period (.)')

	def test_create_code_wrapper_start(self):
		s = create_code()
		self.assertEqual(s[0], '{', 'code created does not start with curley bracket')

	def test_create_code_wrapper_end(self):
		s = create_code()
		self.assertEqual('}', s[-1], 'code created does not end with curley bracket')

	def test_create_code_is_numeric(self):
		s = create_code()
		self.assertTrue(s[1:-1].isnumeric(), 'code created is not numeric')

	def test_get_bullet_character(self):
		s = '•'
		b = get_bullet_character()
		self.assertEqual(s, b, 'bullet characters are not the same')

	def test_get_bullet_character_len(self):
		s = get_bullet_character()
		self.assertEqual(1, len(s), 'bullet character is not a single character')

	def test_replace_bullet(self):
		b = get_bullet_character()
		s = ' - '
		self.assertEqual(f' {b} ', replace_bullet(s), 'strings are not equal after bullet replace')

	def test_not_replace_bullet(self):
		s = '-'
		self.assertEqual('-', replace_bullet(s), 'strings are not equal after bullet replace')

	def test_first_array(self):
		a = ['First', 'Second']
		self.assertEqual('First', first(a))

	def test_first_string(self):
		s = 'Test'
		self.assertEqual('T', first(s))


if __name__ == '__main__':
	unittest.main()