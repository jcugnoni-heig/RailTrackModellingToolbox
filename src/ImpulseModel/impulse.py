import os
import sys
import shutil
import json

print(sys.argv)
parametersFile = sys.argv[1]
#TODO : Il y aura plus besoin de ça quand ce sera dans la toolbox
DevFiles = '/opt/RailTrackModellingToolbox/src/ImpulseModel'
generateMeshFile = os.path.join(DevFiles, "generateMesh.py")
MaxwellGFile = os.path.join(DevFiles, "GeneralizedMaxwell.mfront")
commFile = os.path.join(DevFiles, "impulse.comm")
exportFile = os.path.join(DevFiles, "impulse.export")

with open(parametersFile, 'r') as f:
	txt = f.read()

material = json.loads(txt)
simu_dir = material["simu_folder"]
meshFile = material["mesh"]
debug = material["debug"]
Generate_mesh = material['Geometry']["Creat_geom"]
run_simulation = material["run_simulation"]
memlim = material["memlim"]
nCPUs = material["nCPUs"]
reptrav = material["reptrav"]

if(Generate_mesh):
	os.system('xterm -e' 
				+ ' /opt/SalomeMeca/appli_V2019_univ/salome -t ' 
				+ generateMeshFile 
				+ ' args:' 
				+ parametersFile)

try:
	shutil.rmtree(simu_dir)
except:
	pass
		
try:
	os.makedirs(simu_dir)
except:
	print("The folder " + simu_dir + " could not be created.")

try:
	shutil.copyfile(exportFile, os.path.join(simu_dir, 'impulse.export'))
	shutil.copyfile(commFile, os.path.join(simu_dir, 'impulse.comm'))
	shutil.copyfile(meshFile, os.path.join(simu_dir, 'mesh.med'))
	shutil.copyfile(parametersFile, os.path.join(simu_dir, 'material_prop.json'))
	shutil.copyfile(MaxwellGFile, os.path.join(simu_dir, 'GeneralizedMaxwell.mfront'))
except Exception as e:
	print("Error occurred while copying files:", e)

try:
	os.system('sed -i -E "s!__simu_dir__!' + simu_dir + '!" ' + os.path.join(simu_dir, 'impulse.export'))
	os.system('sed -i -E "s!__memjob__!' + str(memlim*1024) + '!" ' + os.path.join(simu_dir, 'impulse.export'))
	os.system('sed -i -E "s!__memlim__!' + str(memlim) + '!" ' + os.path.join(simu_dir, 'impulse.export'))
	os.system('sed -i -E "s!__memjeveux__!' + str(memlim/4) + '!" ' + os.path.join(simu_dir, 'impulse.export'))
	os.system('sed -i -E "s!__ncpus__!' + str(nCPUs) + '!" ' + os.path.join(simu_dir, 'impulse.export'))
	os.system('sed -i -E "s!__reptrav__!' + str(reptrav) + '!" ' + os.path.join(simu_dir, 'impulse.export'))

except Exception as e:
	print("Error occurred while running sed command:", e)


if(run_simulation):
	hold_option = '-hold' if debug else ''
	code = os.system('xterm ' 
					+ hold_option 
					+ ' -e sh -c "export PATH=\$PATH:/opt/aster/public/tfel-3.2.1/bin && /opt/aster/bin/as_run' 
					+ ' ' 
					+ os.path.join(simu_dir, 'impulse.export') 
					+ '"')
	print("Exit code: ", code)