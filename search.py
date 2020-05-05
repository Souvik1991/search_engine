# -*- coding: utf-8 -*-
import json
import requests
from flask import Flask, request
from flask_cors import cross_origin
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
@cross_origin()
def api_search():
	# Checking if the request if POST or not
	if request.method == 'POST':
		# Handle different kind of request method
		# If the data has been passed as form data or json data
		data_arg = request.form or request.get_json()
		quaries = data_arg.get('quaries') or '[]'
		if type(quaries) == unicode:
			quaries = json.loads(quaries)

		# setting the number of responses should be passed back
		K = int(data_arg.get('K', 0)) or 3
		# Creating unique book id array, so that the third party api would be called only once for each book
		unique_book_ids = []
		# Storing the book details with their query as key so we can fetch them later on
		books = {}
		for query in quaries:
			data = search_engine(query, K)
			books[query] = data
			for d in data:
				if d.get('id') not in unique_book_ids:
					unique_book_ids.append(d.get('id'))

		# Setting author details for each book
		# Making sure that we call the api one time for each book id
		author_object = {}
		for book in unique_book_ids:
			author = fetch_author(book)
			if author:
				author_object[book] = author.get('author')

		# Formatting the response
		# Adding author details to the response
		temp_array = []
		for query in quaries:
			for book in books[query]:
				book['author'] = author_object.get(book.get('id'))

			temp_array.append(books[query])

		return {"quaries": quaries, "K": K, "books": temp_array}

if __name__ == '__main__':
	app.run(debug=True)
