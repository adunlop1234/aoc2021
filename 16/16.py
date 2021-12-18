#!/usr/bin/env python3

'''
Template file for each new challenge.
'''

# Import helper functions
import functools
import os, sys
import numpy as np
from math import prod

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

# Function to perform the required evaluation
def perform_evaluation(values, typeID):

    typeID = int(typeID, 2)
    if typeID == 0:
        return sum(values)
    elif typeID == 1:
        return prod(values)
    elif typeID == 2:
        return min(values)
    elif typeID == 3:
        return max(values)
    elif typeID == 5:
        return int(values[0] > values[1])
    elif typeID == 6:
        return int(values[0] < values[1])
    elif typeID == 7:
        return int(values[0] == values[1])
    else:
        KeyError()

# Define function that returns the total number of versions
def packet_cruncher(packet):
    version_total = 0
    count = 0
    
    # Get packet version
    version = packet[count:3]
    count += 3
    version_total += int(version, 2)
    #print("Version: " + str(int(version, 2)))
    
    # Get packet type
    typeID = packet[count:count+3]
    count += 3
    #print("TypeID: " + str(int(typeID, 2)))
    
    # Get the literal value
    if typeID == '100':
        total = ''
        while True:
            value = packet[count:count+5]
            total += value[1:]
            count += 5
            if value[0] == '0':
                #print("Literal value: " + str(int(total, 2)))
                return packet[count:], version_total, int(total, 2)
    
    # Unpack the operator packet
    else:
        # Get type ID
        typeIDLength = packet[count:count+1]
        count += 1
        values = []

        # If the packet is based on number of bits
        if typeIDLength == '0':
            bit_length = int(packet[count:count+15], 2)
            count += 15
            entry = packet[count:count+bit_length]
            while True:
                entry, versions, value = packet_cruncher(entry)
                version_total += versions
                values.append(value)
                if '1' not in entry:
                    break
            
            return packet[count+bit_length:], version_total, perform_evaluation(values, typeID)

        elif typeIDLength == '1':
            sub_packet_total = int(packet[count:count+11], 2)
            count += 11
            entry = packet[count:]
            for _ in range(sub_packet_total):
                entry, versions, value = packet_cruncher(entry)
                version_total += versions
                values.append(value)

            return entry, version_total, perform_evaluation(values, typeID)

@print_result
def part_one(lines):
    
    # Convert packet to binary
    binary = ''
    for item in lines[0]:
        binary += format(int(item, 16), '04b')

    _, versions, _ = packet_cruncher(binary)
    return versions

@print_result
def part_two(lines):

    # Convert packet to binary
    binary = ''
    for item in lines[0]:
        binary += format(int(item, 16), '04b')

    _, _ , total = packet_cruncher(binary)
    return total

if __name__ == "__main__":
    main()