#!/usr/bin/env python3

'''
Template file for each new challenge.
'''

# Import helper functions
import functools
import os, sys
import numpy as np
from collections import Counter, defaultdict

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

    # Get initial polymer and rules
    polymer = lines[0]
    rules = dict()
    for line in lines[2:]:
        rules[line.split(' -> ')[0]] = line.split(' -> ')[1]

    step = 0
    while step < 10:
        matched_patterns = []
        for pattern in rules.keys():
            if pattern in polymer:
                index = polymer.find(pattern)
                matched_patterns.append((index, pattern))
                while True:
                    if pattern in polymer[index+1:]:
                        index += polymer[index+1:].find(pattern) + 1
                        matched_patterns.append((index, pattern))
                    else: 
                        break

        matched_patterns = sorted(matched_patterns, key=lambda x: x[0], reverse=True)

        for index, pattern in matched_patterns:
            polymer = polymer[:index+1] + rules[pattern] + polymer[index+1:]

        step += 1

    values = list(Counter(list(polymer)).values())

    return max(values) - min(values)

@print_result
def part_two(lines):

    # Get initial polymer and rules
    polymer = lines[0]
    rules = dict()
    for line in lines[2:]:
        rules[line.split(' -> ')[0]] = line.split(' -> ')[1]

    polymer_count = Counter([polymer[i:i+2] for i in range(len(polymer)-1)])
    letter_count = Counter(list(polymer))
    step = 0
    while step < 40:

        # Creates n * first + replace and n * second + replce
        new_polymer_count = polymer_count.copy()
        for pattern in polymer_count.keys():

            # Increase the number of letters for the letter added
            letter_count[rules[pattern]] += polymer_count[pattern]

            # As splitting original pattern remove the number of those
            new_polymer_count[pattern] -= polymer_count[pattern]

            new_patterns = [pattern[0] + rules[pattern], rules[pattern] + pattern[1]]
            for new_pattern in new_patterns:
                new_polymer_count[new_pattern] += polymer_count[pattern]                

        polymer_count = new_polymer_count.copy()

        step += 1

    # Remove all letter counts that have a value of 0
    letter_count_values = [value for value in letter_count.values() if value != 0]

    return max(letter_count_values) - min(letter_count_values)

if __name__ == "__main__":
    main()