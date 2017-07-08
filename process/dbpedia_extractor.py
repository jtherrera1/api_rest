#!flask/bin/python
import nltk
import urllib2
import json

def extract_entity_names(t):
	entity_names = []

	if hasattr(t, 'label') and t.label:
		if t.label() == 'NE':
			entity_names.append(' '.join([child[0] for child in t]))
		else:
			for child in t:
				entity_names.extend(extract_entity_names(child))
	return entity_names

def find_dbpedia_entities(entity):
	dbpedia_url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString={0}"
	req = urllib2.Request(dbpedia_url.format(entity))
	req.add_header('Accept', 'application/json')
	response = urllib2.urlopen(req)

	sj =  json.load(response)

        entity_url = "None"
        entity_label = "None"

	if  sj['results'] is not None and len (sj['results'])>0:
		entity_url = sj['results'][0]['uri']
		entity_label = sj['results'][0]['label']
		

	return {'url': entity_url, 'label':entity_label}

def process_all(data):
	body = data['body']
	sentences = nltk.sent_tokenize(body)
	tokenized_sentences = [nltk.word_tokenize(sentence.encode('utf-8')) for sentence in sentences]
	tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
	chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
	entity_names = []
	#TODO find name entities
	for tree in chunked_sentences:
		entity_names.extend(extract_entity_names(tree))
	all_ents = {}
	for ent in entity_names:
		# find name entities using dbpedia
		all_ents[ent] = find_dbpedia_entities(ent)
		#TODO classify name entities using dbpedia
	return {'results': all_ents}

