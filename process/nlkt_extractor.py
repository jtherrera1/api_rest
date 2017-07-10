import nltk
import urllib2
import dbpedia_mapping

def extract_entity_names(t):
	entity_names = []

	if hasattr(t, 'label') and t.label:
		if t.label() == 'NE':
			entity_names.append(' '.join([child[0] for child in t]))
		else:
			for child in t:
				entity_names.extend(extract_entity_names(child))
	return entity_names

def get_unique_entity(entities):
        dictionary ={}
	entity_names = []
        for entity in entities:
                if entity in dictionary.keys():
                        pass
                else:
                        dictionary[entity]= entity
			entity_names.append(entity)

        return entity_names


def get_entities(data):
	body = data['body']
	sentences = nltk.sent_tokenize(body, language='portuguese')
	tokenized_sentences = [nltk.word_tokenize(sentence.encode('utf-8')) for sentence in sentences]
	tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
	chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
	entity_names = []

	#find name entities
	for tree in chunked_sentences:
		entity_names.extend(extract_entity_names(tree))

	entity_names = get_unique_entity(entity_names)

	return {'results': entity_names}

def map_entities(data):
        entities = get_entities(data)
        entities = entities['results']
        if len(entities) > 0:
                entities = [ dbpedia_mapping.get_entity(entity.decode('utf-8')) for entity in entities]

        return entities
