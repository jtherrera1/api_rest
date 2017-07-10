#!flask/bin/python
import logging
import json

from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, abort, request
from nltk_extractor import NltkExtract
from calais_extractor import CalaisExtract
from polyglot_extractor import PolyglotExtract


app = Flask(__name__)

@app.errorhandler(404)
def handle_invalid_usage(error):
	response = jsonify({'Error 404':' Error: this page does not exist' })
	app.logger.error('Error: this page does not exist (%d)', 404)
	return response

@app.errorhandler(400)
def handle_invalid_usage(error):
        response = jsonify({'Error 400':' Error: There is a problem in your request' })
        app.logger.error('Error: There is a problem in your request (%d)', 400)
        return response

@app.route('/todo/api/v1.0/calais_entities', methods=['GET','POST'])
def calais_entities():
	try:
	        data = request.get_json()
		object_extractor = CalaisExtract()
		app.logger.info('Info: request /todo/api/v1.0/calais_entities')
		result = object_extractor.get_entities(data)
		return jsonify(result)

        except Exception as e:
                app.logger.error(e)
                abort(400)

        return jsonify({})

@app.route('/todo/api/v1.0/polyglot_entities', methods=['GET','POST'])
def polyglot_entities():
	try:
	        data = request.get_json()
	        object_extractor = PolyglotExtract()
	        app.logger.info('Info: request /todo/api/v1.0/polyglot_entities')
		result = object_extractor.get_entities(data)
                return jsonify(result)
        except Exception as e:
                app.logger.error(e)
                abort(400)

        return jsonify({})

@app.route('/todo/api/v1.0/polyglot_process', methods=['GET','POST'])
def polyglot_process():
	try:
	        data = request.get_json()
		object_extractor = PolyglotExtract() 
	        app.logger.info('Info: request /todo/api/v1.0/polyglot_process')
		result = object_extractor.map_entities(data)
		return jsonify(result)
        except Exception as e:
                app.logger.error(e)
                abort(400)

	return jsonify({})

@app.route('/todo/api/v1.0/nltk_entities', methods=['GET','POST'])
def nlkt_entities():
	try:
	        data = request.get_json()
		object_extractor = NltkExtract()
	        app.logger.info('Info: request /todo/api/v1.0/nltk_entities')
		result = object_extractor.get_entities(data)
		return jsonify(result)
	except Exception as e:
		app.logger.error(e)
		abort(400)
       	return jsonify({})

@app.route('/todo/api/v1.0/nltk_process', methods=['GET','POST'])
def nlkt_process():
	try:
	        data = request.get_json()
		object_extractor = NltkExtract()
	        app.logger.info('Info: request /todo/api/v1.0/nltk_process')
		result = object_extractor.map_entities(data)
	        return jsonify(result)
        except Exception as e:
                app.logger.error(e)
                abort(400)
        return jsonify({})


if __name__ == '__main__':
	handler = RotatingFileHandler('api_rest.log', maxBytes=10000, backupCount=1)
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
    	app.run(debug=True)

