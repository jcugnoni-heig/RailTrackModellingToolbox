#!/bin/bash

# CONVERT ABAQUS MESH TO ASTER 

## INPUT PARAMETERS
offsetX="-79.0"
offsetY="50.0"
offsetZ="0.0"

ROTAXIS="x"
ROTANGL="-90.0"

INPUTFILE="Export_Aster.inp"

## SETTINGS
CGXTEMPLATE="meshConv.tpl"
CGXINPUT="meshConv.in"
CGXPATH=__path__CGX
ASRUNPATH=__path__asRun
ASRUNJOB="meshConvert.export"

## EXECUTION
### prep CGX execution
sed -e "s/{offsetX}/$offsetX/g" -e "s/{offsetY}/$offsetY/g" -e "s/{offsetZ}/$offsetZ/g" -e "s/{ROTAXIS}/$ROTAXIS/g" -e "s/{ROTANGL}/$ROTANGL/g" -e "s/{INPUTFILE}/$INPUTFILE/g" $CGXTEMPLATE > $CGXINPUT
### run CGX
$CGXPATH -bg $CGXINPUT
### run ASTER to convert MAIL mesh to MED format (all.mail => importedPad.mesh.med)
$ASRUNPATH $ASRUNJOB

