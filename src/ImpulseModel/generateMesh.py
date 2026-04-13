import sys
import salome
import math
import json

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()


import  SMESH, SALOMEDS, GEOM
from salome.geom import geomBuilder
from salome.smesh import smeshBuilder

parameters_file = sys.argv[1]
# Loading Geometry parameters
with open(parameters_file, 'r') as f:
  txt = f.read()
f.close()
properties = json.loads(txt)

# variable
takeUsp = properties["TakeUSP"]
nbr_sleepers_3D = properties["Geometry"]["Sleepers"]["nbr_sleepers_3D"]
nbr_sleepers = properties["Geometry"]["Sleepers"]["nbr_sleepers"]
slpSpacing = properties["Geometry"]["Sleepers"]["slpSpacing"]
L_Sleeper_z = properties["Geometry"]["Sleepers"]["L_Sleeper_z"]
tiltAngle_rad = properties["Geometry"]["tiltAngle_rad"]
tiltAngle_deg = tiltAngle_rad*180/math.pi
padThickness = properties["Geometry"]["Pads"]["heigth"]
halfDistBtwnRails = properties["Geometry"]["halfDistBtwnRails"] 
SepPart=495
USPthickness = properties["Geometry"]["USPthickness"] 
padYOffset = properties["Geometry"]["padYOffset"] 
railXOffset = slpSpacing 
railYOffset = padYOffset + padThickness*math.cos(tiltAngle_rad)
L_beamSleeper = properties["Geometry"]["Sleepers"]["L_beamSleeper"]

if(nbr_sleepers_3D%2 == 0):
   SymXOffset = -slpSpacing/2
else:
   SymXOffset = 0

if not takeUsp:
   USPthickness = 0

# ----- 3D Ballast Construction -----

Ballast_L = (nbr_sleepers_3D)*slpSpacing
Ballast_l = properties["Geometry"]["Ballast"]["Ballast_l"] 
Ballast_h =  properties["Geometry"]["Ballast"]["Ballast_h"] 
Element_per_edge_h = properties["Geometry"]["Ballast"]["Element_per_edge_h"] 
Element_size_L = properties["Geometry"]["Ballast"]["Element_size_L"] 

geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )

x0 = geompy.MakeVertex(Ballast_L/2, Ballast_h-Ballast_h/Element_per_edge_h, Ballast_l/2)

ballast3D_0 = geompy.MakeBoxDXDYDZ(Ballast_L, Ballast_h, Ballast_l)

Cut_plan = geompy.MakePlane(x0, OY, max(Ballast_l,Ballast_L) +20)
ballast3D = geompy.MakePartition([ballast3D_0], [Cut_plan], [], [], geompy.ShapeType["SOLID"], 0, [], 0)

ballast_h = geompy.CreateGroup(ballast3D, geompy.ShapeType["EDGE"])
bst_up = geompy.CreateGroup(ballast3D, geompy.ShapeType["FACE"])
bst_dwn = geompy.CreateGroup(ballast3D, geompy.ShapeType["FACE"])
ballast_sym = geompy.CreateGroup(ballast3D, geompy.ShapeType["FACE"])
edg_up = geompy.CreateGroup(ballast3D, geompy.ShapeType["EDGE"])
edg_dwn = geompy.CreateGroup(ballast3D, geompy.ShapeType["EDGE"])
v_up = geompy.CreateGroup(ballast3D, geompy.ShapeType["SOLID"])
v_dwn = geompy.CreateGroup(ballast3D, geompy.ShapeType["SOLID"])
ballast = geompy.CreateGroup(ballast3D, geompy.ShapeType["SOLID"])
geompy.UnionIDs(ballast, [2, 36])
geompy.UnionIDs(v_dwn, [2])
geompy.UnionIDs(v_up, [36])
geompy.UnionIDs(edg_dwn, [28, 11, 6, 18])
geompy.UnionIDs(edg_up, [44, 40, 57, 49])
geompy.UnionIDs(bst_up, [50])
geompy.UnionIDs(bst_dwn, [31])
geompy.UnionIDs(ballast_sym, [55, 26])
geompy.UnionIDs(ballast_h, [44, 11, 28, 6, 40, 57, 18, 49])
geompy.addToStudyInFather( ballast3D, ballast_h, 'ballast_h' )
geompy.TranslateDXDYDZ(ballast3D, -Ballast_L/2, -(Ballast_h+ USPthickness), 0)
geompy.addToStudy( ballast3D, 'ballast3D' )
geompy.addToStudyInFather( ballast3D, ballast_h, 'ballast_h' )
geompy.addToStudyInFather( ballast3D, edg_up, 'edg_up' )
geompy.addToStudyInFather( ballast3D, edg_dwn, 'edg_dwn' )
geompy.addToStudyInFather( ballast3D, bst_up, 'bst_up' )
geompy.addToStudyInFather( ballast3D, bst_dwn, 'bst_dwn' )
geompy.addToStudyInFather( ballast3D, v_up, 'v_up' )
geompy.addToStudyInFather( ballast3D, v_dwn, 'v_dwn' )
geompy.addToStudyInFather( ballast3D, ballast, 'ballast' )


# ----- Creat Ballast Mesh -----
smesh = smeshBuilder.New()

Ballast_mesh = smesh.Mesh(ballast3D)
Regular_1D = Ballast_mesh.Segment()
Local_Length_1 = Regular_1D.LocalLength(Element_size_L,None,1e-07)
Quadrangle_2D = Ballast_mesh.Quadrangle(algo=smeshBuilder.QUADRANGLE)
Hexa_3D = Ballast_mesh.Hexahedron(algo=smeshBuilder.Hexa)
Regular_1D_1 = Ballast_mesh.Segment(geom=edg_up)
Number_of_Segments_2 = Regular_1D_1.NumberOfSegments(1)
Regular_1D_2 = Ballast_mesh.Segment(geom=edg_dwn)
Number_of_Segments_2 = Regular_1D_2.NumberOfSegments(Element_per_edge_h-1)
isDone = Ballast_mesh.Compute()
Sub_mesh_1 = Regular_1D_1.GetSubMesh()
Sub_mesh_2 = Regular_1D_2.GetSubMesh()

bst_up = Ballast_mesh.GroupOnGeom(bst_up,'bst_up',SMESH.NODE)
bst_dwn = Ballast_mesh.GroupOnGeom(bst_dwn,'bst_dwn',SMESH.NODE)
ballast_sym = Ballast_mesh.GroupOnGeom(ballast_sym,'ballast_sym',SMESH.NODE)
v_up = Ballast_mesh.GroupOnGeom(v_up,'v_up',SMESH.VOLUME)
v_dwn = Ballast_mesh.GroupOnGeom(v_dwn,'v_dwn',SMESH.VOLUME)
ballast = Ballast_mesh.GroupOnGeom(ballast,'ballast',SMESH.VOLUME)

smesh.SetName(Sub_mesh_1, 'Sub-mesh_1')
smesh.SetName(Local_Length_1, 'Number of Segments_1')
smesh.SetName(Number_of_Segments_2, 'Number of Segments_2')
smesh.SetName(Quadrangle_2D.GetAlgorithm(), 'Quadrangle_2D')
smesh.SetName(Hexa_3D.GetAlgorithm(), 'Hexa_3D')
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(Ballast_mesh.GetMesh(), 'Ballast_mesh')

# ----- Creat Rail Mesh -----
# Rail 3D + Grp

Element_size = properties["Geometry"]["Rail"]["Element_size"] 
Rail_portion = properties["Geometry"]["Rail"]["Rail_portion"] 
Length_element_add = round(Rail_portion/Element_size/2)*(nbr_sleepers_3D-1)
Length_element_addp = round(Rail_portion/Element_size/2)*(nbr_sleepers_3D-1 + (nbr_sleepers_3D+1)%2)
Length_element_addn = round(Rail_portion/Element_size/2)*(nbr_sleepers_3D-1 - (nbr_sleepers_3D+1)%2)
([Rail], status) = smesh.CreateMeshesFromMED(properties["Geometry"]["Rail"]["Rail_mesh"] )
Rail.TranslateObject( Rail, [ SymXOffset, 0, 0 ], 0 )

groups_rail = Rail.GetGroups()
groups_dict_rail = {g.GetName(): g for g in groups_rail}

rntsra = groups_dict_rail.get("rntsra")
Rail_xp = groups_dict_rail.get("Rail_xp")
Rail_xn = groups_dict_rail.get("Rail_xn")

IDnode = rntsra.GetIDs()
x, y, z = Rail.GetNodeXYZ(IDnode[0])


Railp_newGroup = Rail.ExtrusionSweepObjects( [], [], [ Rail_xp ], [ Element_size, 0, 0 ], Length_element_addp, 1, [  ], 0, [  ], [  ], 0 ) # 60E2
Railn_newGroup = Rail.ExtrusionSweepObjects( [], [], [ Rail_xn ], [ -Element_size, 0, 0 ], Length_element_addn, 1, [  ], 0, [  ], [  ], 0 )
Rail_newGroup = Railn_newGroup + Railp_newGroup
Rail.RotateObject( Rail, SMESH.AxisStruct( 0, 0, 0, 1, 0, 0 ), tiltAngle_rad, 0 )
Rail.TranslateObject( Rail, [ 0, railYOffset, halfDistBtwnRails ], 0 )

# Volume for grp

geomObj_1 = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)
sk = geompy.Sketcher2D()
sk.addPoint(75.000000, 0.000000)
sk.addSegmentAbsolute(75.000000, 6.000000)
sk.addSegmentAbsolute(50.000000, 7.300000)
sk.addSegmentAbsolute(12.400000, 13.500000)
sk.addSegmentAbsolute(-12.400000, 13.500000)
sk.addSegmentAbsolute(-50.000000, 7.300000)
sk.addSegmentAbsolute(-75.000000, 6.000000)
sk.addSegmentAbsolute(-75.000000, 0.000000)
sk.close()
Sketch_1 = sk.wire(geomObj_1)
rail_face = geompy.MakeFaceWires([Sketch_1], 1)
geompy.Rotate(rail_face, OY, 90*math.pi/180.0)
geompy.Rotate(rail_face, OX, tiltAngle_rad)
rail_geom = geompy.MakePrismVecH2Ways(rail_face, OX, Rail_portion + Element_size*Length_element_add)
geompy.TranslateDXDYDZ(rail_geom, 0, railYOffset, halfDistBtwnRails)
geompy.addToStudy( Sketch_1, 'Sketch_1' )
geompy.addToStudy( rail_face, 'rail_face' )
geompy.addToStudy( rail_geom, 'rail_geom' )

aCriteria = []
aCriterion = smesh.GetCriterion(SMESH.VOLUME,SMESH.FT_BelongToGeom,SMESH.FT_Undefined,rail_geom,SMESH.FT_Undefined,SMESH.FT_Undefined,0.001)
aCriteria.append(aCriterion)
aFilter00000195BB24D640 = smesh.GetFilterFromCriteria(aCriteria)
retp = Rail.MakeGroupByFilter( 'retp', aFilter00000195BB24D640 )

Newgroups_dict_rail = {g.GetName(): g for g in Rail_newGroup}
Rail_xp_extruded = Newgroups_dict_rail.get("Rail_xp_extruded")
Rail_xn_extruded = Newgroups_dict_rail.get("Rail_xn_extruded")
railBk_top = Newgroups_dict_rail.get("railBk_top")
railFt_top = Newgroups_dict_rail.get("railFt_top")

Rail_xp_extruded.SetName( 'raile' )
Rail_xn_extruded.SetName( 'raile' )
railBk_top.SetName('rBk_top' )
railFt_top.SetName('rft_top' )

# ------ Creat Clamp node ------

rntsrb = groups_dict_rail.get("rntsrb")
rntsla = groups_dict_rail.get("rntsla")
rntslb = groups_dict_rail.get("rntslb")

rntsraIDs = rntsra.GetIDs()
rntsrbIDs = rntsrb.GetIDs()
rntslaIDs = rntsla.GetIDs()
rntslbIDs = rntslb.GetIDs()


x_rntsra , y_rntsra, z_rntsra = Rail.GetNodeXYZ(rntsraIDs[0])
x_rntsrb , y_rntsrb, z_rntsrb = Rail.GetNodeXYZ(rntsrbIDs[0])
x_rntsla , y_rntsla, z_rntsla = Rail.GetNodeXYZ(rntslaIDs[0])
x_rntslb , y_rntslb, z_rntslb = Rail.GetNodeXYZ(rntslbIDs[0])


nID_rntsra, nID_rntsrb, nID_rntsla, nID_rntslb  = [], [], [], []
Dx = 0


for p in range(1, nbr_sleepers_3D):
   Dx = (-1)**(p+1) * (abs(Dx) + slpSpacing * (p % 2))
   nID_rntsra.append(Rail.FindNodeClosestTo(Dx + x_rntsra, y_rntsra, z_rntsra))
   nID_rntsrb.append(Rail.FindNodeClosestTo(Dx + x_rntsrb, y_rntsrb, z_rntsrb))
   nID_rntsla.append(Rail.FindNodeClosestTo(Dx + x_rntsla, y_rntsla, z_rntsla))
   nID_rntslb.append(Rail.FindNodeClosestTo(Dx + x_rntslb, y_rntslb, z_rntslb))

rntsrb.Add(nID_rntsrb)
rntsra.Add(nID_rntsra)
rntslb.Add(nID_rntslb)
rntsla.Add(nID_rntsla)


# ------ Creat Beam Sleeper -----

Vs_1 = geompy.MakeVertex(SymXOffset, padYOffset/2, 0)
Vs_2 = geompy.MakeVertex(SymXOffset, padYOffset/2, L_Sleeper_z)
Full_SleeperBeam = geompy.MakeLineTwoPnt(Vs_1, Vs_2)
Vs_3 = geompy.MakeVertexOnCurveByLength(Full_SleeperBeam, halfDistBtwnRails, Vs_1)
Vs_4 = geompy.MakeVertexOnCurveByLength(Full_SleeperBeam, SepPart, Vs_1)
BeamSlp_1 = geompy.MakePartition([Full_SleeperBeam], [Vs_3,Vs_4], [], [], geompy.ShapeType["EDGE"], 0, [], 0)
BeamSlp_2 = geompy.CreateGroup(BeamSlp_1, geompy.ShapeType["EDGE"])
geompy.UnionIDs(BeamSlp_2, [2, 5, 7])
Sec1 = geompy.CreateGroup(BeamSlp_1, geompy.ShapeType["EDGE"])
Sec2 = geompy.CreateGroup(BeamSlp_1, geompy.ShapeType["EDGE"])
pdsR = geompy.CreateGroup(BeamSlp_1, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(pdsR, [6])
BC_sym = geompy.CreateGroup(BeamSlp_1, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(BC_sym, [3])
geompy.UnionIDs(Sec1, [2])
geompy.UnionIDs(Sec2, [5, 7])
geompy.addToStudy( Vs_1, 'Vertex_1' )
geompy.addToStudy( Vs_2, 'Vertex_2' )
geompy.addToStudy( Full_SleeperBeam, 'BeamSlp' )
geompy.addToStudy( Vs_3, 'Vertex_3' )
geompy.addToStudy( BeamSlp_1, 'BeamSlp' )
geompy.addToStudyInFather( BeamSlp_1, BeamSlp_2, 'BeamSlp' )
geompy.addToStudyInFather( BeamSlp_1, Sec1, 'Sec1' )
geompy.addToStudyInFather( BeamSlp_1, Sec2, 'Sec2' )
geompy.addToStudyInFather( BeamSlp_1, pdsR, 'pdsR' )
geompy.addToStudyInFather( BeamSlp_1, BC_sym, 'BC_sym' )

# ----- Creat Beam Sleeper Mesh ----- 

BeamSlp_Mesh = smesh.Mesh(BeamSlp_1)
Regular_1D = BeamSlp_Mesh.Segment()
Local_Length_1 = Regular_1D.LocalLength(L_beamSleeper,None,1e-07)
Regular_1D_1 = BeamSlp_Mesh.Segment(geom=BeamSlp_2)
status = BeamSlp_Mesh.AddHypothesis(Local_Length_1,BeamSlp_2)
isDone = BeamSlp_Mesh.Compute()
BeamSlp_EdgeGrp = BeamSlp_Mesh.GroupOnGeom(BeamSlp_2,'BeamSlp',SMESH.EDGE)
Sec1 = BeamSlp_Mesh.GroupOnGeom(Sec1,'Sec1',SMESH.EDGE)
Sec2 = BeamSlp_Mesh.GroupOnGeom(Sec2,'Sec2',SMESH.EDGE)
pdsR = BeamSlp_Mesh.GroupOnGeom(pdsR,'pdsR',SMESH.NODE)
BC_sym = BeamSlp_Mesh.GroupOnGeom(BC_sym,'BC_sym',SMESH.NODE)
BmSlpN = BeamSlp_Mesh.GroupOnGeom(BeamSlp_2,'BmSlpN',SMESH.NODE) # BeamSlpNode
Sub_mesh_1 = Regular_1D_1.GetSubMesh()

## Set names of Mesh objects
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(Local_Length_1, 'Number of Segments_1')
smesh.SetName(BeamSlp_Mesh.GetMesh(), 'BeamSlp')


# ----- Creat Sleeper Mesh -----

([Sleeper3D], status) = smesh.CreateMeshesFromMED(properties["Geometry"]["Sleepers"]["Sleeper3D_mesh"])
([Pad], status) = smesh.CreateMeshesFromMED(properties["Geometry"]["Pads"]["Pad_mesh"])
([USP], status) = smesh.CreateMeshesFromMED(properties["Geometry"]["USP_mesh"])

Pad.RotateObject( Pad, SMESH.AxisStruct( 0, 0, 0, 1, 0, 0 ), tiltAngle_rad, 0 )
Pad.TranslateObject( Pad, [ 0, padYOffset, halfDistBtwnRails ], 0 )


USP.TranslateObject( USP, [ 0, -USPthickness, 0 ], 0 )

groups_sleeper = Sleeper3D.GetGroups()
groups_dict_sleeper = {g.GetName(): g for g in groups_sleeper}

sntrea = groups_dict_sleeper.get("sntrea")
sntreb = groups_dict_sleeper.get("sntreb")
sntria = groups_dict_sleeper.get("sntria")
sntrib = groups_dict_sleeper.get("sntrib")


sntreaIDs = sntrea.GetIDs()
sntrebIDs = sntreb.GetIDs()
sntriaIDS = sntria.GetIDs()
sntribIDs = sntrib.GetIDs()
rntsraIDs = rntsra.GetIDs()
rntsrbIDs = rntsrb.GetIDs()
rntslaIDS = rntsla.GetIDs()
rntslbIDs = sntrib.GetIDs()


[ hard, soft, pnts, pntr_3DR ] = Pad.GetGroups()
pntr_3DR.SetName( 'pntr_3DR' )

element_for_MacroEL3D = [ Sleeper3D.GetMesh(), Pad.GetMesh()]
if (takeUsp):
   element_for_MacroEL3D.append(USP.GetMesh())

MacroEL3D = smesh.Concatenate( element_for_MacroEL3D, 1, 0, 1e-05, False )
MacroEL3D.TranslateObject( MacroEL3D, [ SymXOffset, 0 , 0 ], 0 )
smesh.SetName(MacroEL3D.GetMesh(), 'sleeper_1')


SleperObj = [MacroEL3D]
slp_nbr = 2
nLeft=0
nRight=0

nbrRailxp = nbr_sleepers_3D/2
nbrRailxn = nbr_sleepers_3D/2



for k in range(1, (nbr_sleepers)//2 +1):
    for p in range (2):

      if(slp_nbr > nbr_sleepers):
         break

      if(slp_nbr<=nbr_sleepers_3D):
         SleperObj.append(MacroEL3D.TranslateObjectMakeMesh( MacroEL3D, [((-1)**p)*k*slpSpacing, 0, 0 ], 1, 'sleeper_' + str(slp_nbr) ))

      else:
         if(p%2 == 0):
            nLeft +=1
            nameToadd = 'p' + str(nLeft)
            nbrRailxp+= 1
         else:
            nRight +=1
            nameToadd = 'n' + str(nRight)
            nbrRailxn+= 1

         pdsR.SetName('pdsR_' + nameToadd)
         SleperObj.append(BeamSlp_Mesh.TranslateObjectMakeMesh( BeamSlp_Mesh, [ ((-1)**p)*k*slpSpacing, 0, 0 ], 1, 'sleeper_' + str(slp_nbr) ))
      
      print(f"Sleeper No. {slp_nbr} was initialized with k={k} and p={p}")
      slp_nbr += 1


SleeperGroup = smesh.Concatenate( SleperObj, 1, 0, 1e-05, False )
smesh.SetName(SleeperGroup.GetMesh(), 'SleeperGroup')

sntrea_L , sntreb_L , sntria_L, sntrib_L = [], [], [], []
rntsra_L , rntsrb_L , rntsla_L, rntslb_L = [], [], [], []
nw_sntrea = SleeperGroup.GetGroupByName("sntrea")
nw_sntreb = SleeperGroup.GetGroupByName("sntreb")
nw_sntria = SleeperGroup.GetGroupByName("sntria")
nw_sntrib = SleeperGroup.GetGroupByName("sntrib")
nw_rntsra = Rail.GetGroupByName("rntsra")
sntr = [nw_sntrea[-1].GetIDs(),nw_sntreb[-1].GetIDs(), nw_sntria[-1].GetIDs(), nw_sntrib[-1].GetIDs()]
rnts = [nw_rntsra[-1].GetIDs(),rntsrb.GetIDs(), rntsla.GetIDs(), rntslb.GetIDs()]


for k in range (len(sntr[0])):
   Lx, Ly , Lz = [] ,[] ,[]
   for p in range (4):
    x, y , z = SleeperGroup.GetNodeXYZ(sntr[p][k])
    Lx.append(x)
    Ly.append(y)
    Lz.append(z)

   sntrea_L.append({'no' : sntr[0][k], 'x' : Lx[0], 'y' : Ly[0] , 'z' : Lz[0]})
   sntreb_L.append({'no' : sntr[1][k], 'x' : Lx[1], 'y' : Ly[1] , 'z' : Lz[1]})
   sntria_L.append({'no' : sntr[2][k], 'x' : Lx[2], 'y' : Ly[2] , 'z' : Lz[2]})
   sntrib_L.append({'no' : sntr[3][k], 'x' : Lx[3], 'y' : Ly[3] , 'z' : Lz[3]})

   for p in range (4):
    x, y , z = Rail.GetNodeXYZ(rnts[p][k])
    Lx.append(x)
    Ly.append(y)
    Lz.append(z)

   rntsra_L.append({'no' : rnts[0][k], 'x' : Lx[4], 'y' : Ly[4] , 'z' : Lz[4]})
   rntsrb_L.append({'no' : rnts[0][k], 'x' : Lx[5], 'y' : Ly[5] , 'z' : Lz[5]})
   rntsla_L.append({'no' : rnts[0][k], 'x' : Lx[6], 'y' : Ly[6] , 'z' : Lz[6]})
   rntslb_L.append({'no' : rnts[0][k], 'x' : Lx[7], 'y' : Ly[7] , 'z' : Lz[7]})

sntrea_L.sort(key=lambda d: d['x'])
sntreb_L.sort(key=lambda d: d['x'])
sntria_L.sort(key=lambda d: d['x'])
sntrib_L.sort(key=lambda d: d['x'])

rntsra_L.sort(key=lambda d: d['x'])
rntsrb_L.sort(key=lambda d: d['x'])
rntsla_L.sort(key=lambda d: d['x'])
rntslb_L.sort(key=lambda d: d['x'])

sntr_L = [sntrea_L, sntreb_L, sntria_L, sntrib_L]
rnts_L = [rntsra_L, rntsrb_L, rntsla_L, rntslb_L]
name_cmp = ['ia' , 'ib', 'ea', 'eb']


clamp_mesh, clamp_e_grp, clamp_0_grp, clamp_1_grp = [], [], [], []

for k in range(len(sntr_L)):
   for p in range(len(sntrea_L)):
    x1 , y1, z1 = sntr_L[k][p]['x'], sntr_L[k][p]['y'], sntr_L[k][p]['z']
    x2 , y2, z2 = rnts_L[k][p]['x'], rnts_L[k][p]['y'], rnts_L[k][p]['z']
    xia = x2
    clamp_vertex_0 = geompy.MakeVertex(x1, y1, z1)
    clamp_vertex_1 = geompy.MakeVertex(x2, y2, z2)
    clamp = geompy.MakeLineTwoPnt(clamp_vertex_0, clamp_vertex_1)
    clamp_e = geompy.CreateGroup(clamp, geompy.ShapeType["EDGE"])
    clamp_0 = geompy.CreateGroup(clamp, geompy.ShapeType["VERTEX"])
    clamp_1 = geompy.CreateGroup(clamp, geompy.ShapeType["VERTEX"])
    geompy.UnionIDs(clamp_e, [1])
    geompy.UnionIDs(clamp_0, [3])
    geompy.UnionIDs(clamp_1, [2])
    geompy.addToStudy( clamp, 'clamp_' +  name_cmp[k])
    geompy.addToStudyInFather( clamp, clamp_e, 'clamp_' + name_cmp[k] +'e')
    geompy.addToStudyInFather( clamp, clamp_0, 'clamp_' + name_cmp[k] +'0')
    geompy.addToStudyInFather( clamp, clamp_1, 'clamp_'+ name_cmp[k] + '1')

    # Mesh for the clamp
    clamp_mesh.append(smesh.Mesh(clamp))
    Regular_1D = clamp_mesh[-1].Segment()
    Number_of_Segments_7 = Regular_1D.NumberOfSegments(1)
    isDone = clamp_mesh[-1].Compute()
    clamp_e_grp.append(clamp_mesh[-1].GroupOnGeom(clamp_e,'clamp_' + name_cmp[k] +'e',SMESH.EDGE))
    clamp_0_grp.append(clamp_mesh[-1].GroupOnGeom(clamp_0,'clamp_' + name_cmp[k] +'0',SMESH.NODE))
    clamp_1_grp.append(clamp_mesh[-1].GroupOnGeom(clamp_1,'clamp_'+ name_cmp[k] + '1',SMESH.NODE))





# Rail 1D

cz = - 1.85 + 1.85# correction z
cy = - 6.96/2 # correction y
p1x = Rail_portion/2 + Length_element_add*Element_size 
p2x = nbrRailxp*Rail_portion 
p3x = nbrRailxn*Rail_portion
gy = 80.92 + cy
gz = 150/2


Vertex_1 = geompy.MakeVertex(p1x, railYOffset + gy +cy, halfDistBtwnRails +cz)
Vertex_2 = geompy.MakeVertex(p2x, railYOffset + gy +cy, halfDistBtwnRails +cz)
Vertex_3 = geompy.MakeVertex(-p1x, railYOffset + gy +cy, halfDistBtwnRails +cz)
Vertex_4 = geompy.MakeVertex(-p3x, railYOffset + gy +cy, halfDistBtwnRails +cz)
Full_Beam_xp = geompy.MakeLineTwoPnt(Vertex_1, Vertex_2)
Full_Beam_xn = geompy.MakeLineTwoPnt(Vertex_3, Vertex_4)

nodeForPartion_xp=[]
nodeForPartion_xn=[]
for k in range(int(nbrRailxp-nbr_sleepers_3D/2)):
   nodeForPartion_xp.append(geompy.MakeVertexOnCurveByLength(Full_Beam_xp, slpSpacing/2 + k*slpSpacing, Vertex_1))

for p in range(int(nbrRailxn-nbr_sleepers_3D/2)):
   nodeForPartion_xn.append(geompy.MakeVertexOnCurveByLength(Full_Beam_xn, slpSpacing/2 + p*slpSpacing, Vertex_3))

Beam_xp = geompy.MakePartition([Full_Beam_xp], nodeForPartion_xp, [], [], geompy.ShapeType["EDGE"], 0, [], 0)
Beam_xn = geompy.MakePartition([Full_Beam_xn], nodeForPartion_xn, [], [], geompy.ShapeType["EDGE"], 0, [], 0)

Beam_xp_bc = geompy.CreateGroup(Beam_xp, geompy.ShapeType["VERTEX"])
Beam_xn_bc = geompy.CreateGroup(Beam_xn, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Beam_xp_bc, [3])
geompy.UnionIDs(Beam_xn_bc, [3])
geompy.addToStudy( Beam_xp, 'Beam_xp' )
nodeP_pads=[]
nodeN_pads=[]

for p in range (max(len(nodeForPartion_xp),len(nodeForPartion_xn))):
   if(p < len(nodeForPartion_xp)):
      nodeP_pads.append(geompy.CreateGroup(Beam_xp, geompy.ShapeType["VERTEX"]))
      geompy.addToStudyInFather( Beam_xp, nodeP_pads[p], 'pdsS_p' + str(p+1) )
      geompy.UnionIDs(nodeP_pads[p], [4+2*p])
      
   if(p < len(nodeForPartion_xn)):
      nodeN_pads.append(geompy.CreateGroup(Beam_xn, geompy.ShapeType["VERTEX"]))
      geompy.addToStudyInFather( Beam_xn, nodeN_pads[p], 'pdsS_n' + str(p+1) )
      geompy.UnionIDs(nodeN_pads[p], [4+2*p])
   

geompy.addToStudyInFather( Beam_xp, Beam_xp_bc, 'Bm_xpBC' )
geompy.addToStudy( Beam_xn, 'Beam_xn' )
geompy.addToStudyInFather( Beam_xn, Beam_xn_bc, 'Bm_xnBC' )

# Mesh rail Beam

nbr_edges_beam = 15

Beam_xp_mesh = smesh.Mesh(Beam_xp)
Regular_1D = Beam_xp_mesh.Segment()
Number_of_Segments_1 = Regular_1D.NumberOfSegments(nbr_edges_beam)
isDone = Beam_xp_mesh.Compute()
Beam_xn_mesh = smesh.Mesh(Beam_xn)
Regular_1D_2 = Beam_xn_mesh.Segment()
Number_of_Segments_1 = Regular_1D_2.NumberOfSegments(nbr_edges_beam)
isDone = Beam_xn_mesh.Compute()

Beam_xp_mesh.GroupOnGeom(Beam_xp_bc,'Bm_xpBC',SMESH.NODE)
Beam_xn_mesh.GroupOnGeom(Beam_xn_bc,'Bm_xnBC',SMESH.NODE)
BeamRailnegative_edge = Beam_xn_mesh.CreateEmptyGroup( SMESH.EDGE, 'BmRn_e' ) # BeamRailnegative_edge
BeamRailpositive_edge = Beam_xp_mesh.CreateEmptyGroup( SMESH.EDGE, 'BmRp_e' ) # BeamRailpositive_edge
BeamRailnegative_edge.AddFrom( Beam_xn_mesh.GetMesh() )
BeamRailpositive_edge.AddFrom( Beam_xp_mesh.GetMesh() )

for p in range (max(len(nodeForPartion_xp),len(nodeForPartion_xn))):
   if(p < len(nodeForPartion_xp)):
      Beam_xp_mesh.GroupOnGeom(nodeP_pads[p],'pdsS_p' + str(p+1),SMESH.NODE)
   if(p < len(nodeForPartion_xn)):
      Beam_xn_mesh.GroupOnGeom(nodeN_pads[p],'pdsS_n' + str(p+1),SMESH.NODE)

Mesh_Model = smesh.Concatenate( [ SleeperGroup, Beam_xp_mesh, Beam_xn_mesh, Rail, Ballast_mesh] + clamp_mesh, 1, 0, 1e-05, False )
smesh.SetName(Mesh_Model.GetMesh(), 'Mesh_Model')
[ sntrea, sntreb, sntria, sntrib, rntsra, rntsrb, rntsla, rntslb] = [Mesh_Model.GetGroupByName("sntrea"),Mesh_Model.GetGroupByName("sntreb"),Mesh_Model.GetGroupByName("sntria"),Mesh_Model.GetGroupByName("sntrib"),Mesh_Model.GetGroupByName("rntsra"),Mesh_Model.GetGroupByName("rntsrb"),Mesh_Model.GetGroupByName("rntsla"),Mesh_Model.GetGroupByName("rntslb")]
[clamp_ia0, clamp_ia1, clamp_ib0,clamp_ib1,clamp_ea0,clamp_ea1,clamp_eb0,clamp_eb1] = [Mesh_Model.GetGroupByName("clamp_ia0"), Mesh_Model.GetGroupByName("clamp_ia1"), Mesh_Model.GetGroupByName("clamp_ib0"),Mesh_Model.GetGroupByName("clamp_ib1"),Mesh_Model.GetGroupByName("clamp_ea0"),Mesh_Model.GetGroupByName("clamp_ea1"),Mesh_Model.GetGroupByName("clamp_eb0"),Mesh_Model.GetGroupByName("clamp_eb1")]
coincident_nodes_on_part = Mesh_Model.FindCoincidentNodesOnPart( [sntrea[-1], sntreb[-1], sntria[-1], sntrib[-1], rntsra[-1], rntsrb[-1], rntsla[-1], rntslb[-1], clamp_ia0[-1], clamp_ia1[-1], clamp_ib0[-1],clamp_ib1[-1],clamp_ea0[-1],clamp_ea1[-1],clamp_eb0[-1],clamp_eb1[-1]], 0.001, [], 0 )
Mesh_Model.MergeNodes(coincident_nodes_on_part, [], 0)

#Creat the edges for the pads
Spring = Mesh_Model.CreateEmptyGroup( SMESH.EDGE, 'SprgPad' )


for k in range(max(len(nodeForPartion_xp),len(nodeForPartion_xn))):
   if(k < len(nodeForPartion_xp)):
      pdsS_p = Mesh_Model.GetGroupByName("pdsS_p" + str(k+1))
      pdsR_p = Mesh_Model.GetGroupByName("pdsR_p" + str(k+1))
      edgeS = Mesh_Model.AddEdge(pdsR_p[-1].GetIDs() + pdsS_p[-1].GetIDs() )
      Spring.Add([edgeS])
   if(k < len(nodeForPartion_xn)):
      pdsS_n = Mesh_Model.GetGroupByName("pdsS_n" + str(k+1))
      pdsR_n = Mesh_Model.GetGroupByName("pdsR_n" + str(k+1))
      edgeR = Mesh_Model.AddEdge(pdsR_n[-1].GetIDs() + pdsS_n[-1].GetIDs() )
      Spring.Add([edgeR])

   
try:
  Mesh_Model.ExportMED(properties["mesh"],auto_groups=0,minor=40,overwrite=1,meshPart=None,autoDimension=1)
  pass
except:
  print('ExportMED() failed. Invalid file name?')




if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
