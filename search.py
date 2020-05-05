# -*- coding: utf-8 -*-
import json
import requests
from flask import Flask, request
from search.string_match import search_engine
app = Flask(__name__)

# Fetch the author details from the microservice provided
# This function need book id as params
def fetch_author(book_id):
	link = 'https://ie4djxzt8j.execute-api.eu-west-1.amazonaws.com/coding'
	res = requests.post(link, data=json.dumps({"book_id": book_id}))
	# print res.status_code
	if res.status_code == 200:
		return json.loads(res.text)
	return None


@app.route('/search/', methods=['POST'])
def api_search():
	if request.method == 'POST':
		data_arg = request.form or request.get_json()
		quaries = data_arg.get('quaries') or '[]'
		if type(quaries) == unicode:
			quaries = json.loads(quaries)

		K = int(data_arg.get('K')) or 3
		unique_book_ids = []
		books = {}
		for query in quaries:
			data = search_engine(query, K)
			books[query] = data
			for d in data:
				if d.get('id') not in unique_book_ids:
					unique_book_ids.append(d.get('id'))

		author_object = {}
		for book in unique_book_ids:
			author = fetch_author(book)
			if author:
				author_object[book] = author.get('author')

		temp_array = []
		for query in quaries:
			for book in books[query]:
				book['author'] = author_object.get(book.get('id'))

			temp_array.append(books[query])

		return {"books": temp_array}

if __name__ == '__main__':
	app.run(debug=True)
