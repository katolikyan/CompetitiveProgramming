from parsing import *
from data_structures import *
import os
import sys
from datetime import timedelta
from colors import *

# finds shortest path between 2 nodes of a graph using BFS
def bfs_shortest_path(graph, start, goal):
    explored = []
    queue = [[start]]

    if start == goal:
        return "That was easy! Start = goal"

    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                if neighbour == goal:
                    return new_path

            explored.append(node)
    return "So sorry, but a connecting path doesn't exist :("

def main(argv):
# php SCRIPT :
    querie = "php run_me.php " + "'"+argv[1] + "' '" + argv[2]+ "'"
    output = os.system(querie + " 1>/dev/null")
    if os.stat("./tmp_start.json").st_size < 10 or \
            os.stat("./tmp_final.json").st_size < 10 or \
            os.stat("./tmp_semi_parsed_stop_points.json").st_size < 10:
        print ("Wrong place :(")
        sys.exit()


# Making graph from stations:
    graph = {}
    routes = get_routes("./tmp_semi_parsed_stop_points.json")
    for route in routes:
        names = []
        for stop in route.nodes:
            names.append(stop.name);
        for i in range(len(names)):
            if names[i] not in graph:
                graph[names[i]] = []
            if (i - 1 >= 0 and names[i - 1] not in graph[names[i]]):
                graph[names[i]].append(names[i - 1])
            if (i + 1 <= len(names) and names[i - 1] not in graph[names[i]]):
                graph[names[i]].append(names[i + 1])

#get class start end stations:
    start = get_stop("./tmp_start.json")
    end = get_stop("./tmp_final.json")

#Find shortest path:
    trace = bfs_shortest_path(graph, start.name, end.name)  # returns ['G', 'C', 'A', 'B', 'D']
#print(trace)

# maping routes and stations:
    stop_lines = {}
    for route in routes:
        r = [];
        for stop in route.nodes:
            if stop.name not in stop_lines:
                stop_lines[stop.name] = [];
            stop_lines[stop.name].append(route.route_id)

    color_table = {
    'route:0:1001100010001A' : '#FFBF00',
    'route:0:1001100010001R' : '#FFBF00',
    'route:0:1001100020001A' : '#0054C9',
    'route:0:1001100020001R' : '#0054C9',
    'route:0:1001100030001A' : '#6E6E00',
    'route:0:1001100030001R' : '#6E6E00',
    'route:0:1001101030001A' : '#83C9E6',
    'route:0:1001101030001R' : '#83C9E6',
    'route:0:1001100040001R' : '#A2006F',
    'route:0:1001100040001A' : '#A2006F',
    'route:0:1001100050001A' : '#FF5900',
    'route:0:1001100050001R' : '#FF5900',
    'route:0:1001100060001R' : '#82DD73',
    'route:0:1001100060001A' : '#82DD73',
    'route:0:1001100070001A' : '#FF83B5',
    'route:0:1001100070001R' : '#FF83B5',
    'route:0:1001101070001A' : '#82DD73',
    'route:0:1001101070001R' : '#82DD73',
    'route:0:1001100080001A' : '#D383BF',
    'route:0:1001100080001R' : '#D383BF',
    'route:0:1001100090001R' : '#D3D300',
    'route:0:1001100090001A' : '#D3D300',
    'route:0:1001100100001A' : '#DD9700',
    'route:0:1001100100001R' : '#DD9700',
    'route:0:1001100110001R' : '#6F4717',
    'route:0:1001100110001A' : '#6F4717',
    'route:0:1001100120001R' : '#006439',
    'route:0:1001100120001A' : '#006439',
    'route:0:1001100130001A' : '#8ECFE9',
    'route:0:1001100130001R' : '#8ECFE9',
    'route:0:1001100140001R' : '#640083',
    'route:0:1001100140001A' : '#640083'
    }

# maping stations and colors:
    stop_color = {}
    for stop in stop_lines:
        for route in stop_lines[stop]:
            if stop not in stop_color:
                stop_color[stop] = []
            if color_table[route] not in stop_color[stop]:
                stop_color[stop].append(color_table[route])


# dictionary with transfers:
    transfers = {}
    for stop in trace:
        transfers[stop] = 0
    crnt = stop_lines[trace[0]];
    for i in range(len(trace) - 1):
        check = 0;
        for cr in crnt:
            if cr in stop_lines[trace[i + 1]]:
                check = 1;
                break
        if (check == 0):
            crnt = stop_lines[trace[i + 1]]
            transfers[trace[i]] = 1;

# printing the map:
    print("\n\n    ", end='')
    stops = len(trace);
    padding = 4;
    for stop in trace:
        n = 0;
        stops -= 1
        #l = len(stop_color[stop])
        for line_color in stop_color[stop]:
            print(color("⬤", line_color), end='')
            n += 1
            padding += 1
        if transfers[stop]:
            padding -= 1
            print(color("\n" + " " * (padding - n), '#696969'), end='')
            for line_color in stop_color[stop]:
                 print(color("⬤", line_color), end='')
        if (stops):
            print(color(" ─────────", '#696969'), end='')
            padding += 10
# printing short station names:
    print("\n")
    for i in range(len(trace) - 1):
        pad = len(stop_color[trace[i + 1]]) / 2
        if len(stop_color[trace[i]]) % 2 and len(stop_color[trace[i]]) != 1:
            pad += 0.5
        print(trace[i][:7] + '..' + ' ' * 2 + ' ' * int(pad), end='')
        if len(stop_color[trace[i + 1]]) % 2 and len(stop_color[trace[i]]) != 1:
            print(' ', end='')
    print(trace[-1][:7] + '..')


# printing instructions:
    #first station:
    print("\n")
    print("0. Go to ", end='')
    print(color(' ', '', '#353535'), end='')
    for line_color in stop_color[start.name]:
        print(color("●", line_color, '#353535'), end='')
    print(color(' ' + start.name + " ", "white", '#353535'), end='')
    print(" and take a train in direction of ", end='')
    print(color(' ', '', '#353535'), end='')
    for line_color in stop_color[trace[1]]:
        print(color("●", line_color, '#353535'), end='')
    print(color(' ' + trace[1] + " ", "white", '#353535'))

    #transfers:
    step = 1
    for i in range(len(trace) - 1):
        if transfers[trace[i]]:
            print(str(step) + ". ", end='')
            print("Make a transfer on ", end='')
            print(color(' ', '', '#353535'), end='')
            for line_color in stop_color[trace[i]]:
                print(color("●", line_color, '#353535'), end='')
            print(color(' ' + trace[i] + " ", "white", '#353535'), end='')
            print(" in direction of ", end='')
            print(color(' ', '', '#353535'), end='')
            for line_color in stop_color[trace[i + 1]]:
                print(color("●", line_color, '#353535'), end='')
            print(color(' ' + trace[i + 1] + " ", "white", '#353535'))
            step += 1

    #last station:
    print(str(step) + ". ", end='')
    print("Get off the train at ", end='')
    print(color(' ', '', '#353535'), end='')
    for line_color in stop_color[end.name]:
        print(color("●", line_color, '#353535'), end='')
    print(color(' ' + end.name + " ", "white", '#353535'))

# time estimation:
    transfers_num = 0;
    for key in transfers:
        if transfers[key]:
            transfers_num += 1
    print("Estimated time to destination: ", end='')
    print(timedelta(minutes=(len(trace) * 1.5 + transfers_num * 5 + 15)))
    print()



    '''
# printing the route:
    print(start.name + " in direction of " + trace[1])
    crnt = stop_lines[trace[0]];
    for i in range(len(trace) - 1):
        check = 0;
        for cr in crnt:
            if cr in stop_lines[trace[i + 1]]:
                check = 1;
                break
        if (check == 0):
            crnt = stop_lines[trace[i + 1]]
            print("transfer: " + trace[i] + " in direction of " + trace[i + 1])
    print(end.name)
    '''

if __name__ == "__main__":
    main(sys.argv)
