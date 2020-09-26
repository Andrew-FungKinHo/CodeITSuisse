import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

# @app.route('/square', methods=['POST'])
# def evaluate():
#     data = request.get_json()
#     logging.info("data sent for evaluation {}".format(data))
#     # logging.info(f"request {request}")

#     name = data['name']
#     location = data['location']

#     randomlist = data['randomlist']


#     # logging.info("My result :{}".format(result))
#     return jsonify({'result': 'Success!', 'name': name, 'location': location, 'randomkeyinlist': randomlist[1]})
#     # json.dumps(result)



