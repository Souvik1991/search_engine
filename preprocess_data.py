import os
import re
import json

from search.words import all_words

# Read the raw file from json and parse it
# Return the JSON value
def read_raw_data():
	with open('./data.json') as f:
		data = f.read()
		data = json.loads(data)
		return data

# Removing all unicodes as well
# Remove all special characters
def replace_special_characters(string):
	# Replacing unicode to "'"
	string = string.replace(u"\u2019", "'")
	string = re.sub(r'[^\x00-\x7F]+', ' ', string)
	string = re.sub('[/.,-/(/)!@#$%^&/*-_+=;:]', ' ', string)

	return string


# Create word map
def generate_mapping(summary, bid, main_word_id_map):
	# Cleaning up the summary text
	# Removing the repeating text, and universal text
	summary = summary.replace('The Book in Three Sentences:', '')
	summary = summary.lower().strip()
	summary = replace_special_characters(summary)

	# Splitting the summary to get words
	# Keeping the position so that we can detemint the score later on
	# Also the appearance of word in the summary
	words = summary.split(' ')
	word_object = {}
	counter = 0
	for word in words:
		if word and word not in all_words:
			if not word_object.get(word):
				word_object[word] = {
					'appearance': 0,
					'position': []
				}
			word_object.get(word)['appearance'] += 1
			word_object.get(word).get('position').append(counter)

			counter += 1

			if not main_word_id_map.get(word):
				main_word_id_map[word] = [bid]
			elif bid not in main_word_id_map.get(word):
				main_word_id_map.get(word).append(bid)


	# print word_object
	# print '--'
	# print main_word_id_map
	return word_object, main_word_id_map, counter


# Entry point for the code
def start_processing(data):
	temp_object = {}
	main_word_id_map = {}
	for d in data.get('summaries'):
		mapping, main_word_id_map, counter = generate_mapping(d.get('summary', ''), d.get('id'), main_word_id_map)
		temp_object[d.get('id')] = {
			"title": data.get("titles")[d.get('id')],
			"summary": d.get('summary'),
			"mapping": mapping,
			"word_count": counter
		}

		# if d.get('id') == 51:
		# 	# print str(d.get('summary').encode('unicode_escape')).encode("utf-8")
		# 	print d.get('summary')
		# 	print d.get('summary').replace(u"\u2019", "'")
		# 	print re.sub(r'[^\x00-\x7F]+', ' ', d.get('summary'))
		# 	break
	
	# This file contains processed data with each words appearance count and position
	# where they hace appeared
	with open('data.processed.json', 'w') as f:
		f.write(json.dumps(temp_object))

	# This file contains all the words and all the ids where this word is present
	with open('word.map.json', 'w') as f:
		f.write(json.dumps(main_word_id_map))

	return True


if __name__ == "__main__":
	data = read_raw_data()
	if not os.path.exists('data.processed.json'):
		start_processing(data)
