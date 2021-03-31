import unittest

from google_translate import replace_bullet


class GoogleTranslateTestCase(unittest.TestCase):

	'''
	def test_create_code_header(self):
		pass
	'''

	def test_replace_bullet(self):
		b = '•'
		s = ' - '
		self.assertEqual(replace_bullet(s), f' {b} ', 'strings are not equal after bullet replace')


if __name__ == '__main__':
	unittest.main()