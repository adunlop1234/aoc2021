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

@print_result
def part_one(lines):
    
    # Get the numbers
    numbers = [int(number) for number in lines[0].split(',')]
    
    # Store in numpy array and sort
    numbers = np.array(numbers).reshape(-1, 1)
    best_option = int(np.median(numbers))
    min_cost = int(np.absolute(numbers - best_option).sum())

    return "Best option: " + str(int(best_option)) + ". Cost = " + str(int(min_cost))

@print_result
def part_two(lines):

    # Get the numbers
    numbers = [int(number) for number in lines[0].split(',')]
    options = range(0, max(numbers) + 1)

     # Store in numpy array and sort
    numbers = np.array(numbers).reshape(-1, 1)
    totals = {float(n) : (n * (n + 1) * 0.5) for n in range(0, numbers.max() + 1)}

    min_cost = 1000000000000000000000000000000
    best_option = 0
    for option in options:
        deltas = np.absolute(numbers - option)
        cost = 0
        for delta in deltas[:, 0]:
            cost += totals[float(delta)]

        if cost < min_cost:
            min_cost = min(cost, min_cost)
            best_option = option

    return "Best option: " + str(int(best_option)) + ". Cost = " + str(int(min_cost))

if __name__ == "__main__":
    main()