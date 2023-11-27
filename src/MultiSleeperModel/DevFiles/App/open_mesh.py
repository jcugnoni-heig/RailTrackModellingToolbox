#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.3.0 with dump python functionality
###
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()


###
### SMESH component
###

from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

meshFile = __mesh__
([unitCell], status) = smesh.CreateMeshesFromMED(meshFile)


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
