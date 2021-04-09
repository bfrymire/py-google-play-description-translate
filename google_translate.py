import random
import string
import time
import json
import argparse

import urllib.parse
from selenium import webdriver

from languages import Language, get_google_translate_languages, get_google_play_languages, filter_languages


def get_bullet_character():
	return '•'

def replace_bullet(str):
	bullet = get_bullet_character()
	return str.replace(' - ', f' {bullet} ')

def create_code(code_len=15, is_header_code=False):
	code = '{'
	for i in range(code_len):
		code += str(random.choice(range(10)))
	code += '}'
	# Some translations append a period at the end if one doesn't already exist
	if is_header_code and not code[-1] == '.':
		code += '.'
	return code

def first(iter):
	try:
		return iter[0]
	except TypeError:
		print('Not an iterable type, supply an array')
		raise

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--i', '--input', help='location of file to translate',
						type=str)

	args = parser.parse_args()
	
	translate_languages = get_google_translate_languages()
	play_languages = get_google_play_languages()
	header_code = create_code(is_header_code=True)
	blacklist_words = ['Version'] # Blacklist words do not get translated
	blacklist_codes = []
	base_trans_lang = first(filter_languages(['English'], translate_languages))
	languages = ['English', 'Spanish', 'Portuguese']
	language_pairs = []
	for language in languages:
		play = filter_languages([language], play_languages)
		for p in play:
			trans = filter_languages([language], translate_languages)
			for t in trans:
				language_pairs.append((t, p))

	print("language_pairs:")
	for pair in language_pairs:
		print(pair)

	# Google Translate url
	url = 'https://translate.google.com/#view=home'
	
	# "What's New" text file
	with open('input.txt', 'r') as file:
		change_log_text = [line.rstrip('\n') for line in file]

	# Final text that will be written to translated_change_log
	final_text = []

	# Editing special words that shouldn't be translated
	code = ''
	for i, word in enumerate(blacklist_words):
		while not code or code == header_code or code in blacklist_codes:
			code = create_code()
		blacklist_codes.append(code)
		for k, text in enumerate(change_log_text):
			change_log_text[k] = text.replace(word, code)

	# Join the change_log_text back together
	change_log_text = '\n'.join(change_log_text)

	# driver = webdriver.Chrome() ## Use with Google Chrome
	driver = webdriver.Chrome('./chromedriver/chromedriver') ## Use with Google Chrome
	# driver = webdriver.Firefox() ## Use with Mozilla Firefox

	# Go through each language and get the translation
	for i, pair in enumerate(language_pairs, start=1):

		print(pair)

		# Add header to final text
		final_text.append(f'<{pair[1].code}>')

		if base_trans_lang.name.lower() in pair[0].names:
			final_text.append(replace_bullet(change_log_text))
		else:
			# Params to pass into the url
			params = {
				'op': 'translate',
				'sl': base_trans_lang.code,
				'tl': pair[0].code,
				'text': f'{header_code}\n{change_log_text}',
			}

			# Create the full url
			full_url = f'{url}&{urllib.parse.urlencode(params)}'

			# Go to the full url
			driver.get(full_url)

			# Wait for translation to load
			while True:
				try:
					elem = driver.find_element_by_xpath(f'//span[contains(text(), "{header_code}")]')
					break
				except:
					time.sleep(0.25)

			# Getting translated text
			parent = elem.find_element_by_xpath('../../..')
			class_ = parent.get_attribute('class')
			lines = driver.execute_script(f'return document.querySelector(".{class_}").innerText').split('\n')

			# Cleaning text
			for k, line in enumerate(lines):
				# Skip blank lines and the header_code line
				if not line or not k:
					continue
				# Remove non-breaking spaces unicode character
				line = line.replace('&nbsp', ' ')
				# Remove trailing periods
				while line[-1] == '.':
					line = line[:-1]
				# Append space in front of bullet points
				if line[0] == '-':
					line = ' ' + line
				# Replace dashes with bullet points
				line = replace_bullet(line)

				# Add cleaned current line text to final text
				final_text.append(line)

		# Add footer to final text
		final_text.append(f'</{pair[1].code}>')

		# Add a line break between language blocks
		if not i == len(language_pairs):
			final_text.append('')

	# Close the webdriver
	driver.close()

	# Turn special words back into their original word
	for i, text in enumerate(final_text):
		for k in range(len(blacklist_words)):
			final_text[i] = text.replace(blacklist_codes[k], blacklist_words[k])

	# Clear out old translated change log file
	# Write final lines to translated change log file
	with open('output.txt', 'w+') as file:
		for i, text in enumerate(final_text):
			# Write each line
			file.write(text)
			# New line except last line
			if not i == len(final_text) - 1:
				file.write('\n')


if __name__ == "__main__":
	main()
