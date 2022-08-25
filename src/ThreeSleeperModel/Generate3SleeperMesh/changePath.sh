#!/bin/bash
SCRIPT=$(realpath "$0")
# change paths to match current installation

#detect previous path from .export files 
src=$(grep "F comm" *.export | head -1 | cut -d " " -f 3)
sourcePath=${src%/*}

destPath=${SCRIPT%/*}

echo "************"
echo "Changing all paths in .export & .astk files from :"
echo $sourcePath
echo "to"
echo $destPath
echo "************"


read -p "Do you want to proceed? (y/n) " yn

case $yn in 
	[yY] ) echo ok, we will proceed;
             sed -i "s#$sourcePath#$destPath#g" *.astk
             sed -i "s#$sourcePath#$destPath#g" *.export
             exit;;
	[nN] ) echo exiting...;
		exit;;
	* ) echo invalid response;
		exit 1;;
esac
