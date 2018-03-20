import sys
import json
from math import radians, cos, sin, asin, sqrt
from json.decoder import JSONDecodeError


def get_error_report(name_error):
    errors_reports = {
        ValueError: 'Координты введены не верно.'
                    'Пишите только цифры. Напр: "55.9862994"',
        IndexError: 'Укажите путь к файлу',
        FileNotFoundError: 'Файл не найден',
        JSONDecodeError: 'Ошибка. Файл должен быть в формате .JSON',
        UnicodeDecodeError: 'Ошибка кодировки. Требуется UTF-8'
    }
    return errors_reports[name_error]


def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf8') as bars_file:
            return json.load(bars_file)['features']
    except FileNotFoundError:
        return FileNotFoundError
    except (JSONDecodeError, UnicodeDecodeError) as coding_error:
        return type(coding_error)


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
    longitude = float(input('Широта на которой вы находитесь:'))
    latitude = float(input('Долгота на которой вы находитесь:'))
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
    if len(sys.argv) < 2:
        exit(get_error_report(IndexError))
    user_filepath = sys.argv[1]

    bars_data = load_data(user_filepath)
    if bars_data:
        exit(get_error_report(bars_data))

    print_info_bars(get_biggest_bar(bars_data), 'большой')
    print_info_bars(get_smallest_bar(bars_data), 'маленький')

    try:
        user_longitude, user_latitude = get_user_location()
    except ValueError:
        exit(get_error_report(ValueError))

    user_closest_bar = get_closest_bar(
        bars_data,
        user_longitude,
        user_latitude
    )
    print_info_bars(user_closest_bar, 'ближайший')
