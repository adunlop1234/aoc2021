#!/usr/bin/env python3

'''
Template file for each new challenge.
'''

# Import helper functions
import functools
import os, sys
from posixpath import join
import numpy as np
from numpy.lib.arraypad import pad

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

    # Initialise grid
    i_max = len(lines)
    j_max = len(lines[0])
    grid = np.zeros((i_max, j_max))
    for i, line in enumerate(lines):
        grid[i, :] = np.array([int(num) for num in list(line)]).reshape(1, -1)

    # Add padding with constant of 9.9
    padding = 9.9 * np.ones((i_max + 2, j_max + 2))
    for i, row in enumerate(grid):
        padding[i + 1, 1:-1] = row

    # Perform algorithm
    risk = 0
    for i in range(1, i_max + 1):
        for j in range(1, j_max + 1):
            value = padding[i, j]
            left = padding[i, j-1]
            right = padding[i, j+1]
            above = padding[i-1, j]
            below = padding[i+1, j]

            if value < left and value < right and value < above and value < below:
                risk += value + 1

    return risk

class Basin():
    def __init__(self, map, initial_location):
        self.size = 0
        self.map = map
        self.location = initial_location
        self.i = initial_location[0]
        self.j = initial_location[1]
        self.queue = [(self.i, self.j)]

    def add_to_queue(self, location):
        if location not in self.queue:
            self.queue.append(location)

    def get_from_queue(self):
        self.location = self.queue.pop()
        self.i = self.location[0]
        self.j = self.location[1]

    def check_around(self):

        # Set current location to false and increase size count
        self.map[self.i, self.j] = False
        self.size += 1

        # Check cardinal directions
        if self.map[self.i + 1, self.j]:
            self.add_to_queue((self.i + 1, self.j))

        if self.map[self.i - 1, self.j]:
            self.add_to_queue((self.i - 1, self.j))

        if self.map[self.i, self.j + 1]:
            self.add_to_queue((self.i ,self.j + 1))

        if self.map[self.i, self.j - 1]:
            self.add_to_queue((self.i, self.j - 1))        


    def explore_basin(self):

        while len(self.queue):
            self.check_around()
            self.get_from_queue()

        return self.size, self.map

@print_result
def part_two(lines):

    # Initialise grid
    i_max = len(lines)
    j_max = len(lines[0])
    grid = np.zeros((i_max, j_max))
    for i, line in enumerate(lines):
        grid[i, :] = np.array([int(num) for num in list(line)]).reshape(1, -1)

    # Add padding with constant of 9.9
    padding = 9 * np.ones((i_max + 2, j_max + 2))
    for i, row in enumerate(grid):
        padding[i + 1, 1:-1] = row

    # Turn the array into a boolean map
    padding[padding == 9] = -1
    valid = padding >= 0

    # Loop until all of the basins have been found
    valid_remaining = valid.sum().sum()
    basin_size = []
    while valid_remaining:

        # Plonk the agent into a random true location
        locations = np.where(valid)
        initial_location = (locations[0][0], locations[1][0])
        
        # Explore the basin to get the full size
        basin = Basin(valid, initial_location)
        size, valid = basin.explore_basin()
        basin_size.append(size)

        # Check how many remaining
        valid_remaining = valid.sum().sum()
    
    basin_size = sorted(basin_size)

    return basin_size[-1] * basin_size[-2] * basin_size[-3]

if __name__ == "__main__":
    main()