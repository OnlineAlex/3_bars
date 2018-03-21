import sys
import json
from math import radians, cos, sin, asin, sqrt
from json.decoder import JSONDecodeError


def load_data(filepath):
    with open(filepath, 'r', encoding='utf8') as bars_file:
        return json.load(bars_file)['features']


def get_biggest_bar(bars_info):
    biggest_bar = max(
        bars_info,
        key=lambda bar: bar['properties']['Attributes']['SeatsCount']
    )

    return biggest_bar


def get_smallest_bar(bars_info):
    smallest_bar = min(
        bars_info,
        key=lambda bar: bar['properties']['Attributes']['SeatsCount']
    )

    return smallest_bar


def get_user_location():
    longitude = float(input('Введите широту на которой вы находитесь:'))
    latitude = float(input('Введите долготу на которой вы находитесь:'))
    return longitude, latitude


def print_info_bars(bar, type_info):
    bar_name = bar['properties']['Attributes']['Name']
    print('Самый {} бар — {}'.format(type_info, bar_name))


def get_closest_bar(bars_info, user_lon, user_lat):
    closest_bar = min(
        bars_info,
        key=lambda bar: calculates_distance(
            user_lon,
            user_lat,
            bar['geometry']['coordinates'][1],
            bar['geometry']['coordinates'][0]
        )
    )

    return closest_bar


def calculates_distance(lon1, lat1, lon2, lat2):

    """
    Функция считает растояние в КМ между двумя GPS точками.
    Координаты должны быть во float.
    Формула https://en.wikipedia.org/wiki/Haversine_formula
    """

    earth_radius = 6371
    lon1, lat1, lon2, lat2 = map(
        radians,
        (lon1, lat1, lon2, lat2)
    )

    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = earth_radius * c
    return km


if __name__ == '__main__':

    try:
        bars_data = load_data(sys.argv[1])
        user_longitude, user_latitude = get_user_location()
    except (FileNotFoundError, IndexError):
        exit('Файл не найден.'
             'Попробуйте ввести python bars.py <путь к списку московских баров>')
    except (UnicodeDecodeError, JSONDecodeError):
        exit('Ошибка. Файл должен быть в формате .JSON')
    except ValueError:
        exit('Координты введены не верно.'
             'Пишите только цифры. Напр: "55.9862994"')

    print_info_bars(get_biggest_bar(bars_data), 'большой')
    print_info_bars(get_smallest_bar(bars_data), 'маленький')

    user_closest_bar = get_closest_bar(
        bars_data,
        user_longitude,
        user_latitude
    )
    print_info_bars(user_closest_bar, 'ближайший')

