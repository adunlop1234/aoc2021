#!/usr/bin/env python3

'''
Template file for each new challenge.
'''

# Import helper functions
import functools
import os, sys
import numpy as np
from collections import Counter

# Specify the filename
VERSION = os.getcwd().split(os.path.sep)[-1].split('.')[0]
EXAMPLE_FILENAME = str(VERSION) + "_EX.txt"
PROBLEM_FILENAME = str(VERSION) + ".txt"

def main():
    
    # Get the input lines for example and full problem
    example_lines = get_input_lines(EXAMPLE_FILENAME)
    problem_lines = get_input_lines(PROBLEM_FILENAME)

    # Perform function one on example and input lines
    part_one(example_lines)
    part_one(problem_lines)

    # Perform function two on example and input lines
    part_two(example_lines)
    part_two(problem_lines)

def print_result(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        output = func(*args, **kwargs)
        print("Output of " + func.__name__ + " is: " + str(output))
        return output
    return wrapper

# Function to read in the lines of the input file
def get_input_lines(filename):
    with open(filename, "r") as f:
        lines = f.read().splitlines()
        return lines

@print_result
def part_one(lines):

    # Create the map dict
    paths = {}
    for line in lines:
        start, end = line.split('-')

        if start in paths.keys():
            paths[start].append(end)
        else:
            paths[start] = [end]
        
        if end in paths.keys():
            paths[end].append(start)
        else:
            paths[end] = [start]

    for key, value in paths.items():
        if 'start' in value:
            paths[key].remove('start')

    # Function to determine if the option is a small cave or not
    def is_small_cave(option):
        if option in ['start', 'end']:
            return False
        
        if option.lower() == option:
            return True

        return False
    
    routes = []
    def find_route(route):

        # Get the last entry into the route to check validity
        current_option = route[-1]
        
        # Create a list of the small caves visited so far in this route
        small_caves = []
        for cave in route[:-1]:
            if is_small_cave(cave):
                small_caves.append(cave)

        # If the latest location is a small cave previously visited then sack it
        if current_option in small_caves:
            return
        
        # If the latest location is the end then add to possible routes
        elif current_option == 'end':
            routes.append(route)
            return

        # Find all the next routes that lead beyond this current option
        for option in paths[current_option]:
            find_route(route + [option])

    # Set the start point and find the routes
    find_route(['start'])

    return len(routes)

@print_result
def part_two(lines):

    # Create the map dict
    paths = {}
    for line in lines:
        start, end = line.split('-')

        if start in paths.keys():
            paths[start].append(end)
        else:
            paths[start] = [end]
        
        if end in paths.keys():
            paths[end].append(start)
        else:
            paths[end] = [start]

    for key, value in paths.items():
        if 'start' in value:
            paths[key].remove('start')

    # Function to determine if the option is a small cave or not
    def is_small_cave(option):
        if option in ['start', 'end']:
            return False
        
        if option.lower() == option:
            return True

        return False
    
    routes = []
    def find_route(route):

        # Get the last entry into the route to check validity
        current_option = route[-1]
        
        # Create a list of the small caves visited so far in this route
        small_caves = []
        for cave in route[:-1]:
            if is_small_cave(cave):
                small_caves.append(cave)
        small_caves = Counter(small_caves)

        # If the latest location is a small cave previously twice or once and another visted twice then sack it
        if current_option in small_caves.keys():
            previous_visits = small_caves[current_option]
            if previous_visits == 2:
                return
            elif previous_visits == 1 and 2 in small_caves.values():
                return
        
        # If the latest location is the end then add to possible routes
        elif current_option == 'end':
            routes.append(route)
            return

        # Find all the next routes that lead beyond this current option
        for option in paths[current_option]:
            find_route(route + [option])

    # Set the start point and find the routes
    find_route(['start'])

    return len(routes)
if __name__ == "__main__":
    main()