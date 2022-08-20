#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.3.0 with dump python functionality
###

import sys
import salome
import os
cwd = os.getcwd()

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, cwd)

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

# PARAMETERS
thickness = 8.5 # don't forget to adapt gen3sleepersUSP.py
nElemThk = 2
globElemSize = thickness/nElemThk*6
nUSPs = 3 # not used yet

geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Vertex_1 = geompy.MakeVertex(-150, 0, -1300)
Vertex_2 = geompy.MakeVertex(-150, 0, -1060)
Vertex_3 = geompy.MakeVertex(-110, 0, -200)
Mirror_1_1 = geompy.MakeMirrorByAxis(Vertex_1, OX)
Mirror_1_2 = geompy.MakeMirrorByAxis(Vertex_2, OX)
Mirror_1_3 = geompy.MakeMirrorByAxis(Vertex_3, OX)
Mirror_1_4 = geompy.MakeMirrorByAxis(Vertex_1, OZ)
Mirror_1_5 = geompy.MakeMirrorByAxis(Vertex_2, OZ)
Mirror_1_6 = geompy.MakeMirrorByAxis(Vertex_3, OZ)
Mirror_1_7 = geompy.MakeMirrorByAxis(Mirror_1_1, OZ)
Mirror_1_8 = geompy.MakeMirrorByAxis(Mirror_1_2, OZ)
Mirror_1_9 = geompy.MakeMirrorByAxis(Mirror_1_3, OZ)
Curve_1 = geompy.MakePolyline([Vertex_1, Vertex_2, Vertex_3, Mirror_1_3, Mirror_1_2, Mirror_1_1, Mirror_1_7, Mirror_1_8, Mirror_1_9, Mirror_1_6, Mirror_1_5, Mirror_1_4], True)
Face_1 = geompy.MakeFaceWires([Curve_1], 1)

Extrusion_1 = geompy.MakePrismVecH(Face_1, OY, thickness)
USPedge = geompy.CreateGroup(Extrusion_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(USPedge, [36])
USPtop = geompy.CreateGroup(Extrusion_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(USPtop, [89])
USPbot = geompy.CreateGroup(Extrusion_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(USPbot, [87])
Translation_1 = geompy.MakeTranslation(Extrusion_1, 0, thickness-thickness/nElemThk, 0)

geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Vertex_1, 'Vertex_1' )
geompy.addToStudy( Vertex_2, 'Vertex_2' )
geompy.addToStudy( Vertex_3, 'Vertex_3' )
geompy.addToStudy( Mirror_1_2, 'Mirror_1_2' )
geompy.addToStudy( Mirror_1_1, 'Mirror_1_1' )
geompy.addToStudy( Mirror_1_3, 'Mirror_1_3' )
geompy.addToStudy( Mirror_1_4, 'Mirror_1_4' )
geompy.addToStudy( Mirror_1_5, 'Mirror_1_5' )
geompy.addToStudy( Mirror_1_6, 'Mirror_1_6' )
geompy.addToStudy( Mirror_1_7, 'Mirror_1_7' )
geompy.addToStudy( Mirror_1_8, 'Mirror_1_8' )
geompy.addToStudy( Mirror_1_9, 'Mirror_1_9' )
geompy.addToStudy( Curve_1, 'Curve_1' )
geompy.addToStudy( Face_1, 'Face_1' )
geompy.addToStudy( Extrusion_1, 'Extrusion_1' )
geompy.addToStudyInFather( Extrusion_1, USPedge, 'USPedge' )
geompy.addToStudyInFather( Extrusion_1, USPtop, 'USPtop' )
geompy.addToStudyInFather( Extrusion_1, USPbot, 'USPbot' )
geompy.addToStudy( Translation_1, 'Translation_1' )





###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

# Create mesh
aFilterManager = smesh.CreateFilterManager()
Mesh_1 = smesh.Mesh(Extrusion_1)
Regular_1D = Mesh_1.Segment()
Number_of_Segments_1 = Regular_1D.NumberOfSegments(nElemThk)
Quadrangle_2D = Mesh_1.Quadrangle(algo=smeshBuilder.QUADRANGLE)
Hexa_3D = Mesh_1.Hexahedron(algo=smeshBuilder.Hexa)
status = Mesh_1.RemoveHypothesis(Number_of_Segments_1)
Local_Length_1 = Regular_1D.LocalLength(globElemSize,None,1e-07)
Regular_1D_1 = Mesh_1.Segment(geom=USPedge)
status = Mesh_1.AddHypothesis(Number_of_Segments_1,USPedge)
Propagation_of_1D_Hyp = Regular_1D_1.Propagation()
isDone = Mesh_1.Compute()
#Mesh_1.ConvertToQuadratic(0)
#Mesh_1.ConvertFromQuadratic()

# Group bottom nodes
USP1botn = Mesh_1.GroupOnGeom(USPbot,'USPbot',SMESH.NODE)
USP1botn.SetName( 'USP1botn' )

# Group volume elements on top
aCriteria = []
aCriterion = smesh.GetCriterion(SMESH.VOLUME,SMESH.FT_BelongToGeom,SMESH.FT_Undefined,Translation_1)
aCriteria.append(aCriterion)
aFilter_3 = smesh.GetFilterFromCriteria(aCriteria)
aFilter_3.SetMesh(Mesh_1.GetMesh())
USP1topV = Mesh_1.GroupOnFilter( SMESH.VOLUME, 'USP1topV', aFilter_3 )

# Group all volume elements
USP1 = Mesh_1.CreateEmptyGroup( SMESH.VOLUME, 'USP1' )
nbAdd = USP1.AddFrom( Mesh_1.GetMesh() )

# Duplicate mesh 2x (later do a for loop for n times)
Mesh_2 = Mesh_1.TranslateObjectMakeMesh( Mesh_1, [ 600, 0, 0 ], 1, 'Mesh_2' )
[ USP2botn, USP2topV, USP2 ] = Mesh_2.GetGroups()
USP2botn.SetName( 'USP2botn' )
USP2topV.SetName( 'USP2topV' )
USP2.SetName( 'USP2' )
Regular_1D_2 = Regular_1D_1.GetSubMesh()

Mesh_3 = Mesh_1.TranslateObjectMakeMesh( Mesh_1, [ 1200, 0, 0 ], 1, 'Mesh_3' )
[ USP3botn, USP3topV, USP3 ] = Mesh_3.GetGroups()
USP3botn.SetName( 'USP3botn' )
USP3topV.SetName( 'USP3topV' )
USP3.SetName( 'USP3' )
Regular_1D_3 = Regular_1D_1.GetSubMesh()

USPs = smesh.Concatenate( [ Mesh_1.GetMesh(), Mesh_2.GetMesh(), Mesh_3.GetMesh() ], 1, 1, 1e-05, False )


## Set names of Mesh objects
smesh.SetName(USP1topV, 'USP1topV')
smesh.SetName(Local_Length_1, 'Local Length_1')
smesh.SetName(Propagation_of_1D_Hyp, 'Propagation of 1D Hyp. on Opposite Edges_1')
smesh.SetName(Number_of_Segments_1, 'Number of Segments_1')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(Hexa_3D.GetAlgorithm(), 'Hexa_3D')
smesh.SetName(Quadrangle_2D.GetAlgorithm(), 'Quadrangle_2D')
smesh.SetName(USP1botn, 'USP1botn')



try:
  USPs.ExportMED(cwd + r'/Meshes/USPs.med',auto_groups=0,minor=40,overwrite=1,meshPart=None,autoDimension=1)
  pass
except:
  print('ExportMED() failed. Invalid file name?')








if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
