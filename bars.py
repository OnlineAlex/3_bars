import json
from math import radians, cos, sin, asin, sqrt


bars_info_json = 'bars.json'


def load_data(filepath):
    with open(filepath, 'r', encoding="utf8") as bars_info:
        return json.load(bars_info)


def sort_size_bar(json_str):
    # Сортируем бары по колличеству мест
    bars_size = {}

    for bar_id in json_str['features']:
        bars_size[bar_id['properties']['Attributes']['Name']] = bar_id['properties']['Attributes']['SeatsCount']

    bars_size = sorted(bars_size.items(), key=lambda seats_count: seats_count[1])
    return bars_size


def get_biggest_bar(bars_info):
    sorted_bars = sort_size_bar(bars_info)
    biggest_bar = sorted_bars[-1][0]
    return "Самый большой бар — " + biggest_bar


def get_smallest_bar(bars_info):
    sorted_bars = sort_size_bar(bars_info)
    smallest_bar = sorted_bars[0][0]
    return "Самый маленький бар — " + smallest_bar


def get_user_location(coordinates):
    while True:
        try:
            user_coordinates = float(input(coordinates + ' на которой вы находитесь:'))
        except ValueError:
            print('Ошибка значения. ' + coordinates + 'введена не верно. Вводите только цифры. Напр: "55.9862994"')
        else:
            return user_coordinates


def get_closest_bar(json_str, user_lon, user_lat):
    min_distance = calculates_distance(user_lon, user_lat,
                                       json_str['features'][0]['geometry']['coordinates'][1],
                                       json_str['features'][0]['geometry']['coordinates'][0])
    closest_bar = json_str['features'][0]['properties']['Attributes']['Name']

    for bar in json_str['features']:
        bar_lon = bar['geometry']['coordinates'][1]
        bar_lat = bar['geometry']['coordinates'][0]
        bar_distance = calculates_distance(user_lon, user_lat, bar_lon, bar_lat)
        if bar_distance < min_distance:
            min_distance = bar_distance
            closest_bar = bar['properties']['Attributes']['Name']

    return closest_bar


def calculates_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, (lon1, lat1, lon2, lat2))
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


if __name__ == '__main__':
    bars_info_str = load_data(bars_info_json)
    print(get_biggest_bar(bars_info_str))
    print(get_smallest_bar(bars_info_str))
    print('\nСейчас я найду ближайший к вам бар')
    longitude, latitude = get_user_location('Широта'), get_user_location('Высота')
    print('Ближайший бар — ' + get_closest_bar(bars_info_str, longitude, latitude))