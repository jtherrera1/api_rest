import requests
API_KEY = 'GDXA5Upoh3AM1AXcMQxj8egMMWikYGjf' # your Calais API key.
CALAIS_URL = 'https://api.thomsonreuters.com/permid/calais' # this is the older REST interface.

def extract_entity_names(data):
	entities = []
	dictionary = {"_typeReference", "_type", "name", "relevance"}
	for key in data:
        	values = data[key]
		entity ={ key: value for key,value in values.items()  if key in dictionary}
		if len(entity) >= 1:
			entities.append(entity)
	return entities	

def process_all(data):
	body = data['body']
	body = body.encode('utf-8')
	headers = {'X-AG-Access-Token' : API_KEY, 'Content-Type' : 'text/raw', 'outputformat' : 'application/json'}
	response = requests.post(CALAIS_URL, data=body, headers=headers, timeout=80)
	data =  response.json()
	print data
	all_ents = extract_entity_names(data)
	return {'results': all_ents}
