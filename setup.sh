#!/bin/bash

pythonPath="python3"
salomePath="/opt/SalomeMeca/appli_V2019_univ/salome"
asRunPath="/opt/SalomeMeca/V2019_univ/tools/Code_aster_frontend-20190/bin/as_run"
asRunImpulsePath="/opt/aster/bin/as_run"

# Define below all pairs of strings (paths) that must be replaced
declare -A maListe=(
    ["__path__python"]=$pythonPath
    ["__path__salome"]=$salomePath
    ["__path__asRun"]=$asRunPath
    ["__path__asRunImpulse"]=$asRunImpulsePath
    ["__path__ldLibrary"]="/opt/qt511/lib"
    ["__path__setEnvMfront1"]="/opt/aster/bin:/opt/aster/outils:/opt/ThirdParty-4.1/platforms/linux64Gcc/gperftools-svn/bin:/opt/paraviewopenfoam50/bin:/home/cae/OpenFOAM/cae-4.1/platforms/linux64GccDPInt32Opt/bin:/opt/site/4.1/platforms/linux64GccDPInt32Opt/bin:/opt/openfoam4/platforms/linux64GccDPInt32Opt/bin:/opt/openfoam4/bin:/opt/openfoam4/wmake:/home/cae/bin:/home/cae/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/opt/abaqus/Commands:/opt/MATLAB80/bin:/opt/aster/public/tfel-3.2.1/bin/:/opt/aster/public/tfel-3.2.1/bin/"
    ["__path__setEnvMfront2"]="/usr/lib:/opt/ThirdParty-4.1/platforms/linux64Gcc/gperftools-svn/lib:/opt/paraviewopenfoam50/lib/paraview-5.0:/opt/openfoam4/platforms/linux64GccDPInt32Opt/lib/openmpi-system:/opt/ThirdParty-4.1/platforms/linux64GccDPInt32/lib/openmpi-system:/usr/lib/openmpi/lib:/home/cae/OpenFOAM/cae-4.1/platforms/linux64GccDPInt32Opt/lib:/opt/site/4.1/platforms/linux64GccDPInt32Opt/lib:/opt/openfoam4/platforms/linux64GccDPInt32Opt/lib:/opt/ThirdParty-4.1/platforms/linux64GccDPInt32/lib:/opt/openfoam4/platforms/linux64GccDPInt32Opt/lib/dummy:/opt/aster/public/tfel-3.2.1/lib:/opt/aster/public/tfel-3.2.1/lib"
    ["__path__CGX"]="/opt/CLCX-caelinux64/bin/cgx2.12"
)

##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
# START TOOLBOX SETUP

echo ""
echo " **** RAILTRACK MODELLING TOOLBOX SETUP **** "
echo ""

echo "1. Setting all subdirs as writable"
chmod -R a+rwX *
echo -e "Done\n"

echo "2. Changing all shell .sh files as executable"
find -iname "*.sh" -exec chmod a+x {} \;
echo -e "Done\n"

echo "3. Updating all paths in files"

# List of potentially modified files
modified_files=""

# Traverse all files for potential modifications
while IFS= read -r -d '' file; do
    file_modified=false
    
    # Check if the file contains any of the strings to replace
    for search_string in "${!maListe[@]}"; do
        if grep -q "$search_string" "$file"; then
            file_modified=true
            break
        fi
    done

    # If the file has potentially been modified, add it to the list
    if [ "$file_modified" = true ]; then
        modified_files+="$file\n"
    fi
done < <(find . -type f ! -name 'setup.sh' -print0)

# Display potentially modified files
echo -e "Potentially modified files are:"
echo -e "$modified_files"

# Confirmation before modifying the files
read -p "Do you want to proceed with modifications? (y/n): " confirmation
if [ "$confirmation" = "y" ]; then
    # Perform replacements for each string pair in the associative array
    for search_string in "${!maListe[@]}"; do
        replace_string=${maListe[$search_string]}
        find . -type f ! -name 'setup.sh' -exec sed -i -E "s@$search_string@$replace_string@g" {} +
    done
    echo "Modifications successfully applied."
else
    echo "No modifications were made."
fi
