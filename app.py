import os

from flask import Flask, abort

import parsers
import utils

app = Flask(__name__)

parsers.define_parsers()

VIRTUAL_HOST = os.getenv('VIRTUAL_HOST')


@app.route('/mensa/<parser_name>.json')
def index(parser_name):
    try:
        return utils.get_parser(parser_name).get_canteen_index(f'https://{VIRTUAL_HOST}/mensa/{parser_name}/meta')
    except KeyError:
        abort(404)


@app.route('/mensa/<parser_name>/meta/<canteen_name>.xml')
def meta(parser_name, canteen_name):
    try:
        return utils.get_parser(parser_name).get_meta_data(canteen_name, f'https://{VIRTUAL_HOST}/mensa/{parser_name}/feed')
    except KeyError:
        abort(404)


@app.route('/mensa/<parser_name>/feed/<canteen_name>.xml')
def mensa(parser_name, canteen_name):
    try:
        return utils.get_parser(parser_name).get_meal_data(canteen_name)
    except KeyError:
        abort(404)
