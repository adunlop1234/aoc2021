#!/bin/bash

if [ -n "$1" ]; then
    mkdir $1
    touch $1/$1.txt
    touch $1/$1_EX.txt
    cp template.py $1/$1.py
else
    echo "Usage is: ./create_new_folder.sh folder_name
     e.g. ./create_new_folder.sh 2"
fi