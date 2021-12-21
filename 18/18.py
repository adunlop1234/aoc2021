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

class Entry():
    def __init__(self, value, side, parent=None):
        self.value = value
        self.parent = parent
        self.side = side

    def is_entry(self):
        return True

    def traverse_right(self):
        if self.side == 'left':
            if self.parent.right.is_entry():
                return self.parent.right
            else:
                return self.parent.right.traverse_down_left()

        else:
            return self.parent.get_right_entry()

    def __str__(self):
        return str(self.value)

class Pair():
    def __init__(self, left, right, side=None, parent=None):
        
        self.parent = parent
        self.side = side

        if isinstance(left, list):
            self.left = Pair(left[0], left[1], 'left', parent=self)
        else:
            self.left = Entry(left, 'left', parent=self)

        if isinstance(right, list):
            self.right = Pair(right[0], right[1], 'right', parent=self)
        else:
            self.right = Entry(right, 'right', parent=self)         

    def find_explode(self, depth=0):
        
        # Loop through all to find one at depth of 4
        possible = []

        depth += 1
        if depth == 4:
            if not self.left.is_entry():
                possible += [self.left]
            
            if not self.right.is_entry():
                possible += [self.right]

        else:
            if not self.left.is_entry():
                possible += self.left.find_explode(depth)

            if not self.right.is_entry():
                possible += self.right.find_explode(depth)

        return possible

    def explode(self):
        '''
        Recieves the pair to be exploded and performs explosion.
        '''
        left_entry = self.get_left_entry()
        right_entry = self.get_right_entry()

        if left_entry != None:
            left_entry.value += self.left.value

        if right_entry != None:
            right_entry.value += self.right.value

        if self.side == 'left':
            self.parent.left = Entry(0, self.side, parent=self.parent)
        else:
            self.parent.right = Entry(0, self.side, parent=self.parent)

    def find_splits(self):

        current = self.traverse_down_left()

        while True:
            
            if current == None:
                return None

            if current.value > 9:
                return [current.parent, current.side]

            current = current.traverse_right()

    def split(self, location):

        if location == 'left':
            value = self.left.value
            left = math.floor(0.5*value)
            right = math.ceil(0.5*value)
            new_pair = Pair(left, right, side=location, parent=self)
            self.left = new_pair
        else:
            value = self.right.value
            left = math.floor(0.5*value)
            right = math.ceil(0.5*value)
            new_pair = Pair(left, right, side=location, parent=self)
            self.right = new_pair

    def magnitude(self):

        if self.left.is_entry():
            mag_left = self.left.value
        else:
            mag_left = self.left.magnitude()

        if self.right.is_entry():
            mag_right = self.right.value
        else:
            mag_right = self.right.magnitude()

        return 3 * mag_left + 2 * mag_right

    def get_right_entry(self):

        if self.side == 'left':
            if self.parent.right.is_entry():
                return self.parent.right
            else:
                return self.parent.right.traverse_down_left()

        elif self.side == 'right':
            return self.parent.get_right_entry()

    def get_left_entry(self):

        if self.side == 'right':
            if self.parent.left.is_entry():
                return self.parent.left
            else:
                return self.parent.left.traverse_down_right()

        elif self.side == 'left':
            return self.parent.get_left_entry()

    def traverse_down_left(self):
        if self.left.is_entry():
            return self.left
        else:
            return self.left.traverse_down_left()

    def traverse_down_right(self):
        if self.right.is_entry():
            return self.right
        else:
            return self.right.traverse_down_right()

    def is_entry(self):
        return isinstance(self, Entry)

    def __str__(self):
        output = ''
        if isinstance(self.left, int) and isinstance(self.right, int):
            output += '[' + str(self.left) + ',' + str(self.right) + ']'
        elif not isinstance(self.left, int) and not isinstance(self.right, int):
            output += '[' + str(self.left) + ',' + str(self.right) + ']'
        else:
            if isinstance(self.left, int):
                output += '[' + str(self.left) + ','
            else:
                output += '[' + str(self.left)

            if isinstance(self.right, int):
                output += ',' + str(self.right) + ']'
            else:
                output += str(self.right) + ']'

        return output

@print_result
def part_one(lines):
    
    parsed = eval(lines[0])
    tree = Pair(parsed[0], parsed[1])

    for line in lines[1:]:

        # Perform tree addition
        parsed = eval(line)
        old_tree = eval(str(tree))
        #print("Addition:  " + str(old_tree) + ' + ' + str(parsed))
        tree = Pair(old_tree, parsed)
        #print("Addition:  " + str(tree))
        old_tree = ''

        # Loop until number reduced
        while True:
            
            old_tree = str(tree)

            # Perform explosion
            explodes = tree.find_explode()
            for explode in explodes: 
                explode.explode()
                #print("Explosion: " + str(tree))
                continue

            # Perform split
            split = tree.find_splits()
            if split:
                pair, location = split
                pair.split(location)
                #print("Split:     " + str(tree))

            if old_tree == str(tree):
                break
        
        #print("Latest:    " + str(tree) + "\n")

    # Find magnitude
    return tree.magnitude()

@print_result
def part_two(lines):

    def get_magnitude(left, right):
        tree = Pair(left, right)
        old_tree = ''

        # Loop until number reduced
        while True:

            old_tree = str(tree)

            # Perform explosion
            explodes = tree.find_explode()
            for explode in explodes: 
                explode.explode()
                continue

            # Perform split
            split = tree.find_splits()
            if split:
                pair, location = split
                pair.split(location)

            if old_tree == str(tree):
                break
                    
        # Find magnitude
        return tree.magnitude()

    # Read in all the entries
    entries = [eval(line) for line in lines]

    max_mag = 0
    for i, left in enumerate(entries):
        #print(str(i) + ' of ' + str(len(entries)) + ' Complete.')
        for right in entries[i+1:]:
            max_mag = max(max_mag, get_magnitude(left, right), get_magnitude(right, left))

    return max_mag

if __name__ == "__main__":
    main()