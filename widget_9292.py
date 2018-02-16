#!/usr/bin/env python3

# https://api.9292.nl/0.1/locations?lang=nl-NL&type=station,stop&q=plaszicht
# https://api.9292.nl/0.1/locations/reeuwijk/bushalte-plaszicht/departure-times?lang=nl-NL
import json
import urllib.request
import datetime as dt
import pprint
now = dt.datetime.now()
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
departures_filtered_destination = [v for v in departures if v['destinationName'] == 'Gouda']
departures_list = departures_filtered_destination[0:2]

for depa in departures_list:
    dTime = dt.datetime.strptime('{} {}'.format(now.strftime('%Y-%m-%d'), depa['time']),'%Y-%m-%d %H:%M')
    if dTime < now:
        dTime = dTime + dt.timedelta(days=1)
    if depa['realtimeState'] == 'late':
        minutes = depa['realtimeText'].split(' ')[0]
        dTime = dTime + dt.timedelta(seconds=int(minutes)*60)
    deltaNow = dTime - now
    pp.pprint(dTime)
    pp.pprint(divmod(deltaNow.days * 86400 + deltaNow.seconds, 60))

pp.pprint(departures_list)
