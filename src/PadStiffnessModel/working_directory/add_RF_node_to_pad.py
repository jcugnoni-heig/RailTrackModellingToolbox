#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.3.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'/home/caelinux/Documents')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

print('Start of the script.')
geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Vertex_1 = geompy.MakeVertex(0, 7, 0)
Plane_1 = geompy.MakePlane(Vertex_1, OY, 2000)
Plane_2 = geompy.MakePlane(O, OY, 2000)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
print('Creation of a vertex on the face.')
geompy.addToStudy( Vertex_1, 'Vertex_1' )
print('Creation of a plane passsing by the top face.')
geompy.addToStudy( Plane_1, 'Plane_1' )
print('Creation of a plane passsing by the bottom face.')
geompy.addToStudy( Plane_2, 'Plane_2' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)


([ma], status) = smesh.CreateMeshesFromMED(r'/home/cae/Documents/Railpad2/PadStiffness_GUI/working_directory/importedPad.mesh.med')
print('importedPad mesh imported.')
#[ soft, hard, top, bot ] = ma.GetGroups()
ma.GetGroups()
print('Groups loaded.')
nb_of_node = ma.NbNodes()
print('number of node: ' + str(nb_of_node))
node = nb_of_node + 1
nb_of_elem = ma.NbElements()
print('number of elements: ' + str(nb_of_elem))
elem = nb_of_elem + 1
nodeID = ma.AddNode( 0, 10, 0 )
print('RF node added.')
RF = ma.CreateEmptyGroup( SMESH.NODE, 'RF' )
nbAdd = RF.Add( [ node ] )
print('RF node added to RF group.')
#[ soft, hard, top, bot, RF ] = ma.GetGroups()
ma.GetGroups()
elem0d = ma.Add0DElement( node )
print('0D element created.')
RF0D = ma.CreateEmptyGroup( SMESH.ELEM0D, 'RF0D' )
nbAdd = RF0D.Add( [ elem ] )
print('0D element added to group RF0D.')
aCriteria = []
aCriterion = smesh.GetCriterion(SMESH.NODE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,Plane_1)
aCriteria.append(aCriterion)
aFilter_3 = smesh.GetFilterFromCriteria(aCriteria)
topn = ma.MakeGroupByFilter( 'topn', aFilter_3 )
print('Creation of the topn node set of the node from the top face using the plan passing by this face.')
topn.SetColor( SALOMEDS.Color( 0.333333, 1, 0 ))
aCriteria = []
aCriterion = smesh.GetCriterion(SMESH.NODE,SMESH.FT_BelongToPlane,SMESH.FT_Undefined,Plane_2)
aCriteria.append(aCriterion)
aFilter_4 = smesh.GetFilterFromCriteria(aCriteria)
botn = ma.MakeGroupByFilter( 'botn', aFilter_4 )
print('Creation of the botn node set of the node from the bottom face using the plan passing by this face.')
botn.SetColor( SALOMEDS.Color( 0.333333, 1, 0 ))


## Set names of Mesh objects
smesh.SetName(ma.GetMesh(), 'ma')
smesh.SetName(RF, 'RF')
smesh.SetName(topn, 'topn')
smesh.SetName(botn, 'botn')
smesh.SetName(RF0D, 'RF0D')
#smesh.SetName(soft, 'soft')
#smesh.SetName(bot, 'bot')
#smesh.SetName(hard, 'hard')
#smesh.SetName(top, 'top')

try:
  ma.ExportMED(r'/home/cae/Documents/Railpad2/PadStiffness_GUI/working_directory/padWithRF.mesh.med',auto_groups=0,minor=40,overwrite=1,meshPart=None,autoDimension=1)
  print('New mesh exported as: padWithRF.mesh.med')
  pass
except:
  print('ExportMED() failed. Invalid file name?')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
print('Script finished.')
