input = """.........................#.........................#.....................#........#..................#............#...............#.........
............................................................................................................................................
...................................#......................#.................................................................................
............................................................................................#..........................#.....#..............
..#............................#..............#...................#........................................#.............................#..
............................................................................................................................................
................#.....#..............#.......................................#.................#.....#......................................
........#.............................................#..................................................................#..................
..........................................#..................#..........#...............#.........................................#.........
#................................................................................#.............................#..........................#.
............................................................................................................................................
............#...............................................................................................................................
.......................#.....#.................#..........................#.........................................................#.......
.................................................................................................#..........................................
...................................#................#..................................#.............................#......................
....#.....................................................#................................................#................#............#..
..........#......................................................................#............#.............................................
.....................................................................................................#............#..............#..........
........................#.........................................#.....#...............................................#...................
..#............................#............................................................................................................
..............#.........................#...................#.....................................#......#..................................
............................................................................#......#........................................................
...........................................................................................................................#................
...................#.................................................................................#..............#............#..........
..........................#.......................#........................................#.............................................#..
...................................................................#........................................................................
#...............#.....................#.....#.....................................#.........................................................
.................................#.........................................#...........................#....................................
......#.........................................................................................#...........#..............#................
..........................................................#............................................................................#....
....................................................................................................................#..........#............
.............#......#........................#..............................................................................................
.......................................#............................#..................#....................................................
.....................................................#..............................................#.......................................
..#..........................#.................................................#...............#................#...........................
.......#.......#............................................#.....................................................................#.........
.........................................#.....#....................................................................#.....#.................
.......................................................................................................#....................................
....#...............................................#....................#.........#..............#.........................................
.............................................................................................................#.......................#......
.....................#........#.............................................................................................................
............................................................#.....#.........................................................#...............
.............#...............................#.........#.................................#.......................#..........................
........................................................................#......#............................................................
............................#..........................................................................................#...................#
.#.......#..........#..................#.........................................................................................#..........
................................#...........................................................................................................
....................................................#...........#......................#........#...........................................
......#.....#...............................................................................................................................
.........................................................#.......................#......................#.............................#.....
.........................................#.................................#.........................................#......................
...............................................................................................................................#............
.......................#......................................................................#.............................................
#......#......................#...............#.....#..................#...................................................#................
................................................................................#.............................#.............................
..................#.......................#..........................................#..............#...............#............#........#.
............................................................................................................................................
..#.............................#..............................#............................................................................
.............................................#............#............................................................#....................
........................................................................................................................................#...
......................................................................#..........................#.....#.....#..............................
.............#.....#........................................................................................................................
.....#...............................................#.....................................#.......................#........................
...........................#....................................#..............................................................#............
............................................................................................................................................
............................................................................................................................................
...................................#..........#..............#......#.................#..........................#........#...............#.
..............#......................................................................................................................#......
..........................#.............................................#......#............................................................
.......#...........#.........................................................................#..............................................
................................#.................#.................................................#.....#.............#...................
.......................#................................#............................#......................................................
............................................#....................#..................................................#.......................
............................#.............................................................#....................#............................
...........................................................................#................................................................
.......#.....#.......................#.....................................................................#................................
..#.........................................................................................................................................
.....................#.........................................................#...............#............................................
..........................................#..........#.......#........................#.....................................................
................................#...................................#...............................#.....................#.....#...........
............................................................................#...............#...............................................
.............#.............#..........#...........................................#...............................#.........................
...................................................................................................................................#.....#..
.#.......#...............................................................................................#..................................
.........................................#...............#............................#.......................#...............#.............
...........................................................................#............................................#...................
....................#..........#.............#.....................................................#........................................
......#.....................................................................................................................................
#...........................................................................................................................................
....................................................................#.............#.....................#...........#.......................
..........#......................................#.............#.............#..............................................................
..........................#.............................#..................................#...................#...............#.........#..
...................#........................................................................................................................
...................................#..............................#.........................................................................
#..............#.......................................................#.......#..................#........#................................
........................................................................................................................#...................
.......#.................#......#......................................................#.....................................#..............
........................................................#.............................................#.....................................
............................................................................#.....................................#.........................
...............................................................#...................#........#......................................#........
..................#...............................#..................#......................................#...............................
.....................................#................................................................................#.....................
............#.......................................................................................#.......................................
...........................#..............................................................#............................................#....
..........................................#................................#................................................................
.............................................................#................................#.................................#...........
.....................#..............#..............................................................................#........................
..............................#.....................#.............#...................................#.....................................
................#................................................................#.............................#..........#.................
..........#............................................................................#..................#.................................
...................................................................................................#...........................#.....#......
............................................................................................................................................
.....#..............................#.............#.................#.......................................................................
.............................................#...............#...........#..........................................#.......................
.......................#......#.........................#...................................................................#...............
.#........................................................................................#............#............................#.......
..................................#.............................................#................#............#.............................
..........................#.........................#.......................................................................................
.............#......#..........................#.....................................#....................#.................................
............................................................#.............#.........................................#.......................
...........................................#................................................................................................
..........#..........................#...............................#...............................#............................#.........
............................#..................................#.........................#................................................#.
.............................................................................#...................#..........................................
....#...............................................#.................................................................................#.....
.................#.....#.......#...............#......................................#...........................#.........................
....................................#......................................................#................................................
........................................................#........#..............#......................................#....................
#......#.....#........................................................................................#.....................#......#........
...................................................#.........#..........#.......................................#...........................
.........................................................................................#..................................................
...............................................................................................................................#............
................................................#..........................#....................#...........................................
.........#.........................................................................#...................#....................................
..........................#........................................#.........................................#.......#......................
....................................................#...................................#...................................................
............................................#.................#...................................#...........................#.............
.....................#............#.........................................................................................................
.......#....................................................................#...........................#.........................#......#..
.......................................................#.......................................................#............................"""


galaxies = []
for row_idx,line in enumerate(input.split('\n')):
    for col_idx,letter in enumerate(line):
        if letter == '#':
            galaxies.append({"row_idx":row_idx, "col_idx":col_idx})
        
# find rows and columns with no galaxies
galaxy_rows = set(gal["row_idx"] for gal in galaxies)
galaxy_cols = set(gal["col_idx"] for gal in galaxies)

def get_expanded_distance(idxa, idxb):
    global galaxies
    global galaxy_rows
    global galaxy_cols

    mincol = min(galaxies[idxa]["col_idx"], galaxies[idxb]["col_idx"])
    minrow = min(galaxies[idxa]["row_idx"], galaxies[idxb]["row_idx"])
    maxcol = max(galaxies[idxa]["col_idx"], galaxies[idxb]["col_idx"])
    maxrow = max(galaxies[idxa]["row_idx"], galaxies[idxb]["row_idx"])

    scale = 1000000-1

    distance = 0
    for row in range(minrow+1, maxrow+1):
        distance+=1
        # and is this row expanded
        if row not in galaxy_rows:
            distance+=scale

    for col in range(mincol+1, maxcol+1):
        distance+=1
        # and is this row expanded
        if col not in galaxy_cols:
            distance+=scale

    return distance

distance = 0
for idxa in range(0, len(galaxies)):
    for idxb in range(idxa+1, len(galaxies)):
        distance+=get_expanded_distance(idxa, idxb)
print(distance)
