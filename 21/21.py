#!/usr/bin/env python3

'''
Template file for each new challenge.
'''

# Import helper functions
import functools
import os, sys
from collections import Counter
import numpy as np
import time
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

class Player:
    def __init__(self, start_number, score=0):
        self.location = start_number
        self.score = score

    def update_position(self, roll_number):
        self.location = (self.location + roll_number) % 10
        if self.location == 0:
            self.location = 10
        self.score += self.location

    def __str__(self):
        return 'Location: ' + str(self.location) + ' | Score ' + str(self.score)

def deterministic_dice_roll(number):
    if not number % 100:
        return 100
    return (number % 100)

@print_result
def part_one(lines):
    
    # Read in starting positions
    starting_1 = int(lines[0].split(':')[1].strip())
    starting_2 = int(lines[1].split(':')[1].strip())

    # Initialise players
    player_1 = Player(starting_1)
    player_2 = Player(starting_2)

    # Loop until score is 1000
    roll_number = 0
    while True:
        
        # Increase dice total
        dice_total = sum([deterministic_dice_roll(roll_number + number) for number in range(1, 4)])
        roll_number += 3

        # Check if player finished
        player_1.update_position(dice_total)
        if player_1.score >= 1000:
            return player_2.score * roll_number

        # Increase dice total
        dice_total = sum([deterministic_dice_roll(roll_number + number) for number in range(1, 4)])
        roll_number += 3
        
        # Check if player finished
        player_2.update_position(dice_total)
        if player_2.score >= 1000:
            return player_1.score * roll_number           

def update_position(location, score, dice_score):
    location = (location + dice_score) % 10
    if location == 0:
        location = 10
    score += location

    return location, score

# Define the permutations
PERMS = {3:1, 4:3, 5:6, 6:7, 7:6, 8:3, 9:1}

def quantum_game(player_1_location, player_1_score, player_2_location, player_2_score, current_player, dice_score):

    if current_player == 1:
        location = player_1_location
        score = player_1_score
        next_player = 2
    elif current_player == 2:
        location = player_2_location
        score = player_2_score
        next_player = 1

    wins = np.zeros((1, 2), dtype=int)
    
    # Add total to player
    location, score = update_position(location, score, dice_score)
    if score >= 21:
        if current_player == 1:
            wins[0, 0] = 1
        elif current_player == 2:
            wins[0, 1] = 1

        return wins

    # Assign back to player1/2
    if current_player == 1:
        player_1_location = location
        player_1_score = score
    elif current_player == 2:
        player_2_location = location
        player_2_score = score

    for next_score, multiples in PERMS.items():
        result = quantum_game(player_1_location, player_1_score, player_2_location, player_2_score, next_player, next_score)
        wins += multiples * result

    return wins

@print_result
def part_two(lines):
    
    # Brute force solution that takes advantage of the resultant outcomes of 3 dice rolls but takes a long time
    # Could have used dynamic programming/memoisation but since brute force worked didn't bother

    # Read in starting positions
    starting_1 = int(lines[0].split(':')[1].strip())
    starting_2 = int(lines[1].split(':')[1].strip())

    # Get the permutations for each dice roll
    perms = []
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                perms.append(i + j + k)
    perms = Counter(perms)

    wins = np.zeros((1, 2), dtype=int)
    for score, multiples in PERMS.items():
        wins += multiples * quantum_game(starting_1, 0, starting_2, 0, 1, score)
    
    return wins.max().max()

if __name__ == "__main__":
    main()