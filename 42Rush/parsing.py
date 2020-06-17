import json
import os
from data_structures import *

def get_routes(path):
    with open(path) as json_file:
        json_data = json.load(json_file)

    stops = []
    routes = []
    for line in json_data:
        stops = []
        for stop in json_data[str(line)]:
            new_stop = stop_area(stop["label"], stop["id"])
            stops.append(new_stop)
        routes.append(route(str(line), stops))
    return (routes)

def get_startpoint(path):
    return(get_stop(path))

def get_endpoint(path):
    return(get_stop(path))

def get_stop(path):
    with open(path) as json_file:
        json_data = json.load(json_file)
        new_stop = stop_area(json_data[0]["label"], json_data[0]["id"])
        return (new_stop)
