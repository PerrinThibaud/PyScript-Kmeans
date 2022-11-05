import random
from pathlib import Path

import flask

app = flask.Flask(__name__)


@app.get('/')
def index():
    return flask.render_template('index.html')


# @app.get('/serviceWorker.js')
# def worker():
#     js = Path(__file__).parent / 'static' / 'js' / 'serviceWorker.js'
#     text = js.read_text()
#     resp = flask.make_response(text)
#     resp.content_type = 'application/javascript'
#     resp.headers['Service-Worker-Allowed'] = '/'

#     return resp
