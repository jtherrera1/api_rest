import polyglot
import dbpedia_mapping

from polyglot.text import Text, Word

def extract_entity_names(data):
	text = Text(data)
	entities = [ entity for sentence in text.sentences  for entity in sentence.entities]
	dictionary ={}
	for entity in entities:
        	value = ' '.join(entity)
        	if value in dictionary.keys():
			pass
        	else:
                	dictionary[value]= entity.tag

	return dictionary

def get_entities(data):
        body = data['body']
        body = body.encode('utf-8')
        all_ents = extract_entity_names(body)
        return {'results': all_ents}

def map_entities(data):
	entities = get_entities(data)
	entities = entities['results']
	if len(entities) > 0:
		entities = [ dbpedia_mapping.get_entity(entity) for entity,value in entities.iteritems() ]
		
	return entities
