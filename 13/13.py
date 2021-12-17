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

class Paper():
    def __init__(self, coords):
        max_j = max([l[0] for l in coords]) + 1
        max_i = max([l[1] for l in coords]) + 1

        self.map = np.zeros((max_i, max_j), dtype=bool)

        for coord in coords:
            self.map[coord[1], coord[0]] = True

    def fold(self, axis, location):
        
        # Define the reduced size map after fold to just the top/left portion
        if axis == 'y':
            transparent_map = self.map[location+1:, :]
            transparent_map = np.flip(transparent_map, axis=0)
            start_index = location - (self.map.shape[0] - location) + 1

            self.map = self.map[:location, :]
            self.map[start_index:, :] = (self.map[start_index:, :] | transparent_map)

        if axis == 'x':
            transparent_map = self.map[:, location+1:]
            transparent_map = np.flip(transparent_map, axis=1)
            start_index = location - (self.map.shape[1] - location) + 1

            self.map = self.map[:, :location]
            self.map[:, start_index:] = (self.map[:, start_index:] | transparent_map)

    def __str__(self):
        output = ''
        for row in self.map:
            output += ''.join(['#' if item else '.' for item in row]) + '\n'
        return output[:-1]


@print_result
def part_one(lines):
    
    # Get the data
    fold_instructions = False
    coords = []
    folds = []
    for line in lines:
        if line == '':
            fold_instructions = True
            continue

        if fold_instructions:
            axis, location = line.strip('fold along ').split('=')
            folds.append((axis, int(location)))
        else:
            coords.append([int(line.split(',')[0]), int(line.split(',')[1])])

    # Initialise piece of paper
    paper = Paper(coords)

    # Perform folds
    paper.fold(folds[0][0], folds[0][1])

    return paper.map.sum().sum()

@print_result
def part_two(lines):

    # Get the data
    fold_instructions = False
    coords = []
    folds = []
    for line in lines:
        if line == '':
            fold_instructions = True
            continue

        if fold_instructions:
            axis, location = line.strip('fold along ').split('=')
            folds.append((axis, int(location)))
        else:
            coords.append([int(line.split(',')[0]), int(line.split(',')[1])])

    # Initialise piece of paper
    paper = Paper(coords)

    # Perform folds
    for fold in folds:
        paper.fold(fold[0], fold[1])

    return print(paper)

if __name__ == "__main__":
    main()