#!/bin/bash

sourcePath=/home/cae/Documents/Railpad2/ImpulseAster_GUI/impulse3sleeper
destPath=/home/cae/Documents/Railpad2/ImpulseAster_GUI/working_directory

sed -i "s#$sourcePath#$destPath#g" *.astk
sed -i "s#$sourcePath#$destPath#g" *.export


