#!/bin/bash

sourcePath=/home/cae/Documents/Railpad2/PadStiffness_GUI/working_directory
destPath=/home/cae/Documents/TrackSystemEvaluation/materialFit

sed -i "s#$sourcePath#$destPath#g" *.astk
sed -i "s#$sourcePath#$destPath#g" *.export

