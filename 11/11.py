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

MASK = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

class Octopus_Map():
    def __init__(self, map):
        self.map = map
        self.has_flashed = np.zeros(map.shape)
        self.flashes = 0

    def next_step(self):
        self.increase_by_one()
        self.check_flashes()

    def increase_by_one(self):
        self.map += 1

    def check_flashes(self):

        self.has_flashed = np.zeros(self.map.shape)

        # Loop until the initial map is same as final map
        while True:

            # Get all that is above 9 and set to 0 the rest
            flash_location = self.map > 9.0
            self.has_flashed[flash_location] += 1
            self.map[flash_location] = 0

            # Increase all of the 
            flash_indicies = [(i, j) for i, j in zip(np.where(flash_location)[0], np.where(flash_location)[1])]
            flashed_indicies = [(i, j) for i, j in zip(np.where(self.has_flashed)[0], np.where(self.has_flashed)[1])]

            # Return if there are no more areas to flash
            if not len(flash_indicies):
                return self.flashes

            increment_location = []
            for i, j in flash_indicies:
                for a, b in MASK:
                    new_index = (i + a, j + b)
                    if new_index not in flashed_indicies and (0 <= i + a <= 9 and 0 <= j + b <= 9):
                        increment_location.append(new_index)

            # Increment the locations
            for (i, j), value in Counter(increment_location).items():
                self.map[i, j] += value

            self.map[flash_location] = 0

            # Get number of flashes
            self.flashes += len(flash_indicies)

@print_result
def part_one(lines):
    
    # Create map and instance the map
    initial_map = np.zeros((len(lines), len(lines[0])))
    for i, line in enumerate(lines):
        initial_map[i, :] = np.array(list(line))

    octoMap = Octopus_Map(initial_map)

    steps = 100
    step = 0
    while step < steps:

        octoMap.next_step()
        step += 1

    return octoMap.flashes

@print_result
def part_two(lines):
    
    # Create map and instance the map
    initial_map = np.zeros((len(lines), len(lines[0])))
    for i, line in enumerate(lines):
        initial_map[i, :] = np.array(list(line))

    octoMap = Octopus_Map(initial_map)

    step = 0
    while True:

        octoMap.next_step()
        step += 1

        if octoMap.map.sum().sum() == 0:
            return step

if __name__ == "__main__":
    main()