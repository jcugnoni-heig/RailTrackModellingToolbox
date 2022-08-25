#!/bin/bash

# setup script for Railtrack modelling toolbox

##
echo ""
echo " **** RAILTRACK MODELLING TOOLBOX SETUP **** "
echo ""

echo "1. setting all subdirs as writable"
chmod -R a+rwX *

echo "2. changing all shell .sh file as executable"
find -iname "*.sh" -exec chmod a+x {} \;

changepathfiles=`find -iname changePath.sh`
echo " "
echo "  - updating paths for code-aster models (.export files)"
echo " "
for item in $changepathfiles 
do
  echo " executing " $item
  $item
done

echo " setup DONE ! "
