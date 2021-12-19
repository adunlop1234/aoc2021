#!/usr/bin/env python3

'''
Template file for each new challenge.
'''

# Import helper functions
import functools
import os, sys
import numpy as np
import math

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
    '''
    Derived equation of motion at discrete timesteps: 
        x = vx * n + n - n * (n + 1) * 0.5 for 0 <= n  <= vx, for n > vx x = x(n=vx)
        y = vy * n + n - n * (n + 1) * 0.5 for all n
    Maximum values occur a x = vx and y = vy
    '''

    # Get input
    x_text, y_text = lines[0].split(' ')[2:]
    x_min = int(x_text.split('=')[1].split('..')[0])
    x_max = int((x_text.split('..')[1])[:-1])
    y_min = int(y_text.split('=')[1].split('..')[0])
    y_max = int(y_text.split('..')[1])

    # Loop through all of the possible
    vy = 0
    biggest_vy = 0
    while True:
        
        # Check if the timestep at which it would enter the target was an integer
        n1 = 0.5 * ((2*vy + 1) + math.sqrt(((2*vy + 1)**2)-8*y_max))
        n2 = 0.5 * ((2*vy + 1) + math.sqrt(((2*vy + 1)**2)-8*y_min))

        # Record the biggest vy if time is an integer
        if math.floor(n2) == math.ceil(n1):
            biggest_vy = max(vy, biggest_vy)

        # Increment vy
        vy += 1
        if vy == 100000:
            break

    # Get the max height
    max_height = 0.5 * biggest_vy * (biggest_vy + 1)
    return int(max_height)

@print_result
def part_two(lines):
    '''
    Derived equation of motion at discrete timesteps: 
        x = vx * n + n - n * (n + 1) * 0.5 for 0 <= n  <= vx, for n > vx x = x(n=vx)
        y = vy * n + n - n * (n + 1) * 0.5 for all n
    Maximum values occur a x = vx and y = vy
    '''

    # Get input
    x_text, y_text = lines[0].split(' ')[2:]
    x_min = int(x_text.split('=')[1].split('..')[0])
    x_max = int((x_text.split('..')[1])[:-1])
    y_min = int(y_text.split('=')[1].split('..')[0])
    y_max = int(y_text.split('..')[1])

    # Loop through all of the possible and find all possible vy
    possible_vys = []
    vy = 0
    while True:
        
        # Check if the timestep at which it would enter the target was an integer
        n1 = 0.5 * ((2*vy + 1) + math.sqrt(((2*vy + 1)**2)-8*y_max))
        n2 = 0.5 * ((2*vy + 1) + math.sqrt(((2*vy + 1)**2)-8*y_min))

        # Record the biggest vy if time is an integer
        if math.floor(n2) == math.ceil(n1) or abs(n1 - n2) >= 1:
          possible_vys.append([vy, math.ceil(n1), math.floor(n2)])

        # Check for negative vy
        vy *= -1

        # Check if the timestep at which it would enter the target was an integer
        n1 = 0.5 * ((2*vy + 1) + math.sqrt(((2*vy + 1)**2)-8*y_max))
        n2 = 0.5 * ((2*vy + 1) + math.sqrt(((2*vy + 1)**2)-8*y_min))

        # Record the biggest vy if time is an integer
        if math.floor(n2) == math.ceil(n1) or abs(n1 - n2) >= 1 and not vy == 0:
            possible_vys.append([vy, math.ceil(n1), math.floor(n2)])

        # Revert vy to positive
        vy *= -1

        # Increment vy
        vy += 1
        if vy == 100000:
            break

    #possible_vys = sorted(possible_vys)
    velocities = []
    for vy, n1, n2 in possible_vys:

        nmin = min(n1, n2)
        nmax = max(n1, n2)
        ns = range(n1, n2+1)

        # Loop over all of the n1/n2, x_min, x_max combinations
        vmin = 1000000000000000
        vmax = -vmin
        for n in ns:

            # Check the velocity for xmax and xmin for n <= vx
            v1 = x_min/n + 0.5*(n-1)
            if n <= v1:
                vmin = min(vmin, v1)
                vmax = max(vmax, v1)

            v2 = x_max/n + 0.5*(n-1)
            if n <= v2:
                vmin = min(vmin, v2)
                vmax = max(vmax, v2)

            # Check the velocity for xmax and xmin for n >= vx
            v3 = -0.5 + 0.5 * math.sqrt(1 + 8*x_min)
            v4 = -0.5 + 0.5 * math.sqrt(1 + 8*x_max)
            if n >= v3:
                vmin = min(vmin, v3)
                vmax = max(vmax, v3)
            if n >= v4:
                vmin = min(vmin, v4)
                vmax = max(vmax, v4)

        vxs = range(math.ceil(vmin), math.floor(vmax)+1)

        for vx in vxs:
            velocities.append([vx, vy])
    
    return len(velocities)

if __name__ == "__main__":
    main()