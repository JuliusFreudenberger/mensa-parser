import json
import re
from urllib.request import urlopen, Request

from pyopenmensa.feed import LazyBuilder

from utils import Parser, Canteen

allergens = {
    'Gl-a': 'Weizen',
    'Gl-b': 'Roggen',
    'Gl-c': 'Gerste',
    'Gl-d': 'Hafer',
    'Gl-e': 'Dinkel',
    'Nu-a': 'Mandeln',
    'Ei': 'Eier',
    'Er': 'Erdnüsse',
    'So': 'Soja',
    'Sn': 'Senf',
    'Kr': 'Krebstiere (Krusten- und Schalentiere)',
    'Fi': 'Fisch',
    'ML': 'Milch/Laktose',
    'Se': 'Sellerie',
    'Sf': 'Schwefeldioxid und Sulfite',
    'Sa': 'Sesam',
    'Lu': 'Lupine',
    'We': 'Weichtiere',
    'ALK': 'Alkohol'
}

additives = {
    '1': 'Farbstoff',
    '2': 'Konservierungsstoff',
    '3': 'Nitritpökelsalz',
    '4': 'Antioxidationsmittel',
    '5': 'Geschmacksverstärker',
    '6': 'geschwefelt',
    '7': 'geschwärzt',
    '8': 'gewachst',
    '9': 'Süßungsmittel',
    '10': 'enthält eine Phenylalaninquelle',
    '11': 'Phosphat'
}

legend = {
    'F': 'Fisch', 'G': 'Geflügel', 'K': 'Kalb',
    'L': 'Lamm', 'R': 'Rind', 'S': 'Schwein',
    'W': 'Wild', 'top': 'Empfehlung',
    'V': 'vegetarisch', 'vegan': 'vegan',
}

multiple_whitespaces_regex = re.compile('\\s{2,}')


def get_meal_data(url, today=False):
    canteen = LazyBuilder()
    with urlopen(Request(url, None, {'User-Agent': 'Mozilla/5.0'})) as response:
        data = json.loads(response.read())
    if len(data) == 0:
        return canteen.toXMLFeed()
    canteen_data = data[list(data)[0]]
    menus = canteen_data['menus']
    canteen.name = canteen_data['canteen']
    canteen.setLegendData(legend)

    for menu in menus:
        canteen.addMeal(menu['menuDate'], menu['menuLine'],
                        build_menu_name(menu['menu']) if len(menu['menu']) != 0 else menu['menuLine'],
                        build_allergens_additives(menu['allergens'], menu['additives']),
                        {'student': menu['studentPrice'], 'pupil': menu['pupilPrice'], 'other': menu['guestPrice']})
    return canteen.toXMLFeed()


def build_menu_name(menu):
    output = ', '.join(menu)
    output = multiple_whitespaces_regex.sub(' ', output)
    output = output.replace(' [', '(').replace(']', ')').replace('(vegan)', '')
    return output


def build_allergens_additives(raw_allergens, raw_additives):
    output = [allergens.get(element, element) for element in raw_allergens] + \
             [additives.get(element, element) for element in raw_additives]
    return output


def define_parsers():
    with open('parsers/tuebingen.json') as canteen_file:
        canteen_json = json.load(canteen_file)

    parser = Parser(canteen_json['name'], meal_data_handler=get_meal_data,
                    base_url=canteen_json['base_url'])
    for canteen in canteen_json['canteens']:
        parser.define(Canteen(canteen['id'], canteen['suffix'], canteen['name'], canteen['street'], canteen['city']))
