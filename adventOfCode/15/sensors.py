import re
from scipy.spatial.distance import cityblock
import intervaltree

# takes in 2 vectors
def manhattan_distance(p1, p2):
    return cityblock(p1, p2)

assert(manhattan_distance((-10000000,0), (-10000001,1))==2)

def is_in_area(point, sensor, distance):
    return manhattan_distance(point, sensor) < distance

assert(is_in_area((-10000000,0), (-10000001,1), 3))
assert(not is_in_area((-10000000,0), (-10000001,1), 1))

def _open():
    f = open("input.txt")
    text = f.read()
    f.close()
    return text

def scrape_data(text):
    data = []
    for line in text.split('\n'):
        pattern = re.compile("Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)")
        match = re.match(pattern, line)
        if not match:
            print(line)
            continue
        ss = (int(match[1]),int(match[2]))
        bc = (int(match[3]),int(match[4]))
        data.append((ss,bc))
    return data


def get_intersection_with_y(y, sensor, beacon):
    '''
    Return range of points in L (only x coordinates) that the Sensor can see
                      
            ......................
            ..........S........... 
            ..........|...........  
            ..........|...........  
            ..........|...........           
            ..........|...........          
         L: -----iiiiiCiiiii------   
            ..........|...........   
            ..........|__B........  
            ......................    
            ......................
            ......................

            ......................
            ..........S........... 
            ..........|...........  
            ..........|...........  
            ..........|------B....           
            ..........|...........          
         L: -----iiiiiCiiiii------   
            ......................   
            ......................  
            ......................    
            ......................
            ......................
    '''
    center = (sensor[0], y)
    max_distance = manhattan_distance(sensor, beacon)
    # line-to-point distance from L to sensor must be <= to max_distance
    line_point_distance = manhattan_distance(center, sensor)
    # max_distance - manhattan(center, sensor) gives the radius of the range
    x_distance = max_distance - line_point_distance

    if x_distance < 0: return None
    
    print("current pair: " + str(sensor) + str(beacon))
    print("max distance: "+str(max_distance))
    print("center: " + str(center))
    print("x distance: "+str(x_distance))

    # create range
    answer = (center[0]-x_distance, center[0]+x_distance)
    assert(len(range(answer[0], answer[1]+1)) <= 2*max_distance)

    print("range: "+str(answer))
    return answer

def combine_ranges(ranges):
    '''
    Take ranges, merge them into a simpler set of ranges
    '''
    tree = intervaltree.IntervalTree.from_tuples(ranges)
    print(tree)
    tree.merge_overlaps()
    print(tree)
    list_of_lists = list(map(lambda interval: list(range(interval.begin, interval.end+1)),tree.items()))
    return list(set([item for sublist in list_of_lists for item in sublist]))

def main(data = None, Y = 2000000):
    if not data:
        data = scrape_data(_open())

    ranges = []
    for sensor, beacon in data:
        range = get_intersection_with_y(Y, sensor, beacon)
        if range:
            ranges.append(range)

    observed_beacons = map(lambda pair: pair[1], data)
    relevant_beacons = list(set(filter(lambda point: point[1] == Y, observed_beacons)))

    answer = []
    print("the ranges were:")
    for r in ranges:
        print(r)
    print("the relevant beacons were:" + str(relevant_beacons))
    li = combine_ranges(ranges)
    print("length of combined ranges was: " + str(len(li)))
    num_beacons = len(relevant_beacons)
    print("# guaranteed non beacons: "+str(len(li) - num_beacons) )
main()
            

    