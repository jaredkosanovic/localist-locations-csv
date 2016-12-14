FROM python:2-onbuild

CMD [ "python", "./get_locations_csv.py"]

USER nobody:nogroup
