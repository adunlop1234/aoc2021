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
    
    opening_characters = ['(', '[', '{', '<']
    closing_characters = [')', ']', '}', '>']
    valid_closing_characters = {opening : closing for opening, closing in zip(opening_characters, closing_characters)}
    closing_character_score = {closing : score for closing, score in zip(closing_characters, [3, 57, 1197, 25137])}

    stack = []
    score = 0

    for line in lines:

        for character in list(line):
            if character in opening_characters:
                stack.append(character)

            elif character in closing_characters:
                if valid_closing_characters[stack.pop(-1)] != character:
                    #print("Invalid closing character found: " + character)
                    score += closing_character_score[character]
                    break

    return score

@print_result
def part_two(lines):

    opening_characters = ['(', '[', '{', '<']
    closing_characters = [')', ']', '}', '>']
    valid_closing_characters = {opening : closing for opening, closing in zip(opening_characters, closing_characters)}
    closing_character_score = {closing : score for closing, score in zip(closing_characters, [1, 2, 3, 4])}

    scores = []

    for line in lines:
        incomplete_line = True
        score = 0
        stack = []
        for character in list(line):
            if character in opening_characters:
                stack.append(character)

            elif character in closing_characters:
                if valid_closing_characters[stack.pop(-1)] != character:
                    incomplete_line = False
                    break
        
        if incomplete_line:
            for character in reversed(stack):
                score *= 5
                score += closing_character_score[valid_closing_characters[character]]

            scores.append(score)

    return sorted(scores)[int(len(scores)/2)]

if __name__ == "__main__":
    main()