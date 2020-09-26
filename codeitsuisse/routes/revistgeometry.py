import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def get_line_eq(p1, p2):
    # Output: (a, b, c), where the line equation is ax+by=c
    if p1["x"] == p2["x"]:
        # Vertical line
        return (1, 0, p1["x"])
    elif p1["y"] == p2["y"]:
        # Horizontal line
        return (0, 1, p1["y"])
    else:
        # Normal condition
        m = (p1["y"] - p2["y"]) / (p1["x"] - p2["x"])
        return (m, -1, m*p1["x"] - p1["y"])

@app.route('/revisitgeometry', methods=['POST'])
def geometry():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    shapeCoordinates = data.get("shapeCoordinates") 
    lineCoordinates = data.get("lineCoordinates")

    # Equation of input line
    a, b, c, = get_line_eq(lineCoordinates[0], lineCoordinates[1])

    output = []
    sides = len(shapeCoordinates)
    for i in range(sides):
        p1 = shapeCoordinates[i]
        p2 = shapeCoordinates[(i+1)%sides]
        d, e, f = get_line_eq(p1, p2)

        # According to Wolfram Alpha, given the lines ax+by=c and dx+ey=f, the
        # intersection is x=(ce-bf)/(ae-bd) and y=(af-cd)/(ae-bd).
        # We store ae-bd as det (determinant).
        det = a*e - b*d
        if det == 0:
            # Parallel lines
            continue

        # Intersection
        x = round((c*e - b*f) / det, 2)
        y = round((a*f - c*d) / det, 2)
        # Does it lie on the line segment?
        if min(p1["x"], p2["x"]) <= x <= max(p1["x"], p2["x"]) and \
            min(p1["y"], p2["y"]) <= y <= max(p1["y"], p2["y"]):
            output.append({"x": x, "y": y})

    logging.info("My result :{}".format(output))
    return json.dumps(result)



