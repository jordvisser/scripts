#!/usr/bin/env python3

# https://api.9292.nl/0.1/locations?lang=nl-NL&type=station,stop&q=plaszicht
# https://api.9292.nl/0.1/locations/reeuwijk/bushalte-plaszicht/departure-times?lang=nl-NL
import json
import urllib.request
import pprint
pp = pprint.PrettyPrinter(indent=4)

api_url = 'https://api.9292.nl/0.1/'

location_url = api_url + 'locations'
location_arguments = {
    'lang': 'nl-NL',
    'type': 'stop',
    'q': 'plaszicht'
}
request_data = data = urllib.parse.urlencode(location_arguments)
with urllib.request.urlopen(location_url + '?' + request_data) as response:
    response_data = response.read()
    encoding = response.info().get_content_charset('utf-8')

location_data = json.loads(response_data.decode(encoding))
busstop_id = location_data['locations'][0]['id']

departures_url = api_url + 'locations/' + busstop_id + '/departure-times'
departures_arguments = {
    'lang': 'nl-NL'
}
request_data = data = urllib.parse.urlencode(departures_arguments)
with urllib.request.urlopen(departures_url + '?' + request_data) as response:
    response_data = response.read()
    encoding = response.info().get_content_charset('utf-8')

departures_data = json.loads(response_data.decode(encoding))
departures = departures_data['tabs'][0]['departures']
departures_filtered_destination = {k: v for k, v in enumerate(departures) if v['destinationName'] == 'Gouda'}
departures_filtered_time = departures_filtered_destination
pp.pprint(departures_filtered_time)
