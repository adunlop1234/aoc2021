#!/usr/bin/env python3

'''
Template file for each new challenge.
'''

# Import helper functions
import functools
import os, sys

# Specify the filename
VERSION = 1
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

    # Initialise the count and previous value
    previous_value = 10000000000000
    count = 0
    for line in lines:
        current_value = int(line)
        if current_value > previous_value:
            count += 1

        previous_value = current_value

    return count


@print_result
def part_two(lines):
    values = [int(line) for line in lines]

    previous_total = 10000000000000
    count = 0
    for i in range(len(values)-2):
        current_total = sum(values[i:i+3])
        if current_total > previous_total:
            count += 1

        previous_total = current_total

    return count
    

if __name__ == "__main__":
    main()