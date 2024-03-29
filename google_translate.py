import random
import time
import argparse
import os

import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
	return iter[0]

def print_languages(language_type, languages, attr):
	print(f'{language_type} Languages ({len(languages)}):\n{"-"*70}\n{[getattr(language, attr) for language in languages]}\n')

def main():
	play_languages = get_google_play_languages()
	translate_languages = get_google_translate_languages()

	# Argument parser
	parser = argparse.ArgumentParser()
	parser.add_argument('-ol', '--output-language', nargs='+', required=True,
						help='languages to translate input file to')
	parser.add_argument('-b', '--base-language', default='English',
						help='language of input file')
	parser.add_argument('-i', '--input', default='./input.txt',
						help='location of a text file to translate')
	parser.add_argument('-o', '--output', default='./output.txt',
						help='location of file to ouput translation to')
	parser.add_argument('-t', '--translate', action="store_true",
						help='prints out all Google Translate languages')
	parser.add_argument('-tc', '--translate-codes', action="store_true",
						help='prints out all Google Translate language codes')
	parser.add_argument('-p', '--play', action="store_true",
						help='prints out all Google Play languages')
	parser.add_argument('-pc', '--play-codes', action="store_true",
						help='prints out all Google Play language codes')
	parser.add_argument('-hd', '--head', action="store_true",
						help='runs the browser not in headless mode')
	parser.add_argument('-bl', '--blacklist', nargs='+',
						help='words that do not get translated')
	parser.add_argument('-v', '--verbosity', type=int, default=0,
						help='increase output verbosity')
	args = parser.parse_args()
	if args.play:
		print_languages('Google Play', play_languages, 'name')
	if args.play_codes:
		print_languages('Google Play', play_languages, 'code')
	if args.translate:
		print_languages('Google Translate', translate_languages, 'name')
	if args.translate_codes:
		print_languages('Google Translate', translate_languages, 'code')
	if args.play or args.play_codes or args.translate or args.translate_codes:
		quit()
	if not os.path.exists(args.input):
		print(f'Input file does not exist: {args.input}')
		quit()

	# Blacklist words do not get translated
	blacklist_words = []
	blacklist_codes = []
	if args.blacklist:
		blacklist_words = args.blacklist
	
	header_code = create_code(is_header_code=True)
	base_trans_lang = first(filter_languages([args.base_language], translate_languages))
	if not base_trans_lang:
		print(f'Unable to find base language for {args.base_language}. Run --translate to get langauges.')
		quit()
	if args.verbosity >= 2:
		print(f'Setting base language to {base_trans_lang.name}')
	languages = args.output_language
	if not base_trans_lang in languages:
		if args.verbosity >= 1:
			print(f'Adding base language, {base_trans_lang.name} to output languages')
		languages.insert(0, base_trans_lang.name)
	language_pairs = []
	for language in languages:
		play = filter_languages([language], play_languages)
		for p in play:
			trans = filter_languages([language], translate_languages)
			for t in trans:
				language_pairs.append((t, p))

	# Google Translate url
	url = 'https://translate.google.com/#view=home'
	
	# "What's New" text file
	with open(args.input, 'r') as file:
		change_log_text = [line.rstrip('\n') for line in file]

	# Final text that will be written to output file
	final_text = []

	# Creating blacklist code words and replacing blacklist words with them
	if len(blacklist_words) > 0:
		if args.verbosity >= 1:
			print('Creating blacklist codes')
	code = ''
	for i, word in enumerate(blacklist_words):
		while not code or code == header_code or code in blacklist_codes:
			code = create_code()
		blacklist_codes.append(code)
		for k, text in enumerate(change_log_text):
			change_log_text[k] = text.replace(word, code)

	# Join the change_log_text back together
	change_log_text = '\n'.join(change_log_text)

	options = Options()
	if not args.head:
		options.add_argument('--headless')
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	if args.verbosity >= 1:
		if args.head:
			print('Starting web browser in headless mode')
		else:
			print('Starting web browser in headless mode')
	driver = webdriver.Chrome(options=options) ## Use with Google Chrome
	# driver = webdriver.Firefox() ## Use with Mozilla Firefox

	# Go through each language and get the translation
	for i, pair in enumerate(language_pairs, start=1):

		# Add header to final text
		final_text.append(f'<{pair[1].code}>')

		if base_trans_lang.name.lower() in pair[0].names:
			if args.verbosity >= 1:
				print(f'Adding {base_trans_lang.name} to final text')
			final_text.append(replace_bullet(change_log_text))
		else:
			if args.verbosity >= 1:
				print(f'Translating text to {pair[0].name}')

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

			if args.verbosity >= 2:
				print('Waiting for translation to complete')
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
	if args.verbosity >= 1:
		print('Closing web browser')
	driver.close()

	# Turn blacklist words back into their original words
	if args.verbosity >= 1:
		print('Turning blacklist words back to their original words')
	for i, text in enumerate(final_text):
		for k in range(len(blacklist_words)):
			final_text[i] = text.replace(blacklist_codes[k], blacklist_words[k])

	# Clear out old translated change log file
	# Write final lines to translated change log file
	if args.verbosity >= 1:
		print('Writing translations to output file')
	with open(args.output, 'w+') as file:
		for i, text in enumerate(final_text, start=1):
			# Write each line
			file.write(text)
			# New line except last line
			if not i == len(final_text):
				file.write('\n')
	if args.verbosity >= 2:
		print(f'Translations in file: {args.output}')
	print('DONE!')

if __name__ == "__main__":
	main()
