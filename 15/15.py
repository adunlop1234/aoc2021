#!/usr/bin/env python3

'''
Template file for each new challenge.
'''

# Import helper functions
import functools
import os, sys
import numpy as np

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

MASK = [(-1, 0), (0, -1), (0, 1), (1, 0)]

class Area():

    def __init__(self, i, j, total, previous_visited_list):
        self.location = (i, j)
        self.total = total
        self.previous_visited_list = previous_visited_list

@print_result
def part_one(lines):
    '''
    Implementing Dijkstra's algorithm from: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    '''

    # Get the costs grid
    cost = np.zeros((len(lines), len(lines[0])), dtype=int)
    for i, line in enumerate(lines):
        cost[i, :] = np.array(list(line))

    # Create a checked and totals set of nodes
    checked = np.zeros(cost.shape, dtype=bool)
    totals = 100000000000000 * np.ones(cost.shape, dtype=int)

    # Initialise the total of the starting node to 0
    totals[0, 0] = 0
    location = (0, 0)

    while True:
        options = [(location[0] + a, location[1] + b) for a, b in MASK if 0 <= location[0] + a <= cost.shape[0] - 1 and 0 <= location[1] + b <= cost.shape[1] - 1]

        for option in options:
            totals[option] = min(totals[option], totals[location] + cost[option])

        checked[location] = True

        if checked.all():
            break

        temp_totals = totals.copy()
        temp_totals[checked] = 100000000000000

        locations = np.where(temp_totals == temp_totals[~checked].min().min())
        location = (locations[0][0], locations[1][0])

    return totals[cost.shape[0] - 1, cost.shape[1] - 1]


@print_result
def part_two(lines):
    '''
    Implementing Dijkstra's algorithm from: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    '''

    # Get the costs grid
    cost = np.zeros((len(lines), len(lines[0])), dtype=int)
    for i, line in enumerate(lines):
        cost[i, :] = np.array(list(line))

    # Create bigger cost array
    big_cost = np.tile(cost, (5, 5))
    dim_i, dim_j = cost.shape

    for i in range(0, 5):
        for j in range (0, 5):
            big_cost[dim_i * i:dim_i * (i+1), dim_j * j:dim_j * (j+1)] += i + j

    mask = big_cost > 9
    big_cost[mask] -= 9
    cost = big_cost.copy()

    # Create a checked and totals set of nodes
    checked = np.zeros(cost.shape, dtype=bool)
    totals = 100000000000000 * np.ones(cost.shape, dtype=int)

    # Initialise the total of the starting node to 0
    totals[0, 0] = 0
    location = (0, 0)

    while True:
        options = [(location[0] + a, location[1] + b) for a, b in MASK if 0 <= location[0] + a <= cost.shape[0] - 1 and 0 <= location[1] + b <= cost.shape[1] - 1]

        for option in options:
            totals[option] = min(totals[option], totals[location] + cost[option])

        checked[location] = True

        if checked.all():
            break

        temp_totals = totals.copy()
        temp_totals[checked] = 100000000000000

        locations = np.where(temp_totals == temp_totals[~checked].min().min())
        location = (locations[0][0], locations[1][0])

    return totals[cost.shape[0] - 1, cost.shape[1] - 1]

if __name__ == "__main__":
    main()