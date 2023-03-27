#!/bin/bash

sourcePath=/home/cae/Documents/TrackSystemEvaluation/materialFit
destPath=/home/cae/Documents/Railpad3/Toolbox_Work/src/PropertiesIdentification/Sleepers

sed -i "s#$sourcePath#$destPath#g" *.astk
sed -i "s#$sourcePath#$destPath#g" *.export

