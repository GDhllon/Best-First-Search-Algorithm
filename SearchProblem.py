import sys
import heapq
from math import sqrt
from Queue import PriorityQueue


class MyPriorityQueue:#min heap which acts as a priority queue
  def __init__(self):
    self.heap = []

  def add(self, d, pri):
    heapq.heappush(self.heap, (pri, d))

  def get(self):
    pri, d = heapq.heappop(self.heap)
    return d

class SearchProblem:
  """
  This class represents the superclass for a search problem.

  Programmers should subclass this superclass filling in specific
  versions of the methods that are stubbed below.
  """
  
  states = 0 #keep track of states visited
  
  statesAtDepth = [0] * 26 #keep track of the number of possible states at each depth
  
  stop = False; # class variable to end search - single variable accessible to
                # all instances of the class

  visited = []; # class variable that holds the states visited along the
        # path to the current node - used to avoid loops


  def __init__( self, state=None ):
    """
    Stub
    Constructor function for a search problem.

    Each subclass should supply a constructor method that can operate with
    no arguments other than the implicit "self" argument to create the
    start state of a problem.

    It should also supply a constructor method that accepts a "state"
    argument containing a string that represents an arbitrary state in
    the given search problem.

    It should also initialize the "path" member variable to a (blank) string.
    """
    raise NotImplementedError("__init__");

  def edges( self ):
    """
    Stub
    This method must supply a list or iterator for the Edges leading out 
    of the current state.
    """
    raise NotImplementedError("edges");

  def is_target( self ):
    """
    Stub
    This method must return True if the current state is a goal state and
    False otherwise.
    """

    raise NotImplementedError("is_target");

  def __repr__( self ):
    """
    This method must return a string representation of the current state
    which can be "eval"ed to generate an instance of the current state.
    """

    return self.__class__.__name__ + "( " + repr(self.state) + ")";

  def target_found( self ):
    """
    This method is called when the target is found.

    By default it prints out the path that was followed to get to the 
    current state.
    """
    print( "Solution: " + self.path );
    print( "Depth: ",  self.path.count(' '))
    print( "states visited: ", SearchProblem.states )
    
    if(self.path.count(' ') > 0 and self.path.count(' ') < 25):
      print("This game can be solved in less than 25 moves, it has an easy difficulty")
    
    elif(self.path.count(' ') >= 25 and self.path.count(' ') < 50):
      print("This game can be solved in between 25 and 50 moves, it has a medium difficulty")
    
    elif(self.path.count(' ') >= 50):
      print("This game can be solved in 50 or more moves, it has a hard difficulty")
    

  def continue_search( self ):
    """
    This method should return True if the search algorithm is to continue
    to search for more solutions after it has found one, or False if it
    should not.
    """
    return False;
    
  def befs ( self, heuristic ): #best first search algorithm
    queue = MyPriorityQueue()
    queue.add( self, 0 )
    while queue:
      current = queue.get()
      SearchProblem.states+=1
      if SearchProblem.stop:
        return
      for action in current.edges():
        action.destination.path = current.path + " " + str(action.label)
        if repr(action.destination.state) in SearchProblem.visited:
          continue;       # skip if we've visited this one before

        SearchProblem.visited.append( repr(action.destination.state) );
        
        if action.destination.is_target(): 
                # check if destination of edge is target node
          action.destination.target_found();  # perform target found action
          if not self.continue_search():  # stop searching if not required
            SearchProblem.stop = True;    # set class variable to record that we
            break;                        # are done
        
        for item in action.destination.vehicleList:
          if (item.name == "X"):
            break
        
        
        if( heuristic == 0 ): #Euclidean distance from red car to finish coordinates
          priority = pow( abs(4 - item.xcor), 2 ) + pow( abs(2 - item.ycor), 2)
          priority =  sqrt(priority)
          priority = priority + current.path.count(' ')
          queue.add(action.destination, priority)
             
        elif ( heuristic == 1 ):#number of vehicles between red car and finish coordinates
          vehiclesInPath = 0
          for x in range(item.xcor+2,6):
            if ( action.destination.state[x][item.ycor] != "-" ):
              vehiclesInPath+=1
          priority = vehiclesInPath + current.path.count(' ')
          queue.add(action.destination, priority)
          
        

  def bfs( self ):#breadth first search (brute force)
    
    queue = []
    queue.append( self )
    num = 0
    
    while queue:
      current = queue.pop(0)
      SearchProblem.states+=1
      depth = current.path.count(' ')
      if SearchProblem.stop:
        return
      for action in current.edges():
        
        action.destination.path = current.path + " " + str(action.label)
        
        if repr(action.destination.state) in SearchProblem.visited:
          continue;       # skip if we've visited this one before
        
        SearchProblem.visited.append( repr(action.destination.state) );
        
        if action.destination.is_target(): 
                # check if destination of edge is target node
          action.destination.target_found();  # perform target found action
          if not self.continue_search():  # stop searching if not required
            SearchProblem.stop = True;    # set class variable to record that we
            break;                        # are done
        queue.append(action.destination)
                    

  def dfs( self ):
    """
    Perform a depth first search originating from the node, "self".
    Recursive method.
    """

    # print statement for debugging
    depth = self.path.count(' ')
    if SearchProblem.stop:  # check class variable and stop searching...
      return;

    for action in self.edges(): # consider each edge leading out of this node

      action.destination.path = self.path + " " + str(action.label);
                    # get the label associated with the
                    # action and append it to the path
                    # string

      if repr(action.destination.state) in SearchProblem.visited:
        continue;       # skip if we've visited this one before

      SearchProblem.visited.append( repr(self.state) );

      if action.destination.is_target(): 
                # check if destination of edge is target node
        action.destination.target_found();  # perform target found action
        if not self.continue_search():  # stop searching if not required
          SearchProblem.stop = True;    # set class variable to record that we
          break;                        # are done
      
      try:
        SearchProblem.states+=1
        SearchProblem.statesAtDepth[depth]+=1
        action.destination.dfs();           # resume recursive search
      except:
        pass 

      SearchProblem.visited.pop();

class Edge:
  """
  This class represents an edge between two nodes in a SearchProblem.
  Each edge has a "source" (which is a subclass of SearchProblem), a
  "destination" (also a subclass of SearchProblem) and a text "label".
  """

  def __init__( self, source, label, destination ):
    """
    Constructor function assigns member variables "source", "label" and
    "destination" as specified.
    """
    self.source = source;
    self.label = label;
    self.destination = destination;

  def __repr__( self ):
    return "Edge(" + repr( self.source ) + "," + \
                     repr( self.label ) + "," + \
                     repr( self.destination ) + ")";
