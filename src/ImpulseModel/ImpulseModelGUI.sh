#!/bin/bash

# set path to be abel to access mfront executable
export PATH=$PATH:/opt/aster/public/tfel-3.2.1/bin

SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
PYTHONPATH=python3

cd $SCRIPTPATH

$PYTHONPATH GUI_ImpulseModel.py
