parser_list = {}


class Parser:
    sources = {}

    def __init__(self, name, handler, shared_prefix: str):
        self.name = name
        self.handler = handler
        self.shared_prefix = shared_prefix
        parser_list[name] = self

    def define(self, name: str, suffix: str):
        self.sources[name] = suffix

    def parse(self, source: str):
        return self.handler(self.shared_prefix + self.sources[source])


def get_parser(parser_name: str) -> Parser:
    return parser_list[parser_name]
