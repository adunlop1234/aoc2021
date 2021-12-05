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

# Create vents grid class
class Vents_Diagram():
    def __init__(self, x_size, y_size):
        self.grid = np.zeros((y_size, x_size))

    def add_vector(self, coords1, coords2):

        if coords1['x'] == coords2['x']:
            y1 = min(coords1['y'], coords2['y'])
            y2 = max(coords1['y'], coords2['y'])
            self.grid[y1:y2+1, coords1['x']] += 1.0
        elif coords1['y'] == coords2['y']:
            x1 = min(coords1['x'], coords2['x'])
            x2 = max(coords1['x'], coords2['x'])
            self.grid[coords1['y'], x1:x2+1] += 1.0
        else:
            ys = [int(y) for y in np.linspace(coords1['y'], coords2['y'], abs(coords1['y'] - coords2['y']) + 1)]
            xs = [int(x) for x in np.linspace(coords1['x'], coords2['x'], abs(coords1['y'] - coords2['y']) + 1)]
            self.grid[(np.array(ys), np.array(xs))] += 1.0

    def get_sum_multiple_vents(self):
        return (self.grid > 1).sum().sum()


@print_result
def part_one(lines):

    # Initialise lines array
    vent_lines = []
    x_size = -1
    y_size = -1

    for line in lines:

        # Get the coordinates
        line = line.replace(' ', '')
        coords = line.split('->')
        x1, y1 = coords[0].split(',')
        x2, y2 = coords[1].split(',')

        # Do consistency check to only include horizontal/vertical lines
        if x1 != x2 and y1 != y2:
            continue

        # Store the lines
        coords1 = {'x' : int(x1), 'y' : int(y1)}
        coords2 = {'x' : int(x2), 'y' : int(y2)}
        vent_lines.append((coords1, coords2))

        # Get the max x and max y to create the shape of the grid
        x_size = max(x_size, coords1['x'], coords2['x'])
        y_size = max(y_size, coords1['y'], coords2['y'])

    # Initialise vent grid
    vents = Vents_Diagram(x_size + 1, y_size + 1)

    # Loop through each line and add to the vents diagram
    for line in vent_lines:
        vents.add_vector(line[0], line[1])

    # Get number of places > 1
    return vents.get_sum_multiple_vents()
        

@print_result
def part_two(lines):

    # Initialise lines array
    vent_lines = []
    x_size = -1
    y_size = -1

    for line in lines:

        # Get the coordinates
        line = line.replace(' ', '')
        coords = line.split('->')
        x1, y1 = coords[0].split(',')
        x2, y2 = coords[1].split(',')

        # Store the lines
        coords1 = {'x' : int(x1), 'y' : int(y1)}
        coords2 = {'x' : int(x2), 'y' : int(y2)}
        vent_lines.append((coords1, coords2))

        # Get the max x and max y to create the shape of the grid
        x_size = max(x_size, coords1['x'], coords2['x'])
        y_size = max(y_size, coords1['y'], coords2['y'])

    # Initialise vent grid
    vents = Vents_Diagram(x_size + 1, y_size + 1)

    # Loop through each line and add to the vents diagram
    for line in vent_lines:
        vents.add_vector(line[0], line[1])

    # Get number of places > 1
    return vents.get_sum_multiple_vents()

if __name__ == "__main__":
    main()