import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from statistics import mean, median, median_high
from math import ceil

sources = [
    "./source/a.txt",
    "./source/b.txt",
    "./source/c.txt",
    "./source/d.txt",
    "./source/e.txt",
    "./source/f.txt"
]
outputs = [
    "./results/a.txt",
    "./results/b.txt",
    "./results/c.txt",
    "./results/d.txt",
    "./results/e.txt",
    "./results/f.txt"
]
#choise = 4 # from 0 to 5

class Street():

    def __init__(self, B, E, name, L):
        self.B = B
        self.E = E
        self.name = name
        self.L = L
        self.priority = 0
        self.n_times_mentioned = 0

    def calculate_priority(self):
        self.priority = (self.n_times_mentioned / self.L)
        #self.priority = (self.n_times_mentioned * 10) / self.L 
        return self.priority

    def mention(self, start_street=False):
        if start_street:
            #self.n_times_mentioned += 2
            self.n_times_mentioned += 1
        else:
            self.n_times_mentioned += 1

streets_dict_list = {}


def calc_proportional_times(streets):
    proportions = [m.calculate_priority() for m in streets]
    the_min = min(proportions)
    times = [ceil(num / the_min) for num in proportions]

    #times = [m.n_times_mentioned for m in streets]    
    return times


def calc_avg_mentions(streets_dict_list):
    filtered_streets = [s for s in streets_dict_list.values() if s.n_times_mentioned > 0]
    mentions = [m.n_times_mentioned for m in filtered_streets]
    return mean(mentions)

def calc_avg_segm(streets_dict_list):
    filtered_streets = [s for s in streets_dict_list.values() if s.n_times_mentioned > 0]
    mentions = [m.n_times_mentioned for m in filtered_streets]
    midl = mean(mentions)
    top_avg = [i for i in mentions if i > midl]
    high = mean(top_avg) if top_avg else 100000
    super_top = [i for i in top_avg if i > high]
    highest = mean(super_top) if super_top else 100000
    extra_top = [i for i in super_top if i > highest]
    extra_high = mean(super_top) if super_top else 100000
    return midl, high, highest, extra_high




# --- PARSING ---
for choise in range(6):
    with open(sources[choise], "r") as f:
        # getting starting info:

        D, I, S, V, P = map(int, f.readline().split())
        intersections = dict.fromkeys(list(map(str, range(I))), None)

        # for each street in the input:
        for i in range(S):
            B, E, street_name, L = f.readline().split()
            
            # make a street class and add to streets list 
            street = Street(int(B), int(E), street_name, int(L))
            #streets_dict_list[street_name] = {'B': int(B), 'E': int(E), 'L': int(L), 'priority': 0}
            streets_dict_list[street_name] = street

            if intersections[E]:
                intersections[E].append(street)
            else:
                intersections[E] = [street]

        # for each car in the input:
        for i in range(V):
            car_line_input = list(f.readline().split())
            for i, route_street in enumerate(car_line_input[1:]):
                if i == 0:
                    streets_dict_list[route_street].mention(start_street=True)
                else:
                    streets_dict_list[route_street].mention()



    avg_mentions = calc_avg_mentions(streets_dict_list)
    avg_0, avg_1, avg_2, avg_3 = calc_avg_segm(streets_dict_list)
    print(avg_0, avg_1, avg_2, avg_3)

    A = 0
    with open(outputs[choise], "w+") as f:

        # for each intersection:
        for inter, streets in intersections.items():
            # filter not used streets
            filtered_streets = [s for s in streets if s.n_times_mentioned > 0]

            # Check if this intersection even has any mentioned streets.
            E = len(filtered_streets)            
            if E == 0:
                continue
            # increase total num of intersection scheduled
            A += 1

            f.write(str(inter) + "\n")
            f.write(str(E) + "\n")

            # set time
            calculated_times = calc_proportional_times(filtered_streets)
            for i in range(E):
                #f.write(filtered_streets[i].name + ' ' + (str(calculated_times[i]) if calculated_times[i] < D else str(D)) + '\n')
                #f.write(filtered_streets[i].name + ' ' + str(1) + '\n')

                #if filtered_streets[i].n_times_mentioned > ceil(avg_mentions):
                #    f.write(filtered_streets[i].name + ' ' + str(2) + '\n')
                #else:
                #    f.write(filtered_streets[i].name + ' ' + str(1) + '\n')

                if filtered_streets[i].n_times_mentioned > avg_3:
                    f.write(filtered_streets[i].name + ' ' + str(16) + '\n')
                elif filtered_streets[i].n_times_mentioned > avg_2:
                    f.write(filtered_streets[i].name + ' ' + str(8) + '\n')
                elif filtered_streets[i].n_times_mentioned > avg_1:
                    f.write(filtered_streets[i].name + ' ' + str(4) + '\n')
                elif filtered_streets[i].n_times_mentioned > avg_0:
                    f.write(filtered_streets[i].name + ' ' + str(2) + '\n')
                else:
                    f.write(filtered_streets[i].name + ' ' + str(1) + '\n')
 

            
                

    with open(outputs[choise], "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(str(A).rstrip('\r\n') + '\n' + content)