#!flask/bin/python
import nltk
import urllib2
import json
from flask import Flask, jsonify, abort

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def extract_entity_names(t):
	entity_names = []

	if hasattr(t, 'label') and t.label:
		if t.label() == 'NE':
			entity_names.append(' '.join([child[0] for child in t]))
		else:
			for child in t:
				entity_names.extend(extract_entity_names(child))

	return entity_names

def find_dbpedia_classes(entity):
	dbpedia_url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString={0}"
	print dbpedia_url.format(entity)
	req = urllib2.Request(dbpedia_url.format(entity))
	req.add_header('Accept', 'application/json')
	response = urllib2.urlopen(req)
	sj =  json.load(response)
	ent_classes = sj['results'][0]['classes']
	rec = []
	for ec in ent_classes:
		rec.append(ec['label']) 
	return rec

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/search/<string:text>', methods=['GET'])
def process_all(text):
	sentences = nltk.sent_tokenize(text)
	tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
	tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
	chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
	entity_names = []
	#TODO find name entities in other language other than english
	for tree in chunked_sentences:
		entity_names.extend(extract_entity_names(tree))
	all_ents = {}
	for ent in entity_names:
		# find name entities using dbpedia
		all_ents[ent] = find_dbpedia_classes(ent)
		#TODO classify name entities using dbpedia
	return jsonify({'results': all_ents})

	if __name__ == '__main__':
    		app.run(debug=True)

