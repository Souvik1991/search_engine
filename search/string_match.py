# -*- coding: utf-8 -*-
from __future__ import division

import time
import json
import difflib
from itertools import combinations

from .words import all_words

# Loading the word map on the memory
word_map = {}
with open('word.map.json', 'r') as f:
	word_map = json.loads(f.read())
	# print sorted(word_map.keys())

# Loading the data on the memory
data = {}
with open('data.processed.json', 'r') as f:
	data = json.loads(f.read())


# Quick sort a array of object using a key value
def quick_sort_array_of_object(arr, key):
	less = []
	pivot_list = []
	more = []
	if len(arr) <= 1:
		return arr
	else:
		pivot = arr[0]
		for i in arr:
			if i.get(key) < pivot.get(key):
				less.append(i)
			elif i.get(key) > pivot.get(key):
				more.append(i)
			else:
				pivot_list.append(i)
			
		less = quick_sort_array_of_object(less, key)
		more = quick_sort_array_of_object(more, key)
		return less + pivot_list + more


# Creating fuzzy words from the words
# It creates all the combination of words possible
def create_fuzzy_words(word, keys):
	unique_words = [word]
	wlen = len(word)
	# Appending words which contain strings
	for k, d in enumerate(keys):
		if word in d and d not in unique_words and wlen/len(d) > .4:
			unique_words.append(d)

	# print difflib.get_close_matches(word, keys, 2, 0.55)
	word_array = [w for w in word]
	for i in range(1, wlen):
		# if i > int(wlen/2):
		# 	break
		for comb in list(combinations(word_array, i)):
			strr = ''.join(comb)
			if word_map.get(strr):
				flen = len(strr)
				# Measuring how much percentage of alphabets it contains of the main word
				percentage = flen/wlen
				# If the alphabets appearance is more than 55% of the main word consider it
				# print percentage
				if strr not in unique_words and percentage > .5:
					unique_words.append(strr)
	return unique_words


# calculating the score
# It takes the words and book id as argument
def calculate_score(fuzzy_words, words, word_data):
	mapping = word_data.get('mapping')
	total_words = word_data.get('word_count')
	total_score = 0
	total_word_present = 0
	# print fuzzy_words
	for word in words:
		# For the exact words scoring it higher than fuzzy words
		if mapping.get(word):
			total_word_present += 1
			total_score += mapping.get(word).get('appearance') * 1
			# Calculating score based on the position of the string
			# The more close it appear to the begin the score will be more high
			for pos in mapping.get(word).get('position'):
				total_score += ((total_words - pos)/100) * .5

		else:
			for i in range(1, len(fuzzy_words[word])):
				w = fuzzy_words[word][i]
				if mapping.get(w):
					total_score += mapping.get(w).get('appearance') * .2
					# Calculating score based on the position of the string
					# The more close it appear to the begin the score will be more high
					for pos in mapping.get(w).get('position'):
						total_score += ((total_words - pos)/100) * .1

	total_score += total_word_present * 15

	return total_score
	# return total_score,


# Loop through all book ids and return unique book ids
# Which will be used to calculate score
def get_unique_bids(temp_array):
	temp = set([])
	for i, val in enumerate(temp_array):
		if val not in temp:
			temp.add(val)
			
	return list(temp)


# Main function of the search engine code
# Which takes the query and count as input
# Return the relevant book data
def search_engine(query, count):
	if not query: return []
	keys = word_map.keys()
	query = query.lower().strip()
	words = [f.strip() for f in query.split(' ') if f and f not in all_words]
	# wlen = len(words)
	book_id_object = {}
	considered_id = []
	temp_array = []
	fuzzy_words = {}
	for w in words:
		fuzzy = create_fuzzy_words(w, keys)
		fuzzy_words[w] = fuzzy
		for f in fuzzy:
			if word_map.get(f):
				temp_array += word_map.get(f)

	considered_id = get_unique_bids(temp_array)
	return_data = []
	for cid in considered_id:
		word_data = json.loads(json.dumps(data.get(str(cid))))
		score = calculate_score(fuzzy_words, words, word_data)
		word_data['score'] = score
		word_data['id'] = cid
		del word_data['mapping']
		del word_data['word_count']
		# del word_data['score']
		# del word_data['summary']
		# del word_data['title']
		return_data.append(word_data)

	return_data = quick_sort_array_of_object(return_data, 'score')[::-1]
	return return_data[0:count]


if __name__ == "__main__":
	stime = time.time()
	print search_engine("problems", 1)
	print time.time() - stime
