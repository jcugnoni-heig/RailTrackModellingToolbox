#!/bin/bash

# set path to be abel to access mfront executable
export PATH=$PATH:/opt/aster/public/tfel-3.2.1/bin

SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
SCRIPTPATH=$(dirname "$SCRIPT")/GUI_files

cd $SCRIPTPATH

python impulse_model_gui.py
