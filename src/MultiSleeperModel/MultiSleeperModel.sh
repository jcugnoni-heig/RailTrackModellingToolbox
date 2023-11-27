#!/bin/bash

SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")/DevFiles/App
PYTHONPATH=__path__python

cd $SCRIPTPATH

$PYTHONPATH main.py