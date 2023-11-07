#!/bin/bash

# set path to be abel to access mfront executable
export PATH=$PATH:/opt/aster/public/tfel-3.2.1/bin

SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")/GUI_files
PYTHONPATH=python

cd $SCRIPTPATH

$PYTHONPATH impulse_model_gui.py
