# -*- coding: utf-8 -*-
from __future__ import division

import time
import copy 
import json
# import 
from itertools import combinations

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
def create_fuzzy_words(word):
	unique_words = [word]
	word_array = [w for w in word]
	wlen = len(word)
	for i in range(1, wlen):
		for comb in list(combinations(word_array, i)):
			strr = ''.join(comb)
			if word_map.get(strr):
				flen = len(strr)
				# Measuring how much percentage of alphabets it contains of the main word
				percentage = flen/wlen
				# If the alphabets appearance is more than 50% of the main word consider it
				# print percentage
				if strr not in unique_words and percentage > .5:
					unique_words.append(strr)
	return unique_words


def order_by_appearance(fuzzy, book_object):
	temp = set([])
	for f in fuzzy:
		for i, val in enumerate(word_map.get(f) or []):
			# print val
			if val not in temp:
				temp.add(val)
				if not book_object.get(val):
					book_object[val] = 1
				else:
					book_object[val] += 1
	return book_object


# calculating the score
# It takes the words and book id as argument
def calculate_score(words, word_data):
	mapping = word_data.get('mapping')
	total_words = word_data.get('word_count')
	total_score = 0
	for w in words:
		if mapping.get(w):
			total_score += mapping.get(w).get('appearance')
			for pos in mapping.get(w).get('position'):
				total_score += (total_words - pos)/100

	return total_score
	# return total_score,


# Main function of the search engine code
# Which takes the query and count as input
# Return the relevant book data
def search_engine(query, count):
	if not query: return []
	query = query.lower().strip()
	words = [f.strip() for f in query.split(' ') if f]
	wlen = len(words)
	book_id_object = {}
	for w in words:
		fuzzy = create_fuzzy_words(w)
		print fuzzy
		book_id_object = order_by_appearance(fuzzy, book_id_object)
		# book_object = get_matching_book_ids(fuzzy, book_object)
	
	length_obj = {}
	print book_id_object
	for k in book_id_object:
		if not length_obj.get(book_id_object[k]):
			length_obj[book_id_object[k]] = [k]
		elif k not in length_obj.get(book_id_object[k]):
			length_obj.get(book_id_object[k]).append(k)

	clen = wlen
	considered_id = []
	while len(considered_id) < count and clen >= 0:
		if length_obj.get(clen):
			considered_id += length_obj.get(clen)
		clen -= 1

	return_data = []
	print considered_id
	for cid in considered_id:
		word_data = copy.deepcopy(data.get(str(cid)))
		score = calculate_score(words, word_data)
		word_data['score'] = score
		word_data['id'] = cid
		del word_data['mapping']
		del word_data['word_count']
		# del word_data['word_count']
		return_data.append(word_data)

	return_data = quick_sort_array_of_object(return_data, 'score')[::-1]
	return return_data#[0:count]


if __name__ == "__main__":
	stime = time.time()
	print search_engine("achieve take books", 3)
	print time.time() - stime
	# print order_by_appearance(['problems', 'problem'], {})
