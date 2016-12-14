import json, requests, ssl, csv, re, time
from config import *

def get_locations():
    access_token_url = locations_url + "/token"
    post_data = {'client_id': client_id, 
        'client_secret': client_secret, 
        'grant_type': 'client_credentials'}
    token_request = requests.post(access_token_url, data=post_data)
    token_response = token_request.json()
    access_token = 'Bearer ' + token_response["access_token"]
    
    headers = {'Authorization': access_token}
    query_params = {'campus': 'corvallis', 'type':'building', 'page[size]': 9999}
    locations_request = requests.get(locations_url, headers=headers, params=query_params)
    return locations_request.json()

locations_response = get_locations()

locations_csv = csv.writer(open("osu-corvallis-locations-" + time.strftime("%m-%d-%Y") + ".csv", "w"))
locations_csv.writerow(['Name', 'Description', 
    'Type', 'URL', 'Address', 'City', 'State', 
    'Photo URL', 'Longitude', 'Latitude'])

for location in locations_response['data']:
    attributes = location['attributes']
    print attributes
    # Strip summary text of HTML tags
    if attributes['summary'] is not None:
        summary = re.sub("<.*?>", "", attributes['summary'].encode('utf-8').strip())
    else:
        summary = None
    print summary
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
