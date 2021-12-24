#!/usr/bin/env python3

'''
Template file for each new challenge.
'''

# Import helper functions
import functools
import os, sys
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
    algorithm = lines[0]
    image = np.array([[0 if item == '.' else 1 for item in line] for line in lines[2:]], dtype=int)
    return enhance_image(image, algorithm, 2)

@print_result
def part_two(lines):
    algorithm = lines[0]
    image = np.array([[0 if item == '.' else 1 for item in line] for line in lines[2:]], dtype=int)
    return enhance_image(image, algorithm, 50)

def enhance_image(image, algorithm, steps):
    padding_amount = 100
    image = np.pad(image, padding_amount)

    new_image = np.zeros(image.shape, dtype=int)
    i_max, j_max = image.shape[0]-1, image.shape[1]-1

    step = 0
    #for row in image:
        #print(''.join(['#' if item else '.' for item in row]))
    while step < steps:
        for i, row in enumerate(image):
            if i == 0 or i == i_max:
                continue
            for j, item in enumerate(row):
                if j == 0 or j == j_max:
                    continue
                
                converted_number = ''
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        #print(image[i+a, j+b])
                        converted_number += str(image[i+a, j+b])

                converted_number = algorithm[int(converted_number, 2)]
                if converted_number == '#': 
                    converted_number = 1
                else: 
                    converted_number = 0
                new_image[i, j] = converted_number

        step += 1
        image = new_image.copy()
        for row in new_image:
            #print(''.join(['#' if item else '.' for item in row]))
            pass
        print(step)
    
    #print(padding_amount, i_max, j_max)
    delta = steps+1
    return image[padding_amount-delta:i_max-padding_amount+delta, padding_amount-delta:j_max-padding_amount+delta].sum().sum()

if __name__ == "__main__":
    main()