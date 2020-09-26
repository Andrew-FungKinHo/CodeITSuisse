import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def ways_of_sitting(seats, people, space):
  if seats <= 0:
      return 0
  elif people == 1:
      # One person left. The person can sit on any seats.
      return seats
  elif people + space * (people-1) > seats:
      # Not enough space
      return 0

  count = 0
  for i in range(seats):
      # -1 since this passenger already took a seat
      # -space since the the next passenger must maintain social distance
      # -i is to iterate through the possible seats
      count += ways_of_sitting(seats - 1 - space - i, people - 1, space)
  return count

# @app.route('/social_distancing', methods=['POST'])
# def geometry():
#     data = request.get_json()
#     output = {"answers": }
#     output.append({"x": x, "y": y})
#     return jsonify(output)



