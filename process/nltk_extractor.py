import nltk
import urllib2
from dbpedia_mapping import MappingDBpedia

class NltkExtract:

	def _extract_entity_names(self, t):
		entity_names = []

		if hasattr(t, 'label') and t.label:
			if t.label() == 'NE':
				entity_names.append(' '.join([child[0] for child in t]))
			else:
				for child in t:
					entity_names.extend(self._extract_entity_names(child))
		return entity_names

	def _get_unique_entity(self,entities):
	        dictionary ={}
		entity_names = []
	        for entity in entities:
	                if entity in dictionary.keys():
	                        pass
	                else:
	                        dictionary[entity]= entity
				entity_names.append(entity)

	        return entity_names


	def get_entities(self,data):
		try:
                        if data is None:
                                return {'results': 'Sorry, the request is empty'}
                        if 'body' not in data:
                                return {'results': 'The data sent does not have the appropriate structure'}

                        body = data['body']

                        body = body.strip() if body else ''

                        if (not body):
                                return { 'results': 'Warning: The Entity is empty'}

			sentences = nltk.sent_tokenize(body, language='portuguese')
			tokenized_sentences = [nltk.word_tokenize(sentence.encode('utf-8')) for sentence in sentences]
			tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
			chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
			entity_names = []

			#find name entities
			for tree in chunked_sentences:
				entity_names.extend(self._extract_entity_names(tree))

			entity_names = self._get_unique_entity(entity_names)

			return {'results': entity_names}

		except Exception as e:
			raise ValueError('NltkExtract: get_entities(self,data),'+ str(e))


	def map_entities(self, data):
		try:
		        entities = self.get_entities(data)
		        entities = entities['results']
			if  type(entities) == str :
				return { 'results': entities}

			object_dbpedia = MappingDBpedia()
		        if len(entities) > 0:
		                entities = [ object_dbpedia.get_entity(entity.decode('utf-8')) for entity in entities]

	        	return {'results': entities}

                except Exception as e:
                       raise ValueError('NltkExtrat: map_entities (sself,data),'+ str(e))

