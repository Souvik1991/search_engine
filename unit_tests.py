# -*- coding: utf-8 -*-
from __future__ import division
import unittest

from search.string_match import quick_sort_array_of_object, get_unique_bids, create_fuzzy_words, calculate_score, search_engine

if __name__ == "__main__":
	assert quick_sort_array_of_object([{'a': 5, 'score': 10}, {'a': 1, 'score': 2}], 'score') == [{'a': 1, 'score': 2}, {'a': 5, 'score': 10}]
	assert get_unique_bids([0, 0, 23, 3, 23, 1]) == [0, 1, 3, 23]
	assert create_fuzzy_words('prob', ['problems', 'problem', 'prob']) == ['prob', 'problems', 'problem']
	assert create_fuzzy_words('problems', ['problems', 'problem', 'prob']) == ['problems', 'problem']
	assert str(calculate_score({'problems': ['problems', 'problem']}, ['problems'], {'word_count': 56, 'mapping': {'problems': {'position': [16, 28], 'appearance': 2}}})) == '17.34'
	assert search_engine("problems", 1) == [{u'title': u'Slipstream Time Hacking', u'summary': u'The Book in Three Sentences:\xa0Finding something important and meaningful in your life is the most productive use of your time and energy. This is true because every life has problems associated with it and finding meaning in your life will help you sustain the effort needed to overcome the particular problems you face. Thus, we can say that the key to living a good life is not giving a fuck about more things, but rather, giving a fuck only about the things that align with your personal values.', 'score': 17.34, 'id': 48}]


# assert correction('speling') == 'spelling' 