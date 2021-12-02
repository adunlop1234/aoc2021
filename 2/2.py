#!/usr/bin/env python3

'''
Template file for each new challenge.
'''

# Import helper functions
import functools
import os, sys

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
    
    depth = 0
    horizontal = 0
    for line in lines:
        command, value = line.split(' ')

        if command == 'forward':
            horizontal += int(value)
        elif command == 'down':
            depth += int(value)
        elif command == 'up':
            depth -= int(value)

    return depth * horizontal

@print_result
def part_two(lines):

    aim = 0
    depth = 0
    horizontal = 0
    for line in lines:
        command, value = line.split(' ')

        if command == 'forward':
            horizontal += int(value)
            depth += int(value) * aim
        elif command == 'down':
            aim += int(value)
        elif command == 'up':
            aim -= int(value)

    return depth * horizontal

if __name__ == "__main__":
    main()