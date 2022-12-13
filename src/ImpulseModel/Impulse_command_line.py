import sys
import json
import os
import shutil

# Extraction of the argument list in "argv_list"
input_data = sys.argv[1]



def MoveAndRename( src_folder, dst_folder, fileOldName, fileNewName):
    
    # Moving the file in WD
    sourceFile = os.path.join(src_folder, fileOldName)
    destinationFile = os.path.join(dst_folder, fileOldName)
    # Moving the file
    shutil.copyfile(sourceFile, destinationFile)
    # Renaming the file in WD
    destinationFileOldName = os.path.join(dst_folder, fileOldName)
    destinationFileNewName = os.path.join(dst_folder, fileNewName)
    os.rename(destinationFileOldName, destinationFileNewName)

def MoveOnly( src_folder, dst_folder, fileName):
    
    # Moving the file in WD
    sourceFile = os.path.join(src_folder, fileName)
    destinationFile = os.path.join(dst_folder, fileName)
    # Moving the file
    shutil.copyfile(sourceFile, destinationFile)


def MovePadsMXFiles(mx, mx_num):
    
    if (mx_num == 1):
        mx_type = 'mx1'
    if (mx_num == 2):
        mx_type = 'mx2'
    # Moving the material1 properties files in WD
    # E1
    src = os.path.join(padmaterialspath, mx)
    dst = working_directorypath
    fileOldName = 'E.csv'
    fileNewName = 'E_' + mx_type + '.csv'
    MoveAndRename(src, dst, fileOldName, fileNewName)
    # G1
    src = os.path.join(padmaterialspath, mx)
    dst = working_directorypath
    fileOldName = 'G.csv'
    fileNewName = 'G_' + mx_type + '.csv'
    MoveAndRename(src, dst, fileOldName, fileNewName)
    # K1
    src = os.path.join(padmaterialspath, mx)
    dst = working_directorypath
    fileOldName = 'K.csv'
    fileNewName = 'K_' + mx_type + '.csv'
    MoveAndRename(src, dst, fileOldName, fileNewName)
    # tau1
    src = os.path.join(padmaterialspath, mx)
    dst = working_directorypath
    fileOldName = 'tau.csv'
    fileNewName = 'tau_' + mx_type + '.csv'
    MoveAndRename(src, dst, fileOldName, fileNewName)
    # Poisson's Ratio1
    src = os.path.join(padmaterialspath, mx)
    dst = working_directorypath
    fileOldName = 'poisson.csv'
    fileNewName = 'poisson_' + mx_type + '.csv'
    MoveAndRename(src, dst, fileOldName, fileNewName)
    # Density1
    src = os.path.join(padmaterialspath, mx)
    dst = working_directorypath
    fileOldName = 'density.csv'
    fileNewName = 'density_' + mx_type + '.csv'
    MoveAndRename(src, dst, fileOldName, fileNewName)


filepath = os.getcwd()
working_directorypath = os.path.join(filepath,'working_directory')
messagespath = os.path.join(working_directorypath,'messages')
padmaterialspath = os.path.join(filepath,'materials/Pad')
sleepermaterialspath = os.path.join(filepath,'materials/Sleeper')
railmaterialspath = os.path.join(filepath,'materials/Rail')
ballastmaterialspath = os.path.join(filepath,'materials/Ballast')
padmeshespath = os.path.join(filepath,'meshes/Pads')
sleepermeshespath = os.path.join(filepath,'meshes/Sleepers')
railmeshespath = os.path.join(filepath,'meshes/Rails')
ballastmeshespath = os.path.join(filepath,'meshes/Ballasts')



with open(input_data) as json_file:
    data = json.load(json_file)

print("Name of the study:", data['name'])

resultsDirectoryName = data['name']
resultsDirectoryPath = os.path.join(data['path'], resultsDirectoryName)
    
    # Create user folders for results
try:
    os.mkdir(resultsDirectoryPath)
    os.mkdir(os.path.join(resultsDirectoryPath,'med_files'))
    os.mkdir(os.path.join(resultsDirectoryPath,'results_files'))
    os.mkdir(os.path.join(resultsDirectoryPath,'message_files'))
    os.mkdir(os.path.join(resultsDirectoryPath,'mesh_assembly'))
except:
    print("Problem creating the results folders. Maybe the folder already exist ?")
# Create a file for the study parameters
with open(os.path.join(resultsDirectoryPath,'study_parameters.txt'),'a+') as fp:
    fp.write('Here are the parameters selected for the sutdy: ' + resultsDirectoryName + '\n\n')

# Moving the meshes file in WD
srcPad = os.path.join(padmeshespath, data['meshes']['pad'])
srcSleeper = os.path.join(sleepermeshespath, data['meshes']['sleeper'])
srcRail = os.path.join(railmeshespath, data['meshes']['rail'])
srcBallast = os.path.join(ballastmeshespath, data['meshes']['ballast'])
dst = working_directorypath
filePadOldName = os.listdir(srcPad)[0]
fileSleeperOldName = os.listdir(srcSleeper)[0]
fileRailOldName = os.listdir(srcRail)[0]
fileBallastOldName = os.listdir(srcBallast)[0]
filePadNewName = 'pad.med'
fileSleeperNewName = 'sleeper.med'
fileRailNewName = 'rail.med'
fileBallastNewName = 'ballast.med'
try:
    MoveAndRename(srcPad, dst, filePadOldName, filePadNewName)
    MoveAndRename(srcSleeper, dst, fileSleeperOldName, fileSleeperNewName)
    MoveAndRename(srcRail, dst, fileRailOldName, fileRailNewName)
    MoveAndRename(srcBallast, dst, fileBallastOldName, fileBallastNewName)
except:
    print("A problem occure while copying the mesh files from the mesh folder to the working directory.")

# Create a file for the clamps properties
with open(os.path.join(working_directorypath,'clamps_properties.txt'),'a+') as fp:
    fp.write('Stiffness:\n')
    fp.write(str(data['clamps properties']['stiffness X']) + '\n')
    fp.write(str(data['clamps properties']['stiffness Y']) + '\n')
    fp.write(str(data['clamps properties']['stiffness Z']) + '\n')
    fp.write('Damping:\n')
    fp.write(str(data['clamps properties']['damping X']) + '\n')
    fp.write(str(data['clamps properties']['damping Y']) + '\n')
    fp.write(str(data['clamps properties']['damping Z']) + '\n')

# Create a file for the distance between sleepers 
with open(os.path.join(working_directorypath,'sleeperDistance.csv'),'a+') as fp:
    fp.write(str(data['sleeper distance']))

# Add info in the file of parameters
with open(os.path.join(resultsDirectoryPath,'study_parameters.txt'),'a') as fp:
    fp.write('The selected meshes are:\n')
    fp.write('Pads: ' + '\n' + data['meshes']['pad'] + '\n')
    fp.write('Sleepers: ' + '\n' + data['meshes']['sleeper'] + '\n')
    fp.write('Rails: ' + '\n' + data['meshes']['rail'] + '\n')
    fp.write('Ballast: ' + '\n' + data['meshes']['ballast'] + '\n\n')
    fp.write('Distance between sleepers: ' + str(data['sleeper distance']) + '\n\n')

# Add info in the file of parameters
with open(os.path.join(resultsDirectoryPath,'study_parameters.txt'),'a') as fp:
    fp.write('Pads properties:\n')
    fp.write('The material 1 is: ' + data['materials']['pad1'] + '\n')
    fp.write('The material 2 is: ' + data['materials']['pad2'] + '\n\n')
    fp.write('Sleepers properties:\n')
    fp.write('The sleeper\'s material is: ' + data['materials']['sleeper'] + '\n\n')
    fp.write('Rails properties:\n')
    fp.write('The rail\'s material is: ' + data['materials']['rail'] + '\n\n')
    fp.write('Ballasts properties:\n')
    fp.write('The ballast\'s material is: ' + data['materials']['ballast'] + '\n\n')
    fp.write('Clamps properties:\n')
    fp.write('Stiffness:\n')
    fp.write('X : ' + str(data['clamps properties']['stiffness X']) + '[MPa]\n')
    fp.write('Y : ' + str(data['clamps properties']['stiffness Y']) + '[MPa]\n')
    fp.write('Z : ' + str(data['clamps properties']['stiffness Z']) + '[MPa]\n')
    fp.write('Damping:\n')
    fp.write('X : ' + str(data['clamps properties']['damping X']) + '[-]\n')
    fp.write('Y : ' + str(data['clamps properties']['damping Y']) + '[-]\n')
    fp.write('Z : ' + str(data['clamps properties']['damping Z']) + '[-]\n\n')

# Run the cmmande file to assemble the mesh
os.system('cd working_directory \n ./gen3SleepersMesh.sh')

# Run the script in salome to add the edges
os.system('/opt/SalomeMeca/appli_V2019_univ/salome -t ' + working_directorypath + '/script_to_add_edges.py')

# Open the mesh in salome
os.system('/opt/SalomeMeca/runSalome2019.sh ' + working_directorypath + '/open_mesh.py')

isOK = raw_input("Is the mesh assembly ok ? [y/n]  ")

if(isOK == 'y' or isOK == 'yes'):
    print('Ok, let\'s GO!!')

    # Moving the materials files in WD
    # pads
    try:
        MovePadsMXFiles(data['materials']['pad1'], 1)
        MovePadsMXFiles(data['materials']['pad2'], 2)
    except:
        print("Problem copying the pads material files to the working directory.")
        # Delete files of the sutdy
        listOfFileToDelete = ['pad.med', 'sleeper.med', 'rail.med', 'ballast.med',
                                'clamps_properties.txt',
                                'unitCell.med', 'unitCellWithClamps.med']
        for fileToDelete in listOfFileToDelete:
            os.remove(os.path.join(working_directorypath, fileToDelete))
        # removing directory
        shutil.rmtree(resultsDirectoryPath)


    # sleeper
    try:
        listOfFiles = ['sleeper_E.csv','sleeper_Nu.csv','sleeper_Rho.csv','sleeper_AmHyst.csv']
        src = os.path.join(sleepermaterialspath, data['materials']['sleeper'])
        dst = working_directorypath
        for fileName in listOfFiles:
            MoveOnly(src, dst, fileName)
    except:
        print("Problem copying the sleepers material files to the working directory.")
        # Delete files of the sutdy
        listOfFileToDelete = ['pad.med', 'sleeper.med', 'rail.med', 'ballast.med',
                                'E_mx1.csv', 'G_mx1.csv', 'K_mx1.csv', 'tau_mx1.csv', 'poisson_mx1.csv', 'density_mx1.csv',
                                'E_mx2.csv', 'G_mx2.csv', 'K_mx2.csv', 'tau_mx2.csv', 'poisson_mx2.csv', 'density_mx2.csv',
                                'clamps_properties.txt', 'sleeperDistance.csv',
                                'unitCell.med', 'unitCellWithClamps.med']
        for fileToDelete in listOfFileToDelete:
            os.remove(os.path.join(working_directorypath, fileToDelete))
        # removing directory
        shutil.rmtree(resultsDirectoryPath)


    # rail
    try:
        listOfFiles = ['rail_E.csv','rail_Nu.csv','rail_Rho.csv','rail_AmHyst.csv']
        src = os.path.join(railmaterialspath, data['materials']['rail'])
        dst = working_directorypath
        for fileName in listOfFiles:
            MoveOnly(src, dst, fileName)
    except:
        print("Problem copying the rails material files to the working directory.")
        # Delete files of the sutdy
        listOfFileToDelete = ['pad.med', 'sleeper.med', 'rail.med', 'ballast.med',
                                'E_mx1.csv', 'G_mx1.csv', 'K_mx1.csv', 'tau_mx1.csv', 'poisson_mx1.csv', 'density_mx1.csv',
                                'E_mx2.csv', 'G_mx2.csv', 'K_mx2.csv', 'tau_mx2.csv', 'poisson_mx2.csv', 'density_mx2.csv',
                                'sleeper_E.csv','sleeper_Nu.csv','sleeper_Rho.csv','sleeper_AmHyst.csv',
                                'clamps_properties.txt', 'sleeperDistance.csv',
                                'unitCell.med', 'unitCellWithClamps.med']
        for fileToDelete in listOfFileToDelete:
            os.remove(os.path.join(working_directorypath, fileToDelete))
        # removing directory
        shutil.rmtree(resultsDirectoryPath)


    # ballast
    try:
        listOfFiles = ['ballast_E.csv','ballast_Nu.csv','ballast_Rho.csv','ballast_AmHyst.csv']
        src = os.path.join(ballastmaterialspath, data['materials']['ballast'])
        dst = working_directorypath
        for fileName in listOfFiles:
            MoveOnly(src, dst, fileName)
    except:
        print("Problem copying the ballast material files to the working directory.")
        # Delete files of the sutdy
        listOfFileToDelete = ['pad.med', 'sleeper.med', 'rail.med', 'ballast.med',
                                'E_mx1.csv', 'G_mx1.csv', 'K_mx1.csv', 'tau_mx1.csv', 'poisson_mx1.csv', 'density_mx1.csv',
                                'E_mx2.csv', 'G_mx2.csv', 'K_mx2.csv', 'tau_mx2.csv', 'poisson_mx2.csv', 'density_mx2.csv',
                                'sleeper_E.csv','sleeper_Nu.csv','sleeper_Rho.csv','sleeper_AmHyst.csv',
                                'rail_E.csv','rail_Nu.csv','rail_Rho.csv','rail_AmHyst.csv',
                                'clamps_properties.txt', 'sleeperDistance.csv',
                                'unitCell.med', 'unitCellWithClamps.med']
        for fileToDelete in listOfFileToDelete:
            os.remove(os.path.join(working_directorypath, fileToDelete))
        # removing directory
        shutil.rmtree(resultsDirectoryPath)


    
    # Run phase I
    os.system('cd working_directory \n ./runImpulsePhase1.sh')

    # Run phase II
    os.system('cd working_directory \n ./runImpulsePhase2_command_line.sh')

    
    message_copied = True
    med_result_copied = True
    mesh_assembly_copied = True
    txt_results_copied = True

    # Copy messages in User folder
    try:
        listOfFile = ['messageImpulsePhase1.mess','messageImpulsePhase2.mess']
        src = messagespath
        dst = os.path.join(resultsDirectoryPath,'message_files')
        for fileName in listOfFile:
            MoveOnly(src, dst, fileName)
    except:
        print("Problem while copying the message files from the working directory to the result folder.")
        message_copied = False
    

    # Copy med results in User folder
    try:
        listOfFile = ['resultImpulse.res.med']
        src = working_directorypath
        dst = os.path.join(resultsDirectoryPath,'med_files')
        for fileName in listOfFile:
            MoveOnly(src, dst, fileName)
    except:
        print("Problem while copying the .med results file from the working directory to the result folder.")
        med_result_copied = False
    

    # Copy mesh assembly in User folder
    try:
        listOfFile = ['unitCellWithClamps.med']
        src = working_directorypath
        dst = os.path.join(resultsDirectoryPath,'mesh_assembly')
        for fileName in listOfFile:
            MoveOnly(src, dst, fileName)
    except:
        print("Problem while copying the mesh assembly file from the working directory to the result folder.")
        mesh_assembly_copied = False
    

    # Copy impulse results in User folder
    try:
        listOfFile = ['Resultats_ballast_impulse_INVAR.txt', 'Resultats_ballast_impulse_SGIM.txt', 'Resultats_impulse.txt']
        src = working_directorypath
        dst = os.path.join(resultsDirectoryPath,'results_files')
        for fileName in listOfFile:
            MoveOnly(src, dst, fileName)
    except:
        print("Problem while copying the extracted text results files from the working directory to the result folder.")
        txt_results_copied = False



    # Delete files of the sutdy (mx, mesh, message, res.med...etc)
    listOfFileToDelete = ['E_mx1.csv', 'G_mx1.csv', 'K_mx1.csv', 'tau_mx1.csv', 'poisson_mx1.csv', 'density_mx1.csv',
                    'E_mx2.csv', 'G_mx2.csv', 'K_mx2.csv', 'tau_mx2.csv', 'poisson_mx2.csv', 'density_mx2.csv',
                    'sleeper_E.csv','sleeper_Nu.csv','sleeper_Rho.csv','sleeper_AmHyst.csv',
                    'rail_E.csv','rail_Nu.csv','rail_Rho.csv','rail_AmHyst.csv',
                    'ballast_E.csv','ballast_Nu.csv','ballast_Rho.csv','ballast_AmHyst.csv',
                    'pad.med', 'sleeper.med', 'rail.med', 'ballast.med',
                    'clamps_properties.txt', 'sleeperDistance.csv',
                    'unitCell.med']

    if(med_result_copied):
        listOfFileToDelete = listOfFileToDelete + ['resultImpulse.res.med']

    if(mesh_assembly_copied):
        listOfFileToDelete = listOfFileToDelete + ['unitCellWithClamps.med']

    if(txt_results_copied):
        listOfFileToDelete = listOfFileToDelete + ['Resultats_ballast_impulse_INVAR.txt', 'Resultats_ballast_impulse_SGIM.txt', 'Resultats_impulse.txt']

    for fileToDelete in listOfFileToDelete:
        os.remove(os.path.join(working_directorypath, fileToDelete))

    if(message_copied):
        listOfFileToDelete2 = ['messageImpulsePhase1.mess','messageImpulsePhase2.mess']
        for fileToDelete in listOfFileToDelete2:
            os.remove(os.path.join(messagespath, fileToDelete))

if(isOK == 'n' or isOK == 'no'):
    print('No problems, modify the input file and start again...')

    # Delete files of the sutdy (mx, mesh, message, res.med...etc)
    listOfFileToDelete = ['pad.med', 'sleeper.med', 'rail.med', 'ballast.med',
                    'clamps_properties.txt', 'sleeperDistance.csv',
                    'unitCell.med', 'unitCellWithClamps.med']
    for fileToDelete in listOfFileToDelete:
        os.remove(os.path.join(working_directorypath, fileToDelete))
    
    # removing directory
    shutil.rmtree(resultsDirectoryPath)
