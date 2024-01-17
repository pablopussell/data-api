# pylint: disable=missing-module-docstring

import sys
import requests

BASE_URI = "https://weather.lewagon.com"
GEO_URI = "/geo/1.0/direct"
FORECAST_URI = "/data/2.5/forecast"

def search_city(query):
    '''
    Look for a given city. If multiple options are returned, have the user choose between them.
    Return one city (or None)
    '''
    params = f"q={query}&limit=5"
    responses = requests.get(BASE_URI+GEO_URI, params = params).json()
    if responses == []:
        return None
    return responses[0]


def weather_forecast(lat, lon):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''

    params = f"lat={lat}&lon={lon}&units=metric"
    response = requests.get(BASE_URI+FORECAST_URI, params= params).json()
    forecast = response.get('list')[::8]

    return forecast


def main():
    '''Ask user for a city and display weather forecast'''
    query = input("City?\n> ")
    cities = search_city(query)
    if cities is None:
        print("CITY NOT FOUND")

    position = 1
    for city_alternatives in cities:
        print(f"{position}. {city_alternatives['name']}, {city_alternatives['country']}")
        position += 1
    choice = int(input("Multiple matches found, which city did you mean?")) - 1
    forecast = weather_forecast(float(cities[choice].get('lat')), float(cities[choice].get('lon')))

    for day in forecast:
        print(f"{day['dt_txt'].split()[0]}: {day['weather'][0]['main']} ({round(day['main']['temp_max'])}ºC)")



    # wanted_city = input()
    # weather = weather_forecast(city.get('latitude'), city.get('longitude'))

    # TODO: Display weather forecast for a given city

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
