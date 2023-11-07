#!/bin/bash

export LD_LIBRARY_PATH=/opt/qt511/lib:$LD_LIBRARY_PATH

/opt/SalomeMeca/appli_V2019_univ/salome "$@"

