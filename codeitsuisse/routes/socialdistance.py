import logging
import json
from scipy.special import comb
from flask import request, jsonify


from codeitsuisse import app

logger = logging.getLogger(__name__)


def ways_of_sitting(seats, people, space):
    # Minimum seats: PSPSP...
    min_seats = people + space * (people-1)
    if seats >= min_seats:
        # How many slots we can stuff empty seats in (value of n)
        # One slot is before the first person (on the left)
        # For every person we add, we add a slot (on the right of the person)
        slots = 1 + people
        # How many we need to choose (value of r)
        choose = seats - min_seats
        # Number of combinations with replacement is nCr(n+r-1, r)
        #return nCr(slots + choose - 1, choose)
        return comb(slots + choose - 1, choose, exact=True)
    else:
        return 0

@app.route('/social_distancing', methods=['POST'])
def social_distancing():
    data = request.get_json()
    print(data)
    answers = {}
    for key, value in data['tests'].items():
        answers[key] = ways_of_sitting(value['seats'],value['people'],value['spaces'])
    solution = {'answers': answers}
    return jsonify(solution)
