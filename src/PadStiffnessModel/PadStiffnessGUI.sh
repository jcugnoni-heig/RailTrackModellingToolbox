#!/bin/bash

SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
PYTHONPATH=python

cd $SCRIPTPATH

$PYTHONPATH pad_stiffness_model_gui.py
