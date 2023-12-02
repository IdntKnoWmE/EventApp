import json

from rest_framework.exceptions import ValidationError


def get_cities():
    cities_data_file = 'staticfiles/cities.json'
    cities = []
    with open(cities_data_file, 'r') as cities_data:
        json_data = json.load(cities_data)
        for city_instance in json_data:
            cities.append(city_instance.get('city'))
    return cities


def validate_interval(value):
    if value < 0 or value > 10:
        raise ValidationError(f'Rating value must be in the range [0, 10]')
