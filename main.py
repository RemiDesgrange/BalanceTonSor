import io
import os
from flask import Flask, Response, jsonify, request
from random import randint
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import pyotdr.read as read
from tempfile import NamedTemporaryFile
from typing import BinaryIO, Tuple
from io import BytesIO
import traceback

sentry_sdk.init(integrations=[FlaskIntegration()])
app = Flask('BalanceTonSor')


@app.get('/')
def index_get() -> Response:
    """
    :return Response
    """
    return jsonify({'name': 'BalTanceTonSor blah',
                    'details': 'This little api take sor file as input and return a json. Two endpoints: "/metadata" and "/data_points"'
                   })

def read_sor_file(sor_file_binary: bytes) -> Tuple[str, dict, list]:
    with NamedTemporaryFile('wb') as f:
        f.write(sor_file_binary)
        return read.sorparse(f.name)

@app.post('/data_points')
def data_points() -> Response:
    raw_data = request.get_data()
    if not raw_data:
        raise InvalidUsage('You need to provide a sor file')
    _, _, data_points = read_sor_file(raw_data)
    return jsonify(data_points)

@app.post('/metadata')
def metadata():
    """
    :return Response
    """
    raw_data = request.get_data()
    print("yo")
    if not raw_data:
        raise InvalidUsage('You need to provide a sor file')
    status, results, tracedata = read_sor_file(raw_data)
    return jsonify(results)


class InvalidUsage(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(Exception)
def handle_exception(error):
    response = jsonify({'error': str(error)})
    response.status_code = 500
    return response


if __name__ == '__main__':
    app.run()
