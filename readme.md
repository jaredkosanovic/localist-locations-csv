# Localist Locations CSV Generator

Localist allows manually importing a CSV of locations. This generator get's locations from the [locations api](https://github.com/osu-mist/locations-api) and adds them to a csv file able to uploaded directly to Localist.

## Generate a CSV

1. Save [config_example.py](config_example.py) as config.py and modify the contents as appropriate.
2. Build the Docker image
`docker build -t localist-csv .`
3. Run the Docker image
`docker run --rm -v /path/to/localist-locations-csv/:/usr/src/app/ localist-csv`
4. A csv will appear in /path/to/localist-locations-csv/
