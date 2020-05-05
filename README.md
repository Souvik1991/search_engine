This is a small app which runs on ###`Flask` to serve api. It has an api endpoing `/search/` which accept `POST` request with arguments `quaries` and `K`.
`quaries` contains the array of all query
`K` contains the number of responses will be reverted back

Example:
`{"quaries":["what based hope"], "K":3}`

## To run the app
1. Create a virtualenv using the command `virtualenv <PATH TO VIRTUALENV>`
2. Activate the virtualenv by running `source <PATH TO VIRTUALENV>/bin/active`
3. Install all the dependencies present on the `requirements.txt` by running `pip install -r requirements.txt`
4. Now to run the API server type in the following command `python search.py`
5. To do unit test run `python unit_test.py`
6. To preprocess the data again delete the existing `data.processed.json` file and run `python preprocess_data.py`