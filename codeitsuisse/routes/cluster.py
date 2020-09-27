import logging
import json
import numpy as np
from collections import deque

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

# Below lists details all 8 possible movements from a cell
# (top, right, bottom, left and 4 diagonal moves)
row = [-1, -1, -1, 0, 1, 0, 1, 1]
col = [-1, 1, 0, -1, -1, 1, 0, 1]


# Function to check if it is safe to go to position (x, y)
# from current position. The function returns false if x, y:
# is not valid matrix coordinates or (x, y) represents water or
# position (x, y) is already processed
def isSafe(mat, x, y, processed):
  return (x >= 0) and (x < len(processed)) and \
       (y >= 0) and (y < len(processed[0])) and \
       (mat[x][y] == '1' and not processed[x][y])

def BFS(mat, processed, i, j):

  # create an empty queue and enqueue source node
  q = deque()
  q.append((i, j))

  # mark source node as processed
  processed[i][j] = True

  # loop till queue is empty
  while q:

    # pop front node from queue and process it
    x, y = q.popleft()

    # check for all 8 possible movements from current cell
    # and enqueue each valid movement
    for k in range(8):
      # Skip if location is invalid or already processed or has water
      if isSafe(mat, x + row[k], y + col[k], processed):
        # skip if location is invalid or it is already
        # processed or consists of water
        processed[x + row[k]][y + col[k]] = True
        q.append((x + row[k], y + col[k]))

def infect(row,col,matrix,row_dimension,col_dimension):
  # infect this point
  matrix[row,col] = '1'

  # left item
  if col - 1 >= 0:
    if matrix.item(row,col-1) == '0':
      infect(row,col-1,matrix,row_dimension,col_dimension)
  # right item
  if col + 1 <= col_dimension:
    if matrix.item(row,col+1) == '0':
      infect(row ,col+1,matrix,row_dimension,col_dimension)

  # a row above
  if row - 1 >= 0:
    if matrix.item(row-1,col) == '0':
      infect(row - 1 ,col,matrix,row_dimension,col_dimension)

    if col - 1 >= 0:
      if matrix.item(row-1,col-1) == '0':
        infect(row - 1 ,col-1,matrix,row_dimension,col_dimension)
    
    if col + 1 <= col_dimension:
      if matrix.item(row-1,col+1) == '0':
        infect(row - 1 ,col+1,matrix,row_dimension,col_dimension)

  # a row below
  if row + 1 <= row_dimension:
    if matrix.item(row+1,col) == '0':
      infect(row+1,col,matrix,row_dimension,col_dimension)

    if col - 1 >= 0:
      if matrix.item(row+1,col-1) == '0':
        infect(row+1,col-1,matrix,row_dimension,col_dimension)
    
    if col + 1 <= col_dimension:
      if matrix.item(row+1,col+1) == '0':
        infect(row+1,col+1,matrix,row_dimension,col_dimension)

  return matrix


@app.route('/cluster', methods=['POST'])
def findCluster():
    data = request.get_json()
    matrix = np.array(data)
    
    infectedList = list(zip(*np.where(matrix == '1')))

    for i in range(len(infectedList)):
      infect(infectedList[i][0],infectedList[i][1],matrix,len(data) - 1, len(data[0]) - 1)

    (M, N) = (len(matrix), len(matrix[0]))

    # stores if cell is processed or not
    processed = [[False for x in range(N)] for y in range(M)]

    island = 0
    for i in range(M):
      for j in range(N):
        # start BFS from each unprocessed node and increment island count
        if matrix[i][j] == '1' and not processed[i][j]:
          BFS(matrix, processed, i, j)
          island = island + 1

    output = {"answer": island}
    return jsonify(output)



