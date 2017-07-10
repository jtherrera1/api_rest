import urllib2
import urllib
import json

DBPEDIA_LOOKUP = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryString={0}"
def find_dbpedia_entities(ent):
        entities =[]
	try:
		entity_encode = urllib.quote(ent.encode('utf8'))
        	req = urllib2.Request(DBPEDIA_LOOKUP.format(entity_encode))
        	req.add_header('Accept', 'application/json')
        	response = urllib2.urlopen(req)

       		sj =  json.load(response)

        	if  sj['results'] is not None:
                	entities = [ {'uri': entity['uri'], 'label': entity['label'] }  for entity in sj['results']]
	except Exception:
		print ("Sorry: the entity "+ ent + "was not found. ")

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
def levenshtein_distance(source, target):
	if source == "":
        	return len(target)
    	if target == "":
        	return len(source)
   	if source[-1] == target[-1]:
        	cost = 0
   	else:
        	cost = 1
    
    	res = min([levenshtein_distance(source[:-1], target)+1,
        	   levenshtein_distance(source, target[:-1])+1, 
		   levenshtein_distance(source[:-1], target[:-1]) + cost])
	return res

def get_entity(entity):
	entities = find_dbpedia_entities(entity)
	entity =  entity.lower()
	distances = [ {'entity': source, 'distance': levenshtein_distance(entity,source['label'].lower())} for source in entities ]
	mapping = sorted(distances, key=lambda k: k['distance'])
	if len(mapping) > 0 :
		list_map = [ value for value in mapping]
		return  { entity: list_map }
	return  { entity: None }

