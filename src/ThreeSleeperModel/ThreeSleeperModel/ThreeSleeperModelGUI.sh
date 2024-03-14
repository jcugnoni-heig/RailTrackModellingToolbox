#!/bin/bash

SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
PYTHONPATH=__path__python

cd $SCRIPTPATH

$PYTHONPATH main.py
