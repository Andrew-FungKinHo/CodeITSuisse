import logging
import json
import math
from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def getItemSmallest(item,number_of_salads):
  itemSmallest = math.inf
  startingPoint = 0
  for _ in range(len(item) - number_of_salads + 1):
    sublist = item[startingPoint:startingPoint + number_of_salads]
    if 'X' not in sublist:
      sublist = list(map(int, sublist)) 
      if sum(sublist) < itemSmallest and sum(sublist)>0:
        itemSmallest = sum(sublist)
      else:
        continue
    startingPoint += 1

  return itemSmallest

@app.route('/salad-spree', methods=['POST'])
def saladSpree():
    data = request.get_json()
    listSmallest = math.inf
    for j in range(len(data['salad_prices_street_map'])):
        smallest = getItemSmallest(data['salad_prices_street_map'][j],data['number_of_salads'])
        if smallest < listSmallest and smallest > 0:
            listSmallest = smallest
    if listSmallest == math.inf:
        # print(0)
        output = {'result': 0}
    else:
        # print(listSmallest)
        output =  {'result': listSmallest}
        
    return jsonify(output)



