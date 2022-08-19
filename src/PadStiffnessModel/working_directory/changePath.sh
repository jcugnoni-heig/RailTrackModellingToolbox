#!/bin/bash

sourcePath=/home/cae/Documents/Railpad2/PadStiffness_GUI/harmoPadStiffness
destPath=/home/cae/Documents/Railpad2/PadStiffness_GUI/working_directory

sed -i "s#$sourcePath#$destPath#g" *.astk
sed -i "s#$sourcePath#$destPath#g" *.export

