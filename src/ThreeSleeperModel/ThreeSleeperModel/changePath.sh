#!/bin/bash

sourcePath=/home/cae/Documents/Railpad2/ThreeSleeperAster/vibroAcoustic/harmo3sleeper_GUI
destPath=/home/cae/Documents/Railpad2/ModellingToolbox/src/ThreeSleeperModel/ThreeSleeperModel

sed -i "s#$sourcePath#$destPath#g" *.astk
sed -i "s#$sourcePath#$destPath#g" *.export


