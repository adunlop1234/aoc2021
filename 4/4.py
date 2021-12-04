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

# Object for the board
class Board_One():
    def __init__(self, x_dim, y_dim):
        self.board = np.zeros((y_dim, x_dim))
        self.selected = np.zeros((y_dim, x_dim))

    def add_row(self, row, index):
        self.board[index, :] = row.reshape((1, -1))

    def update_number(self, number):
        selected_index = (self.board == float(number))
        self.selected[selected_index] += 1

    def is_complete(self):
        if (self.selected.sum(axis=0)==5).any() or (self.selected.sum(axis=1)==5).any():
            return True
        return False

    def sum_unmarked(self):
        return self.board[np.where(np.ones(self.selected.shape) - self.selected)].sum().sum()

@print_result
def part_one(lines):

    # Get the numbers
    numbers = lines[0].split(',')

    # Read in all of the boards
    boards = []
    current_board = Board_One(5, 5)
    i = 0
    for line in lines[2:]:
        if line == '':
            i = 0
            boards.append(current_board)
            current_board = Board_One(5, 5)
            continue

        current_board.add_row(np.array(line.split()), i)
        i += 1

        if line == lines[-1]:
            boards.append(current_board)

    for number in numbers:
        for board in boards:
            board.update_number(number)
            if board.is_complete():
                return int(float(number) * board.sum_unmarked())


@print_result
def part_two(lines):
    # Get the numbers
    numbers = lines[0].split(',')

    # Read in all of the boards
    boards = []
    current_board = Board_One(5, 5)
    i = 0
    board_count = 0
    for line in lines[2:]:
        if line == '':
            i = 0
            boards.append(current_board)
            current_board = Board_One(5, 5)
            board_count += 1
            continue

        current_board.add_row(np.array(line.split()), i)
        i += 1

        if line == lines[-1]:
            boards.append(current_board)
            board_count += 1

    board_complete_number = np.zeros((board_count, 1))
    for number in numbers:
        for i, board in enumerate(boards):
            board.update_number(number)
            if board_complete_number[i, 0] != 1 and board.is_complete():
                board_complete_number[i, 0] = 1

            if board_complete_number.sum().sum() == board_count:
                return int(float(number) * board.sum_unmarked())

if __name__ == "__main__":
    main()