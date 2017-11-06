import requests
import csv
import re
import sys
from config import locations_url, token_api, client_id, client_secret

def get_access_token():
    post_data = {'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'}
    token_request = requests.post(token_api, data=post_data)

    if token_request.status_code != 200:
        print "Token request failed."
        sys.exit(1)

    token_response = token_request.json()

    return 'Bearer ' + token_response["access_token"]

def get_locations(access_token, campus):
    headers = {'Authorization': access_token}
    query_params = {'campus': campus, 'type':'building', 'page[size]': 9999}
    locations_request = requests.get(locations_url, headers=headers, params=query_params)

    if locations_request.status_code != 200:
        print "Locations request failed."
        sys.exit(1)

    return locations_request.json()

def is_valid_name(name):
    invalid_names = ['garage', 'shed', '-', 'storage', 'feed']

    for invalid_name in invalid_names:
        if invalid_name in name.lower():
            return False
    return True

# Get access token
access_token = get_access_token()
campuses = ['corvallis', 'cascades', 'hmsc', 'other']
ignored_buildings = []

for campus in campuses:
    print "------------------------------------------------------"
    print "Campus: %s" % campus
    locations_response = get_locations(access_token, campus)

    # Initialize a CSV with the needed fields
    try:
        locations_csv = csv.writer(open("osu-%s-locations.csv" % campus, "w"))
        locations_csv.writerow(['Name', 'Description',
            'Type', 'URL', 'Address', 'City', 'State', 'Zip',
            'Photo URL', 'Longitude', 'Latitude'])
    except IOError:
        print "Cannot write to a CSV file"
        sys.exit(1)

    for location in locations_response['data']:
        attributes = location['attributes']
        name = attributes['name']
        print "Processing " + name

        if (is_valid_name(name)):
            # Strip description text of HTML tags
            if attributes['description'] is not None:
                description = re.sub("<.*?>", "", attributes['description'].encode('utf-8').strip())
            else:
                description = None

            # Images are nicer than thumbnails
            if attributes['images']:
                image = attributes['images'][0]
            elif attributes['thumbnails']:
                image = attributes['thumbnails'][0]
            else:
                image = None

            locations_csv.writerow([
                name,
                description,
                attributes['type'],
                attributes['website'],
                attributes['address'],
                attributes['city'],
                attributes['state'],
                attributes['zip'],
                image,
                attributes['longitude'],
                attributes['latitude']])
        else:
            ignored_buildings.append(name)

print "These buildings were ignored:"
print '%s' % ', '.join(map(str, ignored_buildings))
