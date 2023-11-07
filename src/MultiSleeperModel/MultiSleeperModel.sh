#!/bin/bash

SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")/DevFiles/App
PYTHONPATH=python

cd $SCRIPTPATH

$PYTHONPATH main.py