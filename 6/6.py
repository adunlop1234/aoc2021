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

class LanternFish():
    def __init__(self, timer=8):
        self.timer = timer

    def decrease_timer(self):
        self.timer -= 1

    def check_new_fish_created(self):

        if self.timer == -1:
            self.timer = 6
            return True

        return False

    def __str__(self):
        return "Fish with timer of: " + str(self.timer)

@print_result
def part_one(lines):
    
    for line in lines:

        # Get timers of the initial fish
        timers = line.split(',')

    # Initialise the fish
    all_fish = []
    for timer in timers:
        all_fish.append(LanternFish(int(timer)))

    # Loop over the number of days
    days = 80
    day = 0
    while day < days:
        new_fish = []
        for fish in all_fish:
            fish.decrease_timer()

            if fish.check_new_fish_created():
                new_fish.append(LanternFish())

        all_fish += new_fish

        day += 1
        #print("End of day " + str(day) + ": Number of fish = " + str(len(all_fish)))

    return len(all_fish)


@print_result
def part_two(lines):
    for line in lines:

        # Get timers of the initial fish
        timers = line.split(',')

    # Initialise the fish into groups:
    #   number on the timer
    #   number of fish at this level
    #   need 0-8 on the timer so 9 groups that have timer and number
    #       struct:
    #           'timer' : 'number'
    
    all_fish = {timer:number for timer, number in zip(range(0, 9), [0]*9)}

    for timer in timers:
        all_fish[int(timer)] += 1

    # Loop over the number of days
    days = 256
    day = 0
    while day < days:

        new_all_fish = {timer:number for timer, number in zip(range(0, 9), [0]*9)}

        # All the new fish that are born
        new_all_fish[8] = all_fish[0]

        # Decrease the timer
        for i in range(1, 9):
            new_all_fish[i-1] = all_fish[i]

        # Add the old fish at 0 to 6
        new_all_fish[6] += all_fish[0]

        # Set the current fish to be all of the new ones
        all_fish = new_all_fish.copy()

        # Report after each day the calculation of total fish
        total_fish = sum([number for number in all_fish.values()])

        day += 1
        #print("End of day " + str(day) + ": Number of fish = " + str(total_fish))

    return total_fish


if __name__ == "__main__":
    main()