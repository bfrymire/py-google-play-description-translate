import random
import string
import time

import urllib.parse
from selenium import webdriver


def replace_bullet(str):
	# Bullet character
	bullet = '•'
	return str.replace(' - ', f' {bullet} ')

def create_header(header_len=15):
	header = ''
	for i in range(header_len):
		if i % 5 == 0 and i:
			header += "."
		header += str(random.choice(range(10)))
	if not header[-1] == '.':
		header += '.'
	return header


if __name__ == "__main__":

	# driver = webdriver.Chrome() ## Use with Google Chrome
	driver = webdriver.Chrome('./chromedriver/chromedriver') ## Use with Google Chrome
	# driver = webdriver.Firefox() ## Use with Mozilla Firefox

	header = create_header()
	special_words = ['Version'] ## Special words do not get translated
	new_words = []
	original_language = 'en'
	languages = ['en', 'es', 'pt']
	language_codes = ['en-US', 'es-ES', 'pt-BR']
	# Google Translate url
	url = 'https://translate.google.com/#view=home'
	# "What's New" text file

	with open('input.txt', 'r') as file:
		change_log_text = [line.rstrip('\n') for line in file]

	# Final text that will be written to translated_change_log
	final_text = []

	# Editing special words that shouldn't be translated
	for i in range(len(special_words)):
		new_word = ''
		for n in range(10):
			new_word += random.choice(string.ascii_uppercase)
			if n == 4:
				new_word += '-'
		new_words.append(new_word)
		for k in range(len(change_log_text)):
			change_log_text[k] = change_log_text[k].replace(special_words[i], new_word)

	# Join the change_log_text back together
	change_log_text = '\n'.join(change_log_text)

	# Go through each language and get the translation
	for l in range(len(languages)):

		# Add header to final text
		final_text.append(f'<{language_codes[l]}>')

		if languages[l] == original_language:
			final_text.append(replace_bullet(change_log_text))
		else:
			# Params to pass into the url
			params = {
				'op': 'translate',
				'sl': original_language,
				'tl': languages[l],
				'text': f'{header}\n{change_log_text}',
			}

			# Create the full url
			full_url = f'https://translate.google.com/#view=home&{urllib.parse.urlencode(params)}'

			# Go to the full url
			driver.get(full_url)

			# Wait for translation to load
			while True:
				try:
					elem = driver.find_element_by_xpath(f'//span[contains(text(), "{header}")]')
					break
				except:
					time.sleep(0.25)

			parent = elem.find_element_by_xpath('../..')
			lines = parent.text.split('\n')

			# Cleaning text
			for i in range(1, len(lines)):
				# Get the inner text of the element
				current_line = lines[i]
				# Skip blank lines
				if not current_line:
					continue
				# Remove non-breaking spaces unicode character
				current_line = current_line.replace('&nbsp', ' ')
				# Remove trailing periods
				while current_line[-1] == '.':
					current_line = current_line[:-1]
				# Append space in front of bullet points
				if current_line[0] == '-':
					current_line = ' ' + current_line
				# Replace dashes with bullet points
				current_line = replace_bullet(current_line)

				# Add cleaned current line text to final text
				final_text.append(current_line)

		# Add footer to final text
		final_text.append(f'</{language_codes[l]}>')

		# Add a line break between language blocks
		if not l == len(languages) - 1:
			final_text.append('')

	# Close the webdriver
	driver.close()

	# Turn special words back into their original word
	for i in range(len(final_text)):
		for k in range(len(special_words)):
			final_text[i] = final_text[i].replace(new_words[k], special_words[k])

	# Clear out old translated change log file
	# Write final lines to translated change log file
	with open('output.txt', 'w+') as file:
		for i in range(len(final_text)):
			# Write each line
			file.write(final_text[i])
			# New line except last line
			if not i == len(final_text) - 1:
				file.write('\n')
