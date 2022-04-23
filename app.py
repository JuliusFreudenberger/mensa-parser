from flask import Flask, abort

import parsers
import utils

app = Flask(__name__)

parsers.define_parsers()


@app.route('/mensa/<parser_name>/<mensa_name>')
def mensa(parser_name, mensa_name):
    try:
        return utils.get_parser(parser_name).parse(mensa_name)
    except KeyError:
        abort(404)

