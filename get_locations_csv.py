import json, requests, ssl, csv, re, time
from config import *

locations_request = requests.get(locations_url, verify=False, auth=(user, password))
response = locations_request.json()

locations_csv = csv.writer(open("osu-corvallis-locations-" + time.strftime("%m-%d-%Y") + ".csv", "wb+"))
locations_csv.writerow(['Name', 'Description', 
    'Type', 'URL', 'Address', 'City', 'State', 
    'Photo URL', 'Longitude', 'Latitude'])

for location in response['data']:
    attributes = location['attributes']

    # Strip summary text of HTML tags
    if attributes['summary'] is not None:
        summary = re.sub("<.*?>", "", attributes['summary'].encode('utf-8').strip())
    else:
        summary = None

    # Images are nicer than thumbnails.  
    if attributes['images']:
        image = attributes['images'][0] 
    elif attributes['thumbnails']:
        image = attributes['thumbnails'][0]
    else:
        image = None

    locations_csv.writerow([
        attributes['name'],
        summary,
        attributes['type'],
        attributes['website'],
        attributes['address'],
        attributes['city'],
        attributes['state'],
        image,
        attributes['longitude'],
        attributes['latitude']])
