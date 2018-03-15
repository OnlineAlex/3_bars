import sys
import json
from math import radians, cos, sin, asin, sqrt


def load_data(filepath):
    with open(filepath, 'r', encoding='utf8') as bars_file:
        return json.load(bars_file)['features']


def get_biggest_bar(bars_info):
    biggest_bar = max(bars_info,
                      key=lambda bar: bar['properties']
                                         ['Attributes']
                                         ['SeatsCount'])

    return biggest_bar['properties']['Attributes']['Name']


def get_smallest_bar(bars_info):
    smallest_bar = min(bars_info,
                       key=lambda bar: bar['properties']
                                          ['Attributes']
                                          ['SeatsCount'])

    return smallest_bar['properties']['Attributes']['Name']


def get_closest_bar(bars_info, user_lon, user_lat):
    closest_bar = min(bars_info,
                      key=lambda bar: calculates_distance(user_lon,
                                                          user_lat,
                                                          bar['geometry']['coordinates'][1],
                                                          bar['geometry']['coordinates'][0]))

    return closest_bar['properties']['Attributes']['Name']


def calculates_distance(lon1, lat1, lon2, lat2):

    """
    Функция считает растояние в КМ между двумя GPS точками.
    Координаты должны быть во float.
    Формула https://en.wikipedia.org/wiki/Haversine_formula
    """

    earth_radius = 6371
    lon1, lat1, lon2, lat2 = map(radians, (lon1,
                                           lat1,
                                           lon2,
                                           lat2))
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    a = sin(d_lat / 2) ** 2 + \
        cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = earth_radius * c
    return km


if __name__ == '__main__':
    try:
        bars_data_file = sys.argv[1]
        bars_data = load_data(bars_data_file)
    except IndexError:
        print('Ошибка! Вы не указали путь к файлу JSON.')
        print('Сработает, если написать "python bars.py <путь к файлу>"')
    except FileNotFoundError:
        print('Ошибка! Система не нашла такой файл.')
        print('Пробуйте указать полный путь к файлу.')
    except ValueError:
        print('Ошибка. Файл должен быть в формате JSON.')
    else:
        print('Самый большой бар — {}'.format(get_biggest_bar(bars_data)))
        print('Самый маленький бар — {}'.format(get_smallest_bar(bars_data)))

        print('\nСейчас я найду ближайший к вам бар')
        try:
            longitude = float(input('Широта на которой вы находитесь:'))
            latitude = float(input('Долгота на которой вы находитесь:'))
        except ValueError:
            print('Координты введены не верно. Пишите только цифры.'
                  'Напр: "55.9862994"')
        else:
            print('Ближайший бар — {}'.format(get_closest_bar(bars_data,
                                                              longitude,
                                                              latitude)))
