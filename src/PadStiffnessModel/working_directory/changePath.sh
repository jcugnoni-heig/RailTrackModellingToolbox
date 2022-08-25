#!/bin/bash
SCRIPT=$(realpath "$0")
destPath=${SCRIPT%/*}

# change paths to match current installation

#detect previous path from .export files 
src=$(grep "F comm" $destPath/*.export | head -1 | cut -d " " -f 3)
sourcePath=${src%/*}


echo "************"
echo "Changing all paths in .export & .astk files from :"
echo $sourcePath
echo "to"
echo $destPath
echo "************"


read -p "Do you want to proceed? (y/n) " yn

case $yn in 
	[yY] ) echo ok, we will proceed;
             sed -i "s#$sourcePath#$destPath#g" $destPath/*.astk
             sed -i "s#$sourcePath#$destPath#g" $destPath/*.export
             exit;;
	[nN] ) echo exiting...;
		exit;;
	* ) echo invalid response;
		exit 1;;
esac
