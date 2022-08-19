#!/bin/bash

sourcePath=gen3Sleepers
destPath=Generate3SleeperMesh

sed -i "s#$sourcePath#$destPath#g" *.astk
sed -i "s#$sourcePath#$destPath#g" *.export


