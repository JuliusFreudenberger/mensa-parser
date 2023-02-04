parser_list = {}


class Canteen:
    canteen_id: str
    suffix: str
    name: str
    street: str
    city: str

    def __init__(self, canteen_id, suffix, name, street, city):
        self.canteen_id = canteen_id
        self.suffix = suffix
        self.name = name
        self.street = street
        self.city = city

    def address(self):
        return f'{self.street}, {self.city}'


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

    def get_canteen_index(self, prefix: str):
        index: dict[str, str] = {}
        canteen: Canteen
        for canteen in self.canteens.values():
            index[canteen.canteen_id] = f'{prefix}/{canteen.canteen_id}.xml'
        return index


def get_parser(parser_name: str) -> Parser:
    return parser_list[parser_name]
