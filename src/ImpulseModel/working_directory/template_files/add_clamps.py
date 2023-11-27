#!/usr/bin/env python

import os
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()

workingDir = __workingDir__

###
### SMESH component
###

import  SMESH
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()

meshFile = os.path.join(workingDir, 'unitCell.med')
([unitCell], status) = smesh.CreateMeshesFromMED(meshFile)



#_________________________________________________________________
#|              ___                             ___              |
#|             |   |                           |   |             |         
#|    _________|   |___________________________|   |_________    |         
#|   |        a|   |a                         a|   |a        |   |         
#|   |      A  |   |  B     Z<----.         C  |   |  D      |   |         
#|   |________b|   |b_____________|___________b|   |b________|   |          
#|             |   |              |            |   |             |
#|             |   |              |            |   |             |
#|             |   |             \/            |   |             |
#|             |   |             X             |   |             |
#|             |   |                           |   |             |
#|             |   |                           |   |             |
#|    _________|   |___________________________|   |_________    |
#|   |        a|   |a                         a|   |a        |   |
#|   |      E  |   |  F                     G  |   |  H      |   |
#|   |________b|   |b_________________________b|   |b________|   |
#|             |   |                           |   |             |
#|             |   |                           |   |             |
#|             |   |                           |   |             |
#|             |   |                           |   |             |
#|             |   |                           |   |             |
#|    _________|   |___________________________|   |_________    |
#|   |        a|   |a                         a|   |a        |   |
#|   |      I  |   |  J                     K  |   |  L      |   |
#|   |________b|   |b_________________________b|   |b________|   |
#|             |   |                           |   |             |
#|             |   |                           |   |             |
#|             |___|                           |___|             |
#|_______________________________________________________________|
#
# A, B, C..., K and L show the clamps location.



#############
# edge Aa
#############
[sntrrea] = unitCell.GetGroupByName('sntrrea                                                                         ')
[rntsr1a] = unitCell.GetGroupByName('rntsr1a                                                                         ')


nodeaa1 = unitCell.CreateDimGroup( [ sntrrea ], SMESH.NODE, 'nodeaa1', SMESH.ALL_NODES, 0)
nodeaa2 = unitCell.CreateDimGroup( [ rntsr1a ], SMESH.NODE, 'nodeaa2', SMESH.ALL_NODES, 0)
idnodeaa1 = nodeaa1.GetIDs()
idnodeaa2 = nodeaa2.GetIDs()

edgeaa1 = unitCell.AddEdge([ idnodeaa1[0], idnodeaa2[0] ])
edgeaa1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgeaa' )
nbAdd = edgeaa1g.Add( [ edgeaa1 ] )

#############
# edge Ab
#############
[sntrreb] = unitCell.GetGroupByName('sntrreb                                                                         ')
[rntsr1b] = unitCell.GetGroupByName('rntsr1b                                                                         ')


nodeab1 = unitCell.CreateDimGroup( [ sntrreb ], SMESH.NODE, 'nodeab1', SMESH.ALL_NODES, 0)
nodeab2 = unitCell.CreateDimGroup( [ rntsr1b ], SMESH.NODE, 'nodeab2', SMESH.ALL_NODES, 0)
idnodeab1 = nodeab1.GetIDs()
idnodeab2 = nodeab2.GetIDs()

edgeab1 = unitCell.AddEdge([ idnodeab1[0], idnodeab2[0] ])
edgeab1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgeab' )
nbAdd = edgeab1g.Add( [ edgeab1 ] )

#############
# edge Ba
#############
[sntrria] = unitCell.GetGroupByName('sntrria                                                                         ')
[rntsl1a] = unitCell.GetGroupByName('rntsl1a                                                                         ')


nodeba1 = unitCell.CreateDimGroup( [ sntrria ], SMESH.NODE, 'nodeba1', SMESH.ALL_NODES, 0)
nodeba2 = unitCell.CreateDimGroup( [ rntsl1a ], SMESH.NODE, 'nodeba2', SMESH.ALL_NODES, 0)
idnodeba1 = nodeba1.GetIDs()
idnodeba2 = nodeba2.GetIDs()

edgeba1 = unitCell.AddEdge([ idnodeba1[0], idnodeba2[0] ])
edgeba1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgeba' )
nbAdd = edgeba1g.Add( [ edgeba1 ] )

#############
# edge Bb
#############
[sntrrib] = unitCell.GetGroupByName('sntrrib                                                                         ')
[rntsl1b] = unitCell.GetGroupByName('rntsl1b                                                                         ')


nodebb1 = unitCell.CreateDimGroup( [ sntrrib ], SMESH.NODE, 'nodebb1', SMESH.ALL_NODES, 0)
nodebb2 = unitCell.CreateDimGroup( [ rntsl1b ], SMESH.NODE, 'nodebb2', SMESH.ALL_NODES, 0)
idnodebb1 = nodebb1.GetIDs()
idnodebb2 = nodebb2.GetIDs()

edgebb1 = unitCell.AddEdge([ idnodebb1[0], idnodebb2[0] ])
edgebb1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgebb' )
nbAdd = edgebb1g.Add( [ edgebb1 ] )

#############
# edge Ca
#############
[sntrlia] = unitCell.GetGroupByName('sntrlia                                                                         ')
[rntsr1a0] = unitCell.GetGroupByName('rntsr1a0                                                                        ')


nodeca1 = unitCell.CreateDimGroup( [ sntrlia ], SMESH.NODE, 'nodeca1', SMESH.ALL_NODES, 0)
nodeca2 = unitCell.CreateDimGroup( [ rntsr1a0 ], SMESH.NODE, 'nodeca2', SMESH.ALL_NODES, 0)
idnodeca1 = nodeca1.GetIDs()
idnodeca2 = nodeca2.GetIDs()

edgeca1 = unitCell.AddEdge([ idnodeca1[0], idnodeca2[0] ])
edgeca1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgeca' )
nbAdd = edgeca1g.Add( [ edgeca1 ] )

#############
# edge Cb
#############
[sntrlib] = unitCell.GetGroupByName('sntrlib                                                                         ')
[rntsr1b0] = unitCell.GetGroupByName('rntsr1b0                                                                        ')


nodecb1 = unitCell.CreateDimGroup( [ sntrlib ], SMESH.NODE, 'nodecb1', SMESH.ALL_NODES, 0)
nodecb2 = unitCell.CreateDimGroup( [ rntsr1b0 ], SMESH.NODE, 'nodecb2', SMESH.ALL_NODES, 0)
idnodecb1 = nodecb1.GetIDs()
idnodecb2 = nodecb2.GetIDs()

edgecb1 = unitCell.AddEdge([ idnodecb1[0], idnodecb2[0] ])
edgecb1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgecb' )
nbAdd = edgecb1g.Add( [ edgecb1 ] )

#############
# edge Da
#############
[sntrlea] = unitCell.GetGroupByName('sntrlea                                                                         ')
[rntsl1a0] = unitCell.GetGroupByName('rntsl1a0                                                                        ')


nodeda1 = unitCell.CreateDimGroup( [ sntrlea ], SMESH.NODE, 'nodeda1', SMESH.ALL_NODES, 0)
nodeda2 = unitCell.CreateDimGroup( [ rntsl1a0 ], SMESH.NODE, 'nodeda2', SMESH.ALL_NODES, 0)
idnodeda1 = nodeda1.GetIDs()
idnodeda2 = nodeda2.GetIDs()

edgeda1 = unitCell.AddEdge([ idnodeda1[0], idnodeda2[0] ])
edgeda1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgeda' )
nbAdd = edgeda1g.Add( [ edgeda1 ] )

#############
# edge Db
#############
[sntrleb] = unitCell.GetGroupByName('sntrleb                                                                         ')
[rntsl1b0] = unitCell.GetGroupByName('rntsl1b0                                                                        ')


nodedb1 = unitCell.CreateDimGroup( [ sntrleb ], SMESH.NODE, 'nodedb1', SMESH.ALL_NODES, 0)
nodedb2 = unitCell.CreateDimGroup( [ rntsl1b0 ], SMESH.NODE, 'nodedb2', SMESH.ALL_NODES, 0)
idnodedb1 = nodedb1.GetIDs()
idnodedb2 = nodedb2.GetIDs()

edgedb1 = unitCell.AddEdge([ idnodedb1[0], idnodedb2[0] ])
edgedb1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgedb' )
nbAdd = edgedb1g.Add( [ edgedb1 ] )

#############
# edge Ea
#############
[sntrrea0] = unitCell.GetGroupByName('sntrrea0                                                                        ')
[rntsr2a] = unitCell.GetGroupByName('rntsr2a                                                                         ')


nodeea1 = unitCell.CreateDimGroup( [ sntrrea0 ], SMESH.NODE, 'nodeea1', SMESH.ALL_NODES, 0)
nodeea2 = unitCell.CreateDimGroup( [ rntsr2a ], SMESH.NODE, 'nodeea2', SMESH.ALL_NODES, 0)
idnodeea1 = nodeea1.GetIDs()
idnodeea2 = nodeea2.GetIDs()

edgeea1 = unitCell.AddEdge([ idnodeea1[0], idnodeea2[0] ])
edgeea1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgeea' )
nbAdd = edgeea1g.Add( [ edgeea1 ] )

#############
# edge Eb
#############
[sntrreb0] = unitCell.GetGroupByName('sntrreb0                                                                        ')
[rntsr2b] = unitCell.GetGroupByName('rntsr2b                                                                         ')


nodeeb1 = unitCell.CreateDimGroup( [ sntrreb0 ], SMESH.NODE, 'nodeeb1', SMESH.ALL_NODES, 0)
nodeeb2 = unitCell.CreateDimGroup( [ rntsr2b ], SMESH.NODE, 'nodeeb2', SMESH.ALL_NODES, 0)
idnodeeb1 = nodeeb1.GetIDs()
idnodeeb2 = nodeeb2.GetIDs()

edgeeb1 = unitCell.AddEdge([ idnodeeb1[0], idnodeeb2[0] ])
edgeeb1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgeeb' )
nbAdd = edgeeb1g.Add( [ edgeeb1 ] )

#############
# edge Fa
#############
[sntrria0] = unitCell.GetGroupByName('sntrria0                                                                        ')
[rntsl2a] = unitCell.GetGroupByName('rntsl2a                                                                         ')


nodefa1 = unitCell.CreateDimGroup( [ sntrria0 ], SMESH.NODE, 'nodefa1', SMESH.ALL_NODES, 0)
nodefa2 = unitCell.CreateDimGroup( [ rntsl2a ], SMESH.NODE, 'nodefa2', SMESH.ALL_NODES, 0)
idnodefa1 = nodefa1.GetIDs()
idnodefa2 = nodefa2.GetIDs()

edgefa1 = unitCell.AddEdge([ idnodefa1[0], idnodefa2[0] ])
edgefa1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgefa' )
nbAdd = edgefa1g.Add( [ edgefa1 ] )

#############
# edge Fb
#############
[sntrrib0] = unitCell.GetGroupByName('sntrrib0                                                                        ')
[rntsl2b] = unitCell.GetGroupByName('rntsl2b                                                                         ')


nodefb1 = unitCell.CreateDimGroup( [ sntrrib0 ], SMESH.NODE, 'nodefb1', SMESH.ALL_NODES, 0)
nodefb2 = unitCell.CreateDimGroup( [ rntsl2b ], SMESH.NODE, 'nodefb2', SMESH.ALL_NODES, 0)
idnodefb1 = nodefb1.GetIDs()
idnodefb2 = nodefb2.GetIDs()

edgefb1 = unitCell.AddEdge([ idnodefb1[0], idnodefb2[0] ])
edgefb1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgefb' )
nbAdd = edgefb1g.Add( [ edgefb1 ] )

#############
# edge Ga
#############
[sntrlia0] = unitCell.GetGroupByName('sntrlia0                                                                        ')
[rntsr2a0] = unitCell.GetGroupByName('rntsr2a0                                                                        ')


nodega1 = unitCell.CreateDimGroup( [ sntrlia0 ], SMESH.NODE, 'nodega1', SMESH.ALL_NODES, 0)
nodega2 = unitCell.CreateDimGroup( [ rntsr2a0 ], SMESH.NODE, 'nodega2', SMESH.ALL_NODES, 0)
idnodega1 = nodega1.GetIDs()
idnodega2 = nodega2.GetIDs()

edgega1 = unitCell.AddEdge([ idnodega1[0], idnodega2[0] ])
edgega1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgega' )
nbAdd = edgega1g.Add( [ edgega1 ] )

#############
# edge Gb
#############
[sntrlib0] = unitCell.GetGroupByName('sntrlib0                                                                        ')
[rntsr2b0] = unitCell.GetGroupByName('rntsr2b0                                                                        ')


nodegb1 = unitCell.CreateDimGroup( [ sntrlib0 ], SMESH.NODE, 'nodegb1', SMESH.ALL_NODES, 0)
nodegb2 = unitCell.CreateDimGroup( [ rntsr2b0 ], SMESH.NODE, 'nodegb2', SMESH.ALL_NODES, 0)
idnodegb1 = nodegb1.GetIDs()
idnodegb2 = nodegb2.GetIDs()

edgegb1 = unitCell.AddEdge([ idnodegb1[0], idnodegb2[0] ])
edgegb1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgegb' )
nbAdd = edgegb1g.Add( [ edgegb1 ] )

#############
# edge Ha
#############
[sntrlea0] = unitCell.GetGroupByName('sntrlea0                                                                        ')
[rntsl2a0] = unitCell.GetGroupByName('rntsl2a0                                                                        ')


nodeha1 = unitCell.CreateDimGroup( [ sntrlea0 ], SMESH.NODE, 'nodeha1', SMESH.ALL_NODES, 0)
nodeha2 = unitCell.CreateDimGroup( [ rntsl2a0 ], SMESH.NODE, 'nodeha2', SMESH.ALL_NODES, 0)
idnodeha1 = nodeha1.GetIDs()
idnodeha2 = nodeha2.GetIDs()

edgeha1 = unitCell.AddEdge([ idnodeha1[0], idnodeha2[0] ])
edgeha1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgeha' )
nbAdd = edgeha1g.Add( [ edgeha1 ] )

#############
# edge Hb
#############
[sntrleb0] = unitCell.GetGroupByName('sntrleb0                                                                        ')
[rntsl2b0] = unitCell.GetGroupByName('rntsl2b0                                                                        ')


nodehb1 = unitCell.CreateDimGroup( [ sntrleb0 ], SMESH.NODE, 'nodehb1', SMESH.ALL_NODES, 0)
nodehb2 = unitCell.CreateDimGroup( [ rntsl2b0 ], SMESH.NODE, 'nodehb2', SMESH.ALL_NODES, 0)
idnodehb1 = nodehb1.GetIDs()
idnodehb2 = nodehb2.GetIDs()

edgehb1 = unitCell.AddEdge([ idnodehb1[0], idnodehb2[0] ])
edgehb1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgehb' )
nbAdd = edgehb1g.Add( [ edgehb1 ] )

#############
# edge Ia
#############
[sntrrea1] = unitCell.GetGroupByName('sntrrea1                                                                        ')
[rntsr3a] = unitCell.GetGroupByName('rntsr3a                                                                         ')


nodeia1 = unitCell.CreateDimGroup( [ sntrrea1 ], SMESH.NODE, 'nodeia1', SMESH.ALL_NODES, 0)
nodeia2 = unitCell.CreateDimGroup( [ rntsr3a ], SMESH.NODE, 'nodeia2', SMESH.ALL_NODES, 0)
idnodeia1 = nodeia1.GetIDs()
idnodeia2 = nodeia2.GetIDs()

edgeia1 = unitCell.AddEdge([ idnodeia1[0], idnodeia2[0] ])
edgeia1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgeia' )
nbAdd = edgeia1g.Add( [ edgeia1 ] )

#############
# edge Ib
#############
[sntrreb1] = unitCell.GetGroupByName('sntrreb1                                                                        ')
[rntsr3b] = unitCell.GetGroupByName('rntsr3b                                                                         ')


nodeib1 = unitCell.CreateDimGroup( [ sntrreb1 ], SMESH.NODE, 'nodeib1', SMESH.ALL_NODES, 0)
nodeib2 = unitCell.CreateDimGroup( [ rntsr3b ], SMESH.NODE, 'nodeib2', SMESH.ALL_NODES, 0)
idnodeib1 = nodeib1.GetIDs()
idnodeib2 = nodeib2.GetIDs()

edgeib1 = unitCell.AddEdge([ idnodeib1[0], idnodeib2[0] ])
edgeib1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgeib' )
nbAdd = edgeib1g.Add( [ edgeib1 ] )

#############
# edge Ja
#############
[sntrria1] = unitCell.GetGroupByName('sntrria1                                                                        ')
[rntsl3a] = unitCell.GetGroupByName('rntsl3a                                                                         ')


nodeja1 = unitCell.CreateDimGroup( [ sntrria1 ], SMESH.NODE, 'nodeja1', SMESH.ALL_NODES, 0)
nodeja2 = unitCell.CreateDimGroup( [ rntsl3a ], SMESH.NODE, 'nodeja2', SMESH.ALL_NODES, 0)
idnodeja1 = nodeja1.GetIDs()
idnodeja2 = nodeja2.GetIDs()

edgeja1 = unitCell.AddEdge([ idnodeja1[0], idnodeja2[0] ])
edgeja1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgeja' )
nbAdd = edgeja1g.Add( [ edgeja1 ] )

#############
# edge Jb
#############
[sntrrib1] = unitCell.GetGroupByName('sntrrib1                                                                        ')
[rntsl3b] = unitCell.GetGroupByName('rntsl3b                                                                         ')


nodejb1 = unitCell.CreateDimGroup( [ sntrrib1 ], SMESH.NODE, 'nodejb1', SMESH.ALL_NODES, 0)
nodejb2 = unitCell.CreateDimGroup( [ rntsl3b ], SMESH.NODE, 'nodejb2', SMESH.ALL_NODES, 0)
idnodejb1 = nodejb1.GetIDs()
idnodejb2 = nodejb2.GetIDs()

edgejb1 = unitCell.AddEdge([ idnodejb1[0], idnodejb2[0] ])
edgejb1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgejb' )
nbAdd = edgejb1g.Add( [ edgejb1 ] )

#############
# edge Ka
#############
[sntrlia1] = unitCell.GetGroupByName('sntrlia1                                                                        ')
[rntsr3a0] = unitCell.GetGroupByName('rntsr3a0                                                                        ')


nodeka1 = unitCell.CreateDimGroup( [ sntrlia1 ], SMESH.NODE, 'nodeka1', SMESH.ALL_NODES, 0)
nodeka2 = unitCell.CreateDimGroup( [ rntsr3a0 ], SMESH.NODE, 'nodeka2', SMESH.ALL_NODES, 0)
idnodeka1 = nodeka1.GetIDs()
idnodeka2 = nodeka2.GetIDs()

edgeka1 = unitCell.AddEdge([ idnodeka1[0], idnodeka2[0] ])
edgeka1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgeka' )
nbAdd = edgeka1g.Add( [ edgeka1 ] )


#############
# edge Kb
#############
[sntrlib1] = unitCell.GetGroupByName('sntrlib1                                                                        ')
[rntsr3b0] = unitCell.GetGroupByName('rntsr3b0                                                                        ')


nodekb1 = unitCell.CreateDimGroup( [ sntrlib1 ], SMESH.NODE, 'nodekb1', SMESH.ALL_NODES, 0)
nodekb2 = unitCell.CreateDimGroup( [ rntsr3b0 ], SMESH.NODE, 'nodekb2', SMESH.ALL_NODES, 0)
idnodekb1 = nodekb1.GetIDs()
idnodekb2 = nodekb2.GetIDs()

edgekb1 = unitCell.AddEdge([ idnodekb1[0], idnodekb2[0] ])
edgekb1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgekb' )
nbAdd = edgekb1g.Add( [ edgekb1 ] )

#############
# edge La
#############
[sntrlea1] = unitCell.GetGroupByName('sntrlea1                                                                        ')
[rntsl3a0] = unitCell.GetGroupByName('rntsl3a0                                                                        ')


nodela1 = unitCell.CreateDimGroup( [ sntrlea1 ], SMESH.NODE, 'nodela1', SMESH.ALL_NODES, 0)
nodela2 = unitCell.CreateDimGroup( [ rntsl3a0 ], SMESH.NODE, 'nodela2', SMESH.ALL_NODES, 0)
idnodela1 = nodela1.GetIDs()
idnodela2 = nodela2.GetIDs()

edgela1 = unitCell.AddEdge([ idnodela1[0], idnodela2[0] ])
edgela1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgela' )
nbAdd = edgela1g.Add( [ edgela1 ] )

#############
# edge Lb
#############
[sntrleb1] = unitCell.GetGroupByName('sntrleb1                                                                        ')
[rntsl3b0] = unitCell.GetGroupByName('rntsl3b0                                                                        ')

nodelb1 = unitCell.CreateDimGroup( [ sntrleb1 ], SMESH.NODE, 'nodelb1', SMESH.ALL_NODES, 0)
nodelb2 = unitCell.CreateDimGroup( [ rntsl3b0 ], SMESH.NODE, 'nodelb2', SMESH.ALL_NODES, 0)
idnodelb1 = nodelb1.GetIDs()
idnodelb2 = nodelb2.GetIDs()

edgelb1 = unitCell.AddEdge([ idnodelb1[0], idnodelb2[0] ])
edgelb1g = unitCell.CreateEmptyGroup( SMESH.EDGE, 'edgelb' )
nbAdd = edgelb1g.Add( [ edgelb1 ] )

meshFileOut = os.path.join(workingDir, 'unitCellWithClamps.med')
try:
  unitCell.ExportMED(meshFileOut,auto_groups=0,minor=40,overwrite=1,meshPart=None,autoDimension=1)
  pass
except:
  print('ExportMED() failed. Invalid file name?')

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
