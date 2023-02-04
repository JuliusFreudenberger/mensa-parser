from pyopenmensa.feed import LazyBuilder, Feed

parser_list = {}


class Canteen:
    canteen_id: str
    suffix: str
    name: str
    street: str
    zip_code: str
    city: str
    public: bool
    source: str

    def __init__(self, canteen_id, suffix, name, street, zip_code, city, public, source):
        self.canteen_id = canteen_id
        self.suffix = suffix
        self.name = name
        self.street = street
        self.zip_code = zip_code
        self.city = city
        self.public = public
        self.source = source

    def address(self):
        return f'{self.street}, {self.zip_code} {self.city}'


class Parser:
    canteens: dict[str, Canteen] = {}

    def __init__(self, name, meal_data_handler, base_url: str):
        self.name = name
        self.meal_data_handler = meal_data_handler
        self.base_url = base_url
        parser_list[name] = self

    def define(self, canteen: Canteen):
        self.canteens[canteen.canteen_id] = canteen

    def get_meal_data(self, canteen: str):
        return self.meal_data_handler(self.base_url + self.canteens[canteen].suffix)

    def get_meta_data(self, canteen: str, prefix: str):
        canteen = self.canteens[canteen]
        meta_data = LazyBuilder()
        meta_data.name = canteen.name
        meta_data.address = canteen.address()
        meta_data.city = canteen.city
        meta_data.availability = 'public' if canteen.public else 'restricted'
        meta_data.feeds.append(
            Feed('full', priority='0', url=f'{prefix}/{canteen.canteen_id}.xml', source=canteen.source, dayOfWeek='*', dayOfMonth='*',
                 hour='9', minute='30', retry='60 1 1440'))
        return meta_data.toXMLFeed()

    def get_canteen_index(self, prefix: str):
        index: dict[str, str] = {}
        canteen: Canteen
        for canteen in self.canteens.values():
            index[canteen.canteen_id] = f'{prefix}/{canteen.canteen_id}.xml'
        return index


def get_parser(parser_name: str) -> Parser:
    return parser_list[parser_name]
