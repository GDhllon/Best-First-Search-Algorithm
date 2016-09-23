from __future__ import print_function
from copy import copy, deepcopy
from SearchProblem import *
import sys

def check_moves ( self, vehicle ):#check moves at edge and return them
  moves = []
  
  if (vehicle.direction == "H"):#vehicle is horizontal
    if (vehicle.size > 2):#vehicle is a truck
      if( vehicle.xcor+3 < 6 ):
        if self.state[vehicle.xcor+3][vehicle.ycor] == "-" :
          moves.append(vehicle.name + "R")
      if( vehicle.xcor-1 > -1 ):
        if self.state[vehicle.xcor-1][vehicle.ycor] == "-" :
          moves.append(vehicle.name + "L")
    else :#vehicle is a car
      if( vehicle.xcor+2 < 6 ):
        if self.state[vehicle.xcor+2][vehicle.ycor] == "-" :
          moves.append(vehicle.name + "R")
      if( vehicle.xcor-1 > -1 ):
        if self.state[vehicle.xcor-1][vehicle.ycor] == "-" :
          moves.append(vehicle.name + "L")
  else :#vehicle is vertical
    if (vehicle.size > 2):#vehicle is a truck
      if( vehicle.ycor+3 < 6 ):
        if self.state[vehicle.xcor][vehicle.ycor+3] == "-" :
          moves.append(vehicle.name + "D")
      if( vehicle.ycor-1 > -1 ):
        if self.state[vehicle.xcor][vehicle.ycor-1] == "-" :
          moves.append(vehicle.name + "U")
    else :#vehicle is a car
      if( vehicle.ycor+2 < 6 ):
        if self.state[vehicle.xcor][vehicle.ycor+2] == "-" :
          moves.append(vehicle.name + "D")
      if( vehicle.ycor-1 > -1 ):
        if self.state[vehicle.xcor][vehicle.ycor-1] == "-" :
          moves.append(vehicle.name + "U")
  
  return moves

class Vehicle:
    def __init__( self, name, xcor, ycor, direction, size ):
      self.name = name
      self.xcor = int(xcor)
      self.ycor = int(ycor)
      self.direction = direction
      self.size = size

class RushHour (SearchProblem):
  def __init__( self, state, vehicleList, root=False ):
    self.state = deepcopy(state)
    self.vehicleList = deepcopy(vehicleList)
    self.path = ""
    
    if root:
      self.visited = []
  def __repr__( self ):
    string = ""
    for y in range(0,6):
      for x in range(0,6):
        string = string + self.state[x][y]
    print(string)
    return string

  def edges( self ):
    my_edges = []
    num = -1
    for vehicle in self.vehicleList :
      moves = check_moves( self, vehicle )
      num+=1
      for edge in moves:#change placement of vehicles in grid and edit their coordinates in the vehicle list
        newGrid = deepcopy(self.state)
        newVehicleList = deepcopy(self.vehicleList)
        if ( edge[1] == "R" ):
          newGrid[vehicle.xcor][vehicle.ycor] = "-"
          if (vehicle.size > 2):
            newGrid[vehicle.xcor+3][vehicle.ycor] = vehicle.name
          else:
            newGrid[vehicle.xcor+2][vehicle.ycor] = vehicle.name
          newVehicleList[num].xcor = newVehicleList[num].xcor+1
        elif ( edge[1] == "L" ):
          newGrid[vehicle.xcor-1][vehicle.ycor] = vehicle.name
          if (vehicle.size > 2):
            newGrid[vehicle.xcor+2][vehicle.ycor] = "-"
          else:
            newGrid[vehicle.xcor+1][vehicle.ycor] = "-"
          newVehicleList[num].xcor = newVehicleList[num].xcor-1
        elif ( edge[1] == "D" ):
          newGrid[vehicle.xcor][vehicle.ycor] = "-"
          if (vehicle.size > 2):
            newGrid[vehicle.xcor][vehicle.ycor+3] = vehicle.name
          else:
            newGrid[vehicle.xcor][vehicle.ycor+2] = vehicle.name
          newVehicleList[num].ycor = newVehicleList[num].ycor+1
        elif ( edge[1] == "U" ):
          newGrid[vehicle.xcor][vehicle.ycor-1] = vehicle.name
          if (vehicle.size > 2):
            newGrid[vehicle.xcor][vehicle.ycor+2] = "-"
          else:
            newGrid[vehicle.xcor][vehicle.ycor+1] = "-"
          newVehicleList[num].ycor = newVehicleList[num].ycor-1

        my_edges.append( Edge( self, edge, RushHour( newGrid, newVehicleList ) ) );

    return my_edges
        
  
  def is_target( self ):
    return (self.state[4][2] == "X" and self.state[5][2] == "X")

if __name__ == "__main__":  
  
  grid = [[0 for x in range(6)] for x in range(6)]
  vehicleList = []
  f = open('test.txt', 'r')
  data = f.readline()
  while ( data != "" ):
    if( data[0] == "O" or data[0] == "P" or data[0] == "Q" or data[0] == "R"):
      vehicleList.append( Vehicle(data[0], data[1], data[2], data[3], 3) )
    else:
      vehicleList.append( Vehicle(data[0], data[1], data[2], data[3], 2) )
    
    data = f.readline(); #read in line of data from file and add the vehicle info to the vehicle list
  
  for y in range(0,6):
    for x in range(0,6):
      grid[x][y] = "-"
  for vehicle in vehicleList: #for every vehicle read from the file add them onto the grid (state)
      
    if(vehicle.direction == "H"):
      if ( vehicle.size > 2):
        grid[vehicle.xcor + 2][vehicle.ycor] = vehicle.name
        grid[vehicle.xcor + 1][vehicle.ycor] = vehicle.name
        grid[vehicle.xcor][vehicle.ycor] = vehicle.name
      else:
        grid[vehicle.xcor][vehicle.ycor] = vehicle.name
        grid[vehicle.xcor + 1][vehicle.ycor] = vehicle.name
    
    else:
      if ( vehicle.size > 2):
        grid[vehicle.xcor][vehicle.ycor + 2] = vehicle.name
        grid[vehicle.xcor][vehicle.ycor + 1] = vehicle.name
        grid[vehicle.xcor][vehicle.ycor] = vehicle.name
      else:
        grid[vehicle.xcor][vehicle.ycor] = vehicle.name
        grid[vehicle.xcor][vehicle.ycor + 1] = vehicle.name
  
  RushHour( state=grid, vehicleList=vehicleList, root=True).bfs()#change this line to change which search is performed, see pdf report for more
 
