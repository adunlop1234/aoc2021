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
    
    valid_lengths = {2, 3, 4, 7}
    count = 0

    for line in lines:
        after = line.split('|')[1]
        phrases = after.split(' ')[1:]
        for phrase in phrases:
            if len(phrase) in valid_lengths:
                count += 1

    return count

@print_result
def part_two(lines):

    total = 0
    count = 0

    for line in lines:
        empty_set = set()
        conversion = {number : set() for number in range(0, 10)}
        before, after = line.split('|')

        # Identify the correct conversion matrix
        numbers = before.split(' ')[:-1]
        numbers_identified = 0

        for number in numbers:
            number_length = len(number)
            if number_length == 2:
                conversion[1] = set(number)
                numbers_identified += 1
            elif number_length == 3:
                conversion[7] = set(number)
                numbers_identified += 1
            elif number_length == 4:
                conversion[4] = set(number)
                numbers_identified += 1
            elif number_length == 7:
                conversion[8] = set(number)
                numbers_identified += 1
        
        four_distinct = conversion[4] - conversion[1]
        top_line = conversion[7] - conversion[1]
        five_found = False
        three_found = False
        nine_found = False
        six_found = False
        zero_found = False
        two_found = False

        if count == 1:
            print(conversion)

        while numbers_identified != 10:
            for number in numbers:
                number_length = len(number)

                if number_length == 5:
                    if not five_found and not len(four_distinct - set(number)):
                        conversion[5] = set(number)
                        five_found = True
                        numbers_identified += 1
                    elif not three_found and five_found and not len(conversion[1] - set(number)):
                        conversion[3] = set(number)
                        three_found = True
                        numbers_identified += 1
                    elif five_found and three_found and not two_found and len(conversion[1] - set(number)) and len(four_distinct - set(number)):
                        conversion[2] = set(number)
                        two_found = True
                        numbers_identified += 1

                elif number_length == 6:
                    if not zero_found and len(four_distinct - set(number)):
                        conversion[0] = set(number)
                        zero_found = True
                        numbers_identified += 1
                    elif not nine_found and zero_found and not len(conversion[1] - set(number)):
                        conversion[9] = set(number)
                        nine_found = True
                        numbers_identified += 1
                    elif nine_found and zero_found and not six_found and not len(four_distinct - set(number)) and len(conversion[1] - set(number)):
                        conversion[6] = set(number)
                        six_found = True
                        numbers_identified += 1

                if numbers_identified == 10:
                    break

        # Find the number
        digits = after.split(' ')[1:]
        output_value = 0
        for i, digit in enumerate(digits):
            for number, code in conversion.items():
                if len(code.intersection(set(digit))) == len(digit) and len(digit) == len(code):
                    output_value += number * (10**(3-i))

        total += output_value

    return total

# Lengths
# 2 = 1
# 3 = 7
# 4 = 4
# 5 = 2, 3, 5
# 6 = 0, 6, 9
# 7 = 8

# 1, 4, 7, 8 all identified by length

# 5 identified by length 5 and shares two distinct in 4
# 3 identified by length 5 and shares two in 1
# 2 identified by length 5 and not 3 or 5

# 0 identified by length 6 and doesn't have both the ones from 4
# 9 identified by length 6 and shares two in 1
# 6 identified by length 6, doesn't have both from 1 and shares both from 4
# 0 identified by length 6 and not 9 or 6

# 1 is the two on the right
# 7 is the two on the right and the one on top, can identify the 1 on top
# 4 tells you the middle and top left

if __name__ == "__main__":
    main()