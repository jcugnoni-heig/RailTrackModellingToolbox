#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.3.0 with dump python functionality
###

import sys
import salome
import os

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()

cwd = os.getcwd()
sys.path.insert(0, cwd)

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

print('Running gen3sleepers in ' + cwd)

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

print('Reading temp mesh')

([mcomb3d], status) = smesh.CreateMeshesFromMED(cwd + r'/temp.mesh.med')
thickness = 8.5

#groupName = "ballast"
#groupName = groupName + ' '*(80-len(groupName))
#ballast = mcomb3d.GetGroupByName(groupName, SMESH.VOLUME)

#[ soft___4, hard___4, top____4, bot____4, soft___3, hard___3, top____3, bot____3, soft___2, hard___2, top____2, bot____2, soft___1, hard___1, top____1, bot____1, soft___0, hard___0, top____0, bot____0, soft, hard, top, bot, tr3, tr3td, tr3tg, tr2, tr2td, tr2tg, tr1, tr1td, tr1tg, raild, rd2, rd1, rd3, railg, rg3, rg2, rg1, ballast, tr3surf, tr3topd, trAcY, trAcZ, tr3topg, trAcX, tr3bot, tr2surf, tr2topd, tr2topg, tr2bot, tr1surf, tr1topd, tr1topg, tr1bot, Group_36, railsurf, raildAcZ, railAcY, force, Group_38, Group_37, raildAcI, Group_22, railgAcZ, Group_24, Group_25, railgAcI, balbot, balsurf, balAcY, baltop, baltop_1, balbot_1, frfout, frfrailc, frfrailm, noeuForc, frftravg, frftravm, botn, topn, botn___0, topn___0, botn___1, topn___1, botn___2, topn___2, botn___3, topn___3, botn___4, topn___4 ] = mcomb3d.GetGroups()


print('Processing groups')

grps = mcomb3d.GetGroups()
grpNames = mcomb3d.GetGroupNames()
i=0
for elem in grpNames:
    name = elem.split(' ')[0] # 
    if name == "ballast":
        break
    i += 1
ballast = grps[i]


print('Transform current mesh')
mcomb3d.TranslateObject( mcomb3d, [ 0, thickness, 0 ], 0 )
mcomb3d.TranslateObject( ballast, [ 0, -thickness, 0 ], 0 )


print('Read USO mesh')
([Mesh_6], status) = smesh.CreateMeshesFromMED(cwd + r'/Meshes/USPs.med')
#[ USP3, USP3topV, USP2, USP2topV, USP1, USP1topV, USP1botn, USP2botn, USP3botn ] = Mesh_6.GetGroups()


print('Merge meshes')
mesh = smesh.Concatenate( [ mcomb3d.GetMesh(), Mesh_6.GetMesh() ], 1, 0, 1e-05, False )
#[ soft___4_1, hard___4_1, top____4_1, bot____4_1, soft___3_1, hard___3_1, top____3_1, bot____3_1, soft___2_1, hard___2_1, top____2_1, bot____2_1, soft___1_1, hard___1_1, top____1_1, bot____1_1, soft___0_1, hard___0_1, top____0_1, bot____0_1, soft_1, hard_1, top_1, bot_1, tr3_1, tr3td_1, tr3tg_1, tr2_1, tr2td_1, tr2tg_1, tr1_1, tr1td_1, tr1tg_1, raild_1, rd2_1, rd1_1, rd3_1, railg_1, rg3_1, rg2_1, rg1_1, ballast_1, tr3surf_1, tr3topd_1, trAcY_1, trAcZ_1, tr3topg_1, trAcX_1, tr3bot_1, tr2surf_1, tr2topd_1, tr2topg_1, tr2bot_1, tr1surf_1, tr1topd_1, tr1topg_1, tr1bot_1, Group_36_1, railsurf_1, raildAcZ_1, railAcY_1, force_1, Group_38_1, Group_37_1, raildAcI_1, Group_22_1, railgAcZ_1, Group_24_1, Group_25_1, railgAcI_1, balbot_2, balsurf_1, balAcY_1, baltop_2, baltop_3, balbot_3, frfout_1, frfrailc_1, frfrailm_1, noeuForc_1, frftravg_1, frftravm_1, botn_1, topn_1, botn___0_1, topn___0_1, botn___1_1, topn___1_1, botn___2_1, topn___2_1, botn___3_1, topn___3_1, botn___4_1, topn___4_1, USP3_1, USP3topV_1, USP2_1, USP2topV_1, USP1_1, USP1topV_1, USP1botn_1, USP2botn_1, USP3botn_1 ] = mesh.GetGroups()


try:

  print('Exporting Mesh')
  mesh.ExportMED(cwd + r'/temp.mesh.med',auto_groups=0,minor=40,overwrite=1,meshPart=None,autoDimension=1)
  pass
except:
  print('ExportMED() failed. Invalid file name?')


print('Finishing gen3sleepers')

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
