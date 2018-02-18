#!/usr/bin/env python3

# https://api.9292.nl/0.1/locations?lang=nl-NL&type=station,stop&q=plaszicht
# https://api.9292.nl/0.1/locations/reeuwijk/bushalte-plaszicht/departure-times?lang=nl-NL
import sys
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
departures_list = departures_filtered_destination #[0:2]

departures_output = []

for depa in departures_list:
    dTime = dt.datetime.strptime('{} {}'.format(now.strftime('%Y-%m-%d'), depa['time']),'%Y-%m-%d %H:%M')
    if dTime < now:
        dTime = dTime + dt.timedelta(days=1)
    if depa['realtimeState'] == 'ontime':
        depText = 'op tijd'
        #sys.stdout.write("\033[1;32m")
    elif depa['realtimeState'] == 'late':
        minutes = int(depa['realtimeText'].split(' ')[0])
        dTime = dTime + dt.timedelta(seconds=minutes*60)
        depText = '{} minuten vertraagd'.format(minutes)
        #sys.stdout.write("\033[1;31m")
    else:
        minutes = int(depa['realtimeText'].split(' ')[0])
        depText = '-- {} || {} min. --'.format(depa['realtimeState'], minutes)
        #sys.stdout.write("\033[38;5;208m")

    deltaNow = dTime - now
    deltaCalc = divmod(deltaNow.days * 86400 + deltaNow.seconds, 60)
    #sys.stdout.write("\033[1m")
    if deltaCalc[0] < 70:
        departures_output.append('Bus {} is {} en vertrekt over {} minuten om {}.'.format(depa['service'],depText,deltaCalc[0],dTime.strftime('%H:%M')))
    else:
        #sys.stdout.write("\033[0m")
        break

if len(departures_output) == 0:
    print('Er vertrekken geen bussen het komende uur.')
else:
    for depout in departures_output:
        print(depout)

pp.pprint(departures_list)
