import requests
API_KEY = 'GDXA5Upoh3AM1AXcMQxj8egMMWikYGjf' # your Calais API key.
CALAIS_URL = 'https://api.thomsonreuters.com/permid/calais' # this is the older REST interface.

class CalaisExtract:

	def _extract_entity_names(self, data):
		entities = []
		dictionary = {"_typeReference", "_type", "name", "relevance"}
		for key in data:
	        	values = data[key]
			entity ={ key: value for key,value in values.items()  if key in dictionary}
			if len(entity) >= 1:
				entities.append(entity)
		return entities	

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

			headers = {'X-AG-Access-Token' : API_KEY, 'Content-Type' : 'text/raw', 'outputformat' : 'application/json'}
			response = requests.post(CALAIS_URL, data=body, headers=headers, timeout=80)
			data =  response.json()
			if 'error' in data:
				return {'results': data} 
			all_ents = self._extract_entity_names(data)
			return {'results': all_ents}

		except Exception as e:
			raise ValueError('CalaisExtract: get_entities(self,data),'+ str(e))

