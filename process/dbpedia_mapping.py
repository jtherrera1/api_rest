import urllib2
import urllib
import json

DBPEDIA_LOOKUP = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString={0}"

class MappingDBpedia:
	def _find_dbpedia_entities(self, ent):
	        entities =[]
		try:
			entity_encode = urllib.quote(ent.encode('utf8'))
	        	req = urllib2.Request(DBPEDIA_LOOKUP.format(entity_encode))
	        	req.add_header('Accept', 'application/json')
	        	response = urllib2.urlopen(req)
	       		sj =  json.load(response)
        		if  sj['results'] is not None:
                		entities = [ {'uri': entity['uri'], 'label': entity['label'] }  for entity in sj['results']]
		except Exception as e:
			raise ValueError('MappingDBpedia: find_dbpedia_entities(self,entity),'+ str(e))

	        return entities

	def call_counter(func):
		def helper(*args, **kwargs):
	        	helper.calls += 1
	        	return func(*args, **kwargs)
		helper.calls = 0
		helper.__name__= func.__name__
		return helper
	def memoize(func):
		mem = {}
		def memoizer(*args, **kwargs):
			key = str(args) + str(kwargs)
	        	if key not in mem:
	            		mem[key] = func(*args, **kwargs)
	        	return mem[key]
		return memoizer
	@call_counter
	@memoize    
	def _levenshtein_distance(self, source, target):
		if source == "":
	        	return len(target)
	    	if target == "":
	        	return len(source)
	   	if source[-1] == target[-1]:
	        	cost = 0
	   	else:
	        	cost = 1
    
    		res = min([self._levenshtein_distance(source[:-1], target)+1,
	        	   self._levenshtein_distance(source, target[:-1])+1, 
			   self._levenshtein_distance(source[:-1], target[:-1]) + cost])
		return res

	def get_entity(self, entity):
		try:
			entity = entity.strip() if entity else ''

			if (not entity):
				return { 'Message': 'Warning: The Entity is empty'}

			entities = self._find_dbpedia_entities(entity)
			entity =  entity.lower()
			distances = [ {'entity': source, 'distance': self._levenshtein_distance(entity,source['label'].lower())} for source in entities ]
			mapping = sorted(distances, key=lambda k: k['distance'])
			if len(mapping) > 0 :
				list_map = [ value for value in mapping]
				return  { entity: list_map }
                except Exception as e:
                         raise ValueError('MappingDBpedia: get_entity(self,entity),'+ str(e))

                return {entity: 'Warning: Sorry, no results'}

