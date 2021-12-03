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
    number_of_bits = len(lines[0])
    number_of_lines = len(lines)
    input_sequence = np.zeros((number_of_lines, number_of_bits))
    for i, line in enumerate(lines):
        input_sequence[i, :] = np.array(list(line))

    total = input_sequence.sum(axis=0) / number_of_lines

    gamma_rate = "".join([str(int(round(bit))) for bit in total])
    epsilon_rate = "".join([str(1 - int(bit)) for bit in list(gamma_rate)])

    return int(gamma_rate, 2) * int(epsilon_rate, 2)

@print_result
def part_two(lines):
    number_of_bits = len(lines[0])
    number_of_lines = len(lines)
    input_sequence = np.zeros((number_of_lines, number_of_bits))
    for i, line in enumerate(lines):
        input_sequence[i, :] = np.array(list(line))

    oxygen_rating_lines = input_sequence.copy()
    co2_rating_lines = input_sequence.copy()

    i = 0
    while oxygen_rating_lines.shape[0] != 1:
        most_common_bit = oxygen_rating_lines[:, i].sum(axis=0) / oxygen_rating_lines.shape[0]
        if most_common_bit == 0.5:
            most_common_bit = 1
        else:
            most_common_bit = int(round(most_common_bit))

        oxygen_rating_lines = oxygen_rating_lines[oxygen_rating_lines[:, i]==most_common_bit, :]
        i += 1
        
    oxygen_rating = "".join([str(int(bit)) for bit in oxygen_rating_lines[0, :]])

    i = 0
    while co2_rating_lines.shape[0] != 1:
        most_common_bit = co2_rating_lines[:, i].sum(axis=0) / co2_rating_lines.shape[0]
        if most_common_bit == 0.5:
            most_common_bit = 0
        else:
            most_common_bit = 1 - int(round(most_common_bit))

        co2_rating_lines = co2_rating_lines[co2_rating_lines[:, i]==most_common_bit, :]
        i += 1
        
    co2_rating = "".join([str(int(bit)) for bit in co2_rating_lines[0, :]])

    return int(oxygen_rating, 2) * int(co2_rating, 2)

if __name__ == "__main__":
    main()