#!/bin/bash

SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
PYTHONPATH=python

cd $SCRIPTPATH

$PYTHONPATH main.py
