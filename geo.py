import requests

APY_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"
def geocode(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": APY_KEY,
        "geocode": address,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    toponym = json_response['response']['GeoObjectCollection']['featureMember']
    return toponym[0]['GeoObject'] if toponym else None

def get_coordinates(address):
    toponym = geocode(address)
    toponym_coordinates = toponym['Point']['pos']
    long, lat = toponym_coordinates.split()
    return float(long), float(lat)

def get_ll_span(address):
    toponym = geocode(address)
    if not toponym:
        return (None, None)

    toponym_coordinates = toponym['Point']['pos']
    long, lat = toponym_coordinates.split()
    ll = ','.join([long, lat])
    env = toponym['boundedBy']['Envelope']
    l, b = env['lowerCorner'].split(" ")
    r, t = env['lowerCorner'].split(" ")
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    span = f"{dx}, {dy}"
    return ll, span