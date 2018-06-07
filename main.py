import io
import os
from flask import Flask, Response, jsonify, request
from random import randint
import pyOTDR.read as read
from raven.contrib.flask import Sentry
from tempfile import NamedTemporaryFile

app = Flask('BalanceTonSor')
Sentry(app)


#UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))

@app.route('/', methods=['GET'])
def index_get():
    """
    :return Response
    """
    return jsonify({'name': 'BalanceTonSor', 
                    'details': 'This little api take sor file as input and return a json'
                   })


@app.route('/', methods=['POST'])
def index_post():
    """
    :return Response
    """ 
    raw_data = request.get_data()
    if not raw_data:
        raise InvalidUsage('You need to provide a sor file')
    # the lib kind of sucks in file mgmt, so writing the file to disk (tmp)  
    with NamedTemporaryFile('wb') as f:
        f.write(raw_data)
        status, results, tracedata = read.sorparse(f.name)
        if status != 'ok':
            raise InvalidUsage('There where an error in the processing', status_code=500)
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
