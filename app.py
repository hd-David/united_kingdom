from flask import Flask, jsonify
import csv
import pprint
from collections import defaultdict , Counter

pp = pprint.PrettyPrinter(indent=4)

list_of_dict = []
with open("uk-towns-sample.csv", "r") as file:
    towns_reader = csv.DictReader(file)
    for town in towns_reader:
        town["easting"] = int(town["easting"])
        town["northing"] = int(town["northing"])
        town["latitude"] = float(town["latitude"])
        town["longitude"] = float(town["longitude"])
        town["elevation"] = int(town["elevation"])
        list_of_dict.append(town)
        #pp.pprint(list_of_dict)

app = Flask(__name__)


""" This function is finding the duplictates names.
    Input - list of dictionaries.  
    Output - list of dictionary for dulpicates names 
"""
@app.route("/names/<name>")
def duplicates_name(name):
    list_of_towns = []
    output_dict = {}
    for town_dict in list_of_dict:
        list_of_towns.append(town_dict["name"])
    counter_of_town = Counter(list_of_towns)
    for key, value in counter_of_town.items():
        if value > 1:
            output_dict[key] = value
    return jsonify(output_dict)


""" This function is filtering all the towns where (Meads) exist.
    Input - list of dictionaries 
    Output - The list of names where Meads exist
"""
@app.route("/mead/<name>")
def meads_in_name(name):
    list_of_town_with_meads = []
    for town in list_of_dict:
        if "Meads" in town["name"]:
            list_of_town_with_meads.append(town)
    return jsonify(list_of_town_with_meads)     


""" This function is finding all towns in between two latitude and longitude.
    Input - Two lists of dictionaries.
    Output - list of towns that are inside the the the given latitude and longitude. 
"""
@app.route("/cities/<lat1>/<long1>/<lat2>/<long2>")
def cities_between_long_lat(lat1, long1, lat2, long2):
    list_of_towns = []
    for town in list_of_dict:
        if town["latitude"] < float(lat1):
                if town["latitude"] > float(lat2):
                    if town["longitude"] > float(long1):               
                        if town["longitude"] < float(long2):
                            list_of_towns.append(town)
    return jsonify(list_of_towns)

""" This function is filtering all towns based on the user input.
    Input -  list of dictionaries.
    Output - strings as the list of dictionaries 
"""
@app.route("/elevations/<min>/<max>")
def towns_above_elevetion_of_100(min,max):
    list_of_towns = []
    for town in list_of_dict:
        if town["elevation"] < int(max):
            if town["elevation"] > int(min):
                list_of_towns.append(town)
    return jsonify(list_of_towns)

""" This function is filtering names of all the villages.
    Input - list of dictionaries.
    Output - list of names whose town type is village
"""
@app.route("/villages/<town_types>")
def all_villages(town_types):
    list_of_villages = []
    for village in list_of_dict:
        if village["town_type"] == town_types:
            list_of_villages.append(village) 
    return jsonify(list_of_villages)