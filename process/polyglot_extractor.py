import polyglot
from dbpedia_mapping import MappingDBpedia

from polyglot.text import Text, Word

class PolyglotExtract:
	def _extract_entity_names(self,data):
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

	def get_entities(self, data):
		try:
		        body = data['body']
		        body = body.encode('utf-8')
		        all_ents = self._extract_entity_names(body)
		        return {'results': all_ents}
                except Exception as e:
                        raise ValueError('NltkExtract: get_entities(self,data),'+ str(e))

                return {}

	def map_entities(self,data):
		try:
			entities = self.get_entities(data)
			entities = entities['results']
        	        object_dbpedia = MappingDBpedia()

			if len(entities) > 0:
				entities = [ object_dbpedia.get_entity(entity) for entity,value in entities.iteritems() ]
		
			return entities
                except Exception:
                       raise ValueError('NltkExtrat: map_entities (sself,data),'+ str(e))
		
		return {}


