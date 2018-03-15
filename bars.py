import json
from math import radians, cos, sin, asin, sqrt


def get_dict_bars(bars_json):
    try:
        bars_dict = load_data(bars_json)
    except FileNotFoundError:
        print('Ошибка! Система не нашла такой файл.')
        print('Пробуйте указать полный путь к файлу.')
    except ValueError:
        print('Ошибка. Файл должен быть в формате JSON.')
    else:
        return bars_dict['features']


def load_data(filepath):
    with open(filepath, 'r', encoding="utf8") as bars_file:
        return json.load(bars_file)


def get_biggest_bar(bars_info):
    biggest_bar = max(bars_info, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])
    return biggest_bar


def get_smallest_bar(bars_info):
    smallest_bar = min(bars_info, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])
    return smallest_bar


def get_user_location(coordinates):
    user_coordinates = float(input('{} на которой вы находитесь:'.format(coordinates)))
    return user_coordinates


def check_user_location(user_location, type_location):
    if type(user_location) is float:
        return True
    else:
        print('{} введена не верно. '
              'Вводите только цифры. '
              'Напр: "55.9862994"'.format(type_location))
        exit()


def get_closest_bar(bars_info, user_lon, user_lat):
    bars_distance = {}
    for bar in bars_info:
        bar_lon = bar['geometry']['coordinates'][1]
        bar_lat = bar['geometry']['coordinates'][0]
        bar_distance = calculates_distance(user_lon,
                                           user_lat,
                                           bar_lon,
                                           bar_lat)
        bars_distance[bar['properties']['Attributes']['Name']] = bar_distance

    closest_bar = min(bars_distance.items(), key=lambda bar: bar[1])

    return closest_bar[0]


def calculates_distance(lon1, lat1, lon2, lat2):

    """
    Функция считает растояние в КМ между двумя GPS точками.
    Координаты должны быть во float.
    """

    lon1, lat1, lon2, lat2 = map(radians, (lon1, lat1, lon2, lat2))
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


if __name__ == '__main__':
    bars_data_file = input('Напишите путь к файлу c данными о барах: \n'
                           'Скачать его можно по ссылке data.mos.ru/opendata/7710881420-bary \n')
    bars_data = get_dict_bars(bars_data_file)

    name_biggest_bar = get_biggest_bar(bars_data)['properties']['Attributes']['Name']
    print('Самый большой бар — {}'.format(name_biggest_bar))

    name_smallest_bar = get_smallest_bar(bars_data)['properties']['Attributes']['Name']
    print('Самый маленький бар — {}'.format(name_smallest_bar))

    print('\nСейчас я найду ближайший к вам бар')
    longitude, latitude = get_user_location('Широта'), get_user_location('Высота')
    check_user_location(longitude, 'Широта')
    check_user_location(latitude, 'Высота')
    print('Ближайший бар — {}'.format(get_closest_bar(bars_data, longitude, latitude)))
