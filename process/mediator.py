#!flask/bin/python

import dbpedia_extractor
import calais_extractor

import json

from flask import Flask, jsonify, abort, request

app = Flask(__name__)

@app.errorhandler(404)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@app.route('/todo/api/v1.0/calais', methods=['GET','POST'])
def process_calais():
        data = request.get_json()
        return jsonify(calais_extractor.process_all(data))

@app.route('/todo/api/v1.0/search', methods=['GET','POST'])
def process_dbpedia():
	data = request.get_json()
	return jsonify(dbpedia_extractor.process_all(data))

if __name__ == '__main__':
    	app.run(debug=True)

