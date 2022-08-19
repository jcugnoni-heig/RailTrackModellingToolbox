#!/bin/bash

sourcePath=convMesh
destPath=ConvertAbaqusPadMesh

sed -i "s#$sourcePath#$destPath#g" *.astk
sed -i "s#$sourcePath#$destPath#g" *.export