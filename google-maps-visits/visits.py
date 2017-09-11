class MongoDb:
	from pymongo import MongoClient

	def __init__(self, db, collection):
		self._db = db
		self._collection = collection
		self._client = MongoClient()[db][collection]

	def add(self, records):
		for r in records:
			self._client.update_one({'place_id': r['place_id']}, {'$set': r}, upsert=True)

	def find_missing_url(self):
		return list(self._client.find({'url': {'$exists': False}}))


class MapsApi:
	import json
	import requests

	def __init__(self, keypath, search_keyword):
		self._api_url = 'https://maps.googleapis.com/maps/api/place'
		self._api_format = 'json'
		self._backend = MongoDb('maps_project', 'coffee')
		self._sleep_pagenation = 2
		self._search_keyword = search_keyword
		
		with open(keypath) as f:
			self._api_key = f.read()

	def __get_reponse(self, endpoint, **kwargs):
		url = '{BASE}/{ENDPOINT}/{FORMAT}?{ARGS}&key={KEY}'.format(
			BASE=self._api_url,
			ENDPOINT=endpoint,
			FORMAT=self._api_format,
			ARGS=urlencode(kwargs),
			KEY=self._api_key
			)
		return json.loads(requests.get(url).content)

	def get_nearby(self, **kwargs):
		key = 'results'
		data = self.__get_reponse('nearbysearch', **kwargs)
		self._backend.add(data['results'])

		while 'next_page_token' in data.keys():
			print('Additional page found. Waiting {}ms'.format(self._sleep_pagenation*1000))
			sleep(self._sleep_pagenation)

			params = {
				'pagetoken': data['next_page_token']
			}
			data = self.__get_reponse('nearbysearch', **kwargs)
			self._backend.add(data[key])

	def get_nearby_many(self, points):
		count = len(points)

		i = 1
		for point in points:
			print('Sweeping point {} of {}'.format(i, count))
			params = {
				'location': point,
				'radius': 50000,
				'keyword': self._search_keyword
			}
			search_nearby(**params)
			sleep(self._sleep_pagenation)
			i+=1

	def get_details(self, **kwargs):
		key = 'result'    
		data = self.__get_reponse('details', **kwargs)
		return data[key]

	def append_details(self):
		missing_records = self._backend.find_missing_url()
		count = len(missing_records)

		print('Updating {} records without URL'.format(count))
		i = 1
		for r in missing_records:
			params = {
				'place_id': r['place_id']
			}
			details = self.get_details(**params)

			record = {
				'place_id': place['place_id'],
				'url': details['url']
			}
			self._backend.add([record])

			print('Added record {} of {}. Sleeping {}ms'.format(i, count, self._sleep_pagenation))
			sleep(self._sleep_pagenation)

			i += 1
