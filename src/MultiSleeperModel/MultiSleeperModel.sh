#!/bin/bash

SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")/DevFiles/App

cd $SCRIPTPATH

python main.py