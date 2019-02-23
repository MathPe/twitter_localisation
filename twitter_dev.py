from twython import Twython
from geopy.geocoders import Nominatim
import json
import gmplot

geolocator = Nominatim(user_agent="test_geo")

# Load credentials
with open("twitter_credentials.json", "r") as file:
	credentials = json.load(file)

collected_tweets = Twython(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])

# Add filters to our query
query = {
		'q': "snow OR Snow OR rain OR Rain",
		'result_type': 'recent',
		'count': 100,
		'lang': 'fr'
		}


coordinates = {'latitude': [], 'longitude': []}
for i in range(0,20):
	for status in collected_tweets.search(**query)['statuses']:

		location = status['geo']
		if location == None:
			location = status['user']['location']

		try:
			locator = geolocator.geocode(location)

			if locator:
				coordinates['latitude'].append(locator.latitude)
				coordinates['longitude'].append(locator.longitude)

		except:
			pass

gmap = gmplot.GoogleMapPlotter(30,0,3)
gmap.heatmap(coordinates['latitude'], coordinates['longitude'], radius=20)

gmap.draw("python_heatmap.html")
