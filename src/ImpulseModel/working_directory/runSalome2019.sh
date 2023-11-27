#!/bin/bash

export LD_LIBRARY_PATH=__path__ldLibrary:$LD_LIBRARY_PATH

__path__salome "$@"

