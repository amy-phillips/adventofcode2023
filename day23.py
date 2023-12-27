from __future__ import annotations  # i want to be able to typehint a Node inside a Node

import cProfile
import copy

type Location = tuple[int,int]

# a segment is a group of Locations with no forks in it - a single line of Locations, may be twisty turny
class Segment:
    location_count: int
    end_location: Location
    prev_end_location: Location
    came_from: Segment 

    def __init__(self, _start_location: Location, _came_from: Segment) -> Segment:
        self.location_count = 1
        self.end_location = _start_location
        self.prev_end_location = None
        self.came_from = _came_from

    def add_location(self, location: Location):
        self.prev_end_location = self.end_location
        self.end_location = location
        self.location_count+=1

    #def get_end_location(self):
    #    return self.end_location
    
    #def check_for_doubling_back(self, location: Location):
    #    return location == self.prev_end_location


def parse_input(_input: str) -> (dict[Location,str], list[Location], tuple[int,int]):
    lines = _input.split("\n")
    map_squares = {}
    entrances = []
    for y,line in enumerate(lines):
        for x,char in enumerate(line):
            map_squares[(x,y)]=char
            is_on_side = (x==0 or x==len(line)-1) or (y==0 or y==len(lines)-1)
            if char == '.' and  is_on_side:
                entrances.append((x,y))
    extents = (len(lines[0]),len(lines))
    return map_squares,entrances,extents

def is_neighbour_accessible(possible_neighbour:Location, map_squares: dict[Location,str]):
    if possible_neighbour not in map_squares: # check we didn;t fall off the edge
        return False
    if map_squares[possible_neighbour] == "#":
        return False
    return True

# we just need to test against the ends of each segment, we couldn't get to the middles without passing the ends!
def is_visited(neighbour:Location, current:Segment):
    # first check we're not doubling back in the current segment
    #if current.check_for_doubling_back(neighbour): removed function call for speed
    if neighbour == current.prev_end_location:
        return True
    while current.came_from is not None:
        current = current.came_from
        if current.end_location == neighbour:
            return True
        
    return False

def get_possible_neighbours(current: Location, last_segment:Segment, map_squares: dict[Location,str]):
  
    neighbours: list[Location] = []

    # let's look in the 4 directions around us
    possible_neighbour=(current[0]-1,current[1])
    if is_neighbour_accessible(possible_neighbour, map_squares) and not is_visited(possible_neighbour,last_segment) :
        neighbours.append(possible_neighbour)
    possible_neighbour=(current[0]+1,current[1])
    if is_neighbour_accessible(possible_neighbour, map_squares) and not is_visited(possible_neighbour,last_segment):
        neighbours.append(possible_neighbour)
    possible_neighbour=(current[0],current[1]-1)
    if is_neighbour_accessible(possible_neighbour, map_squares) and not is_visited(possible_neighbour,last_segment):
        neighbours.append(possible_neighbour)
    possible_neighbour=(current[0],current[1]+1)
    if is_neighbour_accessible(possible_neighbour, map_squares) and not is_visited(possible_neighbour,last_segment):
        neighbours.append(possible_neighbour)

    return neighbours

def reconstruct_path_length(current: Segment) -> list[Location]:
    total_path_length = current.location_count
    while current.came_from is not None:
        current = current.came_from
        total_path_length += current.location_count
    return total_path_length

#result_count = 0

def follow_path(start:Location, goal:Location, map_squares: dict[Location,str]) -> int:

    max_path_len = 0

    open_nodes: list[Segment] = []
    open_nodes.append(Segment(start,None))
    while len(open_nodes) > 0:
        current = open_nodes.pop()

        # follow this path until it splits, building it up inside current Segment
        while True:
            if current.end_location == goal:
                path_len = reconstruct_path_length(current)
                print(path_len)
                max_path_len = max(max_path_len,path_len)
                #global result_count
                #result_count += 1
                #if result_count > 200:
                #    exit(0)
                break 

            neighbours = get_possible_neighbours(current.end_location, current, map_squares)
            if len(neighbours) == 0:
                # dead end
                # back to the last decision
                break

            if len(neighbours) == 1:
                current.add_location(neighbours[0])
                continue

            if len(neighbours) > 1:
                # new segments
                for neighbour in neighbours:
                    open_nodes.append( Segment(neighbour,current) )

                break
    
    return max_path_len
   

def run(_input):
    map_squares,entrances,extents=parse_input(_input)
    start = entrances[0]
    goal = entrances[1]
    longest = follow_path(start,goal,map_squares)
    print(longest)

with open("day23_actual_input.txt", "r") as f:
    cProfile.run("run(f.read())")

