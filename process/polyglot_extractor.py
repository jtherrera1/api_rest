import polyglot
import logging
logging.basicConfig()

from dbpedia_mapping import MappingDBpedia

from polyglot.text import Text, Word

class PolyglotExtract:
	def _extract_entity_names(self,data):
		text = Text(data, hint_language_code="pt")
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
                        if data is None:
                                return {'results': 'Sorry, the request is empty'}
                        if 'body' not in data:
                                return {'results': 'The data sent does not have the appropriate structure'}

                        body = data['body']

                        body = body.strip() if body else ''

                        if (not body):
                                return { 'results': 'Warning: The Entity is empty'}

		        body = body.encode('utf-8')
		        all_ents = self._extract_entity_names(body)
		        return {'results': all_ents}
                except Exception as e:
                        raise ValueError('PolyglotExtract: get_entities(self,data),'+ str(e))


	def map_entities(self,data):
		try:
			entities = self.get_entities(data)
			entities = entities['results']
                        if  type(entities) == str :
                                return { 'results': entities}

        	        object_dbpedia = MappingDBpedia()

			if len(entities) > 0:
				entities = [ object_dbpedia.get_entity(entity) for entity,value in entities.iteritems() ]
		
			return {'results': entities}
                except Exception as e:
                       raise ValueError('PolyglotExtract: map_entities (sself,data),'+ str(e))
		

