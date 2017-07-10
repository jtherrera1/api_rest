#!flask/bin/python

import nlkt_extractor
import calais_extractor
import polyglot_extractor
import json

from flask import Flask, jsonify, abort, request

app = Flask(__name__)

@app.errorhandler(404)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@app.route('/todo/api/v1.0/calais_entities', methods=['GET','POST'])
def calais_entities():
        data = request.get_json()
        return jsonify(calais_extractor.get_entities(data))

@app.route('/todo/api/v1.0/polyglot_entities', methods=['GET','POST'])
def polyglot_entities():
        data = request.get_json()
        return jsonify(polyglot_extractor.get_entities(data))

@app.route('/todo/api/v1.0/polyglot_process', methods=['GET','POST'])
def polyglot_process():
        data = request.get_json()
        return jsonify(polyglot_extractor.map_entities(data))

@app.route('/todo/api/v1.0/nlkt_entities', methods=['GET','POST'])
def nlkt_entities():
        data = request.get_json()
        return jsonify(nlkt_extractor.get_entities(data))

@app.route('/todo/api/v1.0/nlkt_process', methods=['GET','POST'])
def nlkt_process():
        data = request.get_json()
        return jsonify(nlkt_extractor.map_entities(data))


if __name__ == '__main__':
    	app.run(debug=True)

