

type Position = tuple[int,int,int]
type Velocity = tuple[int,int,int]

class Line:
    start_point: Position
    velocity: Velocity

    def __init__(self, point:Position, velocity:Velocity):
        self.start_point = point
        self.velocity = velocity

    def point_is_in_past(self, point:Position) -> bool:
        time = (point[0]-self.start_point[0]) / self.velocity[0]
        return time < 0

def parse_input(_input:str):
    lines: list[Line] = []
    for line in _input.split('\n'):
        pos,vel = line.split('@')
        position: Position = tuple(map(int, pos.split(',')))
        velocity: Velocity = tuple(map(int, vel.split(',')))

        lines.append(Line(position, velocity))

    return lines

# https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line
def intersect_lines(lineA:Line, lineB:Line):
    x1 = lineA.start_point[0]
    x2 = lineA.start_point[0]+lineA.velocity[0]
    y1 = lineA.start_point[1]
    y2 = lineA.start_point[1]+lineA.velocity[1]
    x3 = lineB.start_point[0]
    x4 = lineB.start_point[0]+lineB.velocity[0]
    y3 = lineB.start_point[1]
    y4 = lineB.start_point[1]+lineB.velocity[1] 

    # test for parallel
    if ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)) == 0:
        return None
    
    px = ((x1*y2 - y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4)) / ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    py = ((x1*y2 - y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4)) / ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    return (px,py)

def point_is_inside_area(position:Position, area_min:Position, area_max:Position):
    if position[0]<area_min[0]:
        return False
    if position[1]<area_min[1]:
        return False
    if position[0]>area_max[0]:
        return False
    if position[1]>area_max[1]:
        return False
    return True




def run(_input: str):
    lines = parse_input(_input)
    area_min = (200000000000000,200000000000000)
    area_max = (400000000000000,400000000000000)
    total_crossings = 0
    for line_a_idx,line_a in enumerate(lines):
        for line_b_idx in range(line_a_idx+1, len(lines)):
            line_b = lines[line_b_idx]
            intersection = intersect_lines(line_a, line_b)
            if intersection is None:
                print("no intersection")
                continue
            if line_a.point_is_in_past(intersection):
                print(f"{intersection} is in past for A")
                continue
            if line_b.point_is_in_past(intersection):
                print(f"{intersection} is in past for B")
                continue
            if point_is_inside_area(intersection, area_min, area_max):
                print(f"{intersection} is inside")
                total_crossings+=1
            else:
                print(f"{intersection} is outside")
                continue
    print(total_crossings)
    return total_crossings

with open("day24_test_input.txt", "r") as f:
    run(f.read())