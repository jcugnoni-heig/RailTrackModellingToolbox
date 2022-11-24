#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.3.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'/home/cae/Documents/TrackSystemEvaluation/working_directory')

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

([unitCell], status) = smesh.CreateMeshesFromMED(r'/home/cae/Documents/TrackSystemEvaluation/working_directory/unitCellWithClamps.med')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
