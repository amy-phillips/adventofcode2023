input = """.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##..S####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
................................."""

type MapTile = tuple[int,int]
type LocationInMapTile = tuple[int,int]

type Location = tuple[LocationInMapTile, MapTile] # location is x,y then maptilex, maptiley (might be nicer as classes!)
type Garden = dict[Location,str]

import cProfile
import unittest

def parse_map(input: str):
    garden_map: dict[LocationInMapTile,character] = {}
    start_position: Location
    for line_idx,line in enumerate(input.split('\n')):
        for row_idx,character in enumerate(line):
            garden_map[(row_idx,line_idx)]=character
            if character == 'S':
                start_position = ((row_idx,line_idx),(0,0))
    return garden_map, start_position, (row_idx+1,line_idx+1)

def try_position(position:Location, garden_map: Garden, extents:tuple[int,int]):
    # if fell off edge - wrap to a new tile
    if position[0][0] < 0:
        position = ((position[0][0]+extents[0],position[0][1]),(position[1][0]-1, position[1][1]))
    elif position[0][0] >= extents[0]:
        position = ((position[0][0]-extents[0],position[0][1]),(position[1][0]+1, position[1][1]))
    if position[0][1] < 0:
        position = ((position[0][0],position[0][1]+extents[1]),(position[1][0], position[1][1]-1))
    elif position[0][1] >= extents[1]:
        position = ((position[0][0],position[0][1]-extents[1]),(position[1][0], position[1][1]+1))

    in_tile_position = position[0]

    if garden_map[in_tile_position] == '.':
        return position # can move here
    if garden_map[in_tile_position] == 'S':
        return position # can move here
    return None # no - can't move here!

def take_step(position: Location, garden_map: Garden, extents: tuple[int,int]):
    positions = []
    possible_position = try_position(((position[0][0]-1,position[0][1]),position[1]), garden_map, extents)
    if possible_position is not None:
        positions.append(possible_position)
    possible_position = try_position(((position[0][0]+1,position[0][1]),position[1]), garden_map, extents)
    if possible_position is not None:
        positions.append(possible_position)
    possible_position = try_position(((position[0][0],position[0][1]-1),position[1]), garden_map, extents)
    if possible_position is not None:
        positions.append(possible_position)
    possible_position = try_position(((position[0][0],position[0][1]+1),position[1]), garden_map, extents)
    if possible_position is not None:
        positions.append(possible_position)
    return positions

def debug_print(positions: list[Location], garden_map: Garden, extents: tuple[int,int]):
    for y in range(0,extents[1]):
        for x in range(0,extents[0]):
            if (x,y) in positions:
                print("O",end="")
            else:
                print(f"{garden_map[(x,y)]}",end="")
        print("") # newline
    print("") # newline

class PositionCache:
    tile_caches: dict[MapTile,dict[int,int]] = {}
    all_positions_seen: dict[MapTile,list[set[LocationInMapTile]]] = {}

    def gethashkey(self, current_positions: frozenset[LocationInMapTile]):
        return hash(frozenset(current_positions))

    def add_positions(self, current_positions: frozenset[LocationInMapTile], tile: MapTile):
        # gonna keep a separate cache per maptile - maybe can share in same direction.... maybe??
        if not tile in self.tile_caches:
            self.tile_caches[tile] = {}
            self.all_positions_seen[tile] = []
        tile_cache = self.tile_caches[tile]
        cache_key = self.gethashkey(current_positions)
        if cache_key in tile_cache:
            # don't overwrite cache entry, we're rounding a loop!
            return
        self.all_positions_seen[tile].append(current_positions)
        tile_cache[cache_key] = len(self.all_positions_seen[tile])-1

    def get_next_positions(self, current_positions: frozenset[LocationInMapTile], tile: MapTile):
        # gonna keep a separate cache per maptile - maybe can share in same direction.... maybe??
        if not tile in self.tile_caches:
            return None
        tile_cache = self.tile_caches[tile]
        cache_key = self.gethashkey(current_positions)
        if cache_key in tile_cache:
            same_as_step = tile_cache[cache_key]
            if same_as_step+1 < len(self.all_positions_seen[tile]):
                # so next up is same_as_step+1
                #print(f"{tile}: cache match on step {same_as_step} == {len(self.all_positions_seen[tile])}  {cache_key}")
                return self.all_positions_seen[tile][same_as_step+1]
        return None



def run(step_count:int):
    garden_map, starting_position, extents = parse_map(input)

    steps_cache: PositionCache = PositionCache()
    positions: dict[MapTile,set[Location]] = {}
    positions[(0,0)] = {starting_position}
    next_positions: dict[MapTile,list[Location]] = {}
    for i in range(0,step_count):
        # split positions into tiles for caching
        for map_tile, map_tile_positions in positions.items():
            cached_positions = steps_cache.get_next_positions(map_tile_positions,map_tile)
            if cached_positions is None:
                for position in map_tile_positions:
                    stepped_positions = take_step(position, garden_map, extents)
                    # some of these need to move to their own lists!
                    for pos in stepped_positions:
                        if not pos[1] in next_positions:
                            next_positions[pos[1]] = set()
                        next_positions[pos[1]].add(pos)
                steps_cache.add_positions(next_positions[map_tile],map_tile)
            else:
                next_positions[map_tile] = cached_positions

        positions,next_positions = next_positions,positions # swap lists
        
    #debug_print(positions, garden_map, extents)
    total=0
    for positions_in_tile in positions.values():
        #print(len(positions_in_tile))
        total+=len(positions_in_tile)
    print(total)
    return total

class TestSmallerRuns(unittest.TestCase):

    def test_6_steps(self):
        plot_count = run(6)
        self.assertEqual(plot_count, 16)

    def test_10_steps(self):
        plot_count = run(10)
        self.assertEqual(plot_count, 50)
   
    def test_50_steps(self):
        plot_count = run(50)
        self.assertEqual(plot_count, 1594)

    def test_100_steps(self):
        plot_count = run(100)
        self.assertEqual(plot_count, 6536)

    def test_500_steps(self):
        plot_count = run(500)
        self.assertEqual(plot_count, 167004)

    #def test_1000_steps(self):
    #    plot_count = run(1000)
    #    self.assertEqual(plot_count, 668697)

    #def test_5000_steps(self):
    #    plot_count = run(5000)
    #    self.assertEqual(plot_count, 16733044)


if __name__ == '__main__':
    #unittest.main()
    cProfile.run("run(500)")