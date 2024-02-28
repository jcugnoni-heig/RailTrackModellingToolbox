import os
import shutil
import time
import math
import json
from datetime import datetime

def RunSimulation(p_dictSimu):

	reptravroot = p_dictSimu.get('reptrav')
	reptrav1 = os.path.join(reptravroot, 'cae-caesrv1-interactif_0101')

	try:
		shutil.rmtree(reptrav1)
	except:
		pass

	nJobs = p_dictSimu.get('nJobs')
	for i in range(nJobs):
		reptrav2 = os.path.join(reptravroot, 'cae-caesrv1-interactif_0102' + str(i+1))
		try:
			shutil.rmtree(reptrav2)
		except:
			pass

	if p_dictSimu.get('computeModes') == True:

		now = datetime.now()
		date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
		modesFolder = p_dictSimu['modesFolder']
		modesName = os.path.basename(modesFolder)
		print('[' + date_time + '] Running eigenmodes simulation: "' + modesName + '" ...')

		code = RunJobModes(p_dictSimu)
		if code != 0:
			return code
		
		now = datetime.now()
		date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
		print('[' + date_time + '] Eigenmodes simulation: "' + modesName + '" over.')

	now = datetime.now()
	date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
	simuName = p_dictSimu['name']
	print('[' + date_time + '] Running harmonic simulation: "' + simuName + '" ...')
	
	code = RunJobHarmo(p_dictSimu)
	if code != 0:
		return code

	now = datetime.now()
	date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
	simuName = p_dictSimu['name']
	print('[' + date_time + '] Harmonic simulation: "' + simuName + '" over.')
		
	return 0
		


def CreateMesh(p_dictSimu):

	reptravroot = p_dictSimu.get('reptrav')
	reptrav1 = os.path.join(reptravroot, 'cae-caesrv1-interactif_0100')

	try:
		shutil.rmtree(reptrav1)
	except:
		pass

	code = RunJobModes(p_dictSimu, True)
	return code
		
		
		
def RunJobModes(p_dictSimu, p_createMeshOnly=False):
	code = PrepareFilesPhase1(p_dictSimu, p_createMeshOnly)
	if code != 0:
		return code
	
	cwd = p_dictSimu['cwd']
	simFolder = p_dictSimu['phase1WorkingDir']
	modesFolder = p_dictSimu['modesFolder']
	messageFile = os.path.join(cwd, 'DevFiles', 'Messages', 'message_modesSimu.mess')
	debugMode = p_dictSimu['debugPh1']

	if p_createMeshOnly:
		debugMode = False

	code = RunMultiJobs(cwd, simFolder, 'computeModes', 1, messageFile, debugMode)

	if p_createMeshOnly:
		try:
			shutil.copyfile(os.path.join(simFolder, 'mesh.med'), os.path.join(modesFolder, 'mesh.med'))
		except:
			return "Error copying " + os.path.join(simFolder, 'mesh.med') + " to " + os.path.join(modesFolder, 'mesh.med')
		return code

	try:
		shutil.copyfile(messageFile, os.path.join(simFolder, 'message_modesSimu.mess'))
	except:
		return "Could not copy message_modesSimu.mess to " + simFolder

	if code != 0:
		return code
		
	code = SaveBaseFiles(p_dictSimu, modesFolder, simFolder)
	if code != 0:
		return code
		
	code = DeletePycFiles(p_dictSimu['appPath'])
	if code != 0:
		return code

	return 0
	
def RunJobHarmo(p_dictSimu):
	code = PrepareFilesPhase2(p_dictSimu)
	if code != 0:
		return code
	
	cwd = p_dictSimu['cwd']
	simFolder = os.path.join(p_dictSimu.get('simuParentFolder'), p_dictSimu.get('name'))
	nJobs = p_dictSimu['nJobs']
	messageFile = os.path.join(cwd, 'DevFiles', 'Messages', 'message_harmonicSimu_b1.mess')
	debugMode = p_dictSimu['debugPh2']
		
	code = RunMultiJobs(cwd, simFolder, 'runSimulation_b', nJobs, messageFile, debugMode)

	try:
		shutil.copyfile(messageFile, os.path.join(simFolder, 'Outputs', 'message_harmonicSimu_b1.mess'))
	except:
		return "Could not copy message_harmonicSimu_b1.mess to harmonic simulation outputs directory."

	if code != 0:
		return code
	
	code = PostProcessResults(p_dictSimu)
	if code != 0:
		return code
	
	code = DeletePycFiles(cwd)
	if code != 0:
		return code

	return 0
		
def PrepareFilesPhase1(p_dictSimu, p_createMeshOnly=False):
	# Create empty simulation folder
	fullDir = p_dictSimu.get('phase1WorkingDir')

	# Phase 1: if different mat props but same mesh (no sleeper shift), and computeModeShapesPh1 False, no need to compute new macroelement mode shapes.
	# True if either: a separate macroEl is requested for macroEl2, or a sleeper shift is set (!=0)
	bool_macroEl2_Ph1 = ('macroEl2' in p_dictSimu.keys()) and ((("computeModeShapesPh1" in p_dictSimu['macroEl2'].keys()) and (p_dictSimu['macroEl2']['computeModeShapesPh1'] is True)) or (("slpShift" in p_dictSimu['macroEl2'].keys()) and (p_dictSimu['macroEl2']['slpShift'] !=0)))
	
	try:
		shutil.rmtree(fullDir)
	except:
		pass
		
	try:
		os.makedirs(fullDir)
	except:
		return "The folder " + fullDir + " could not be created (modes simulation)."
	
	# Create JSON parameter file
	p_dictSimu['createMeshOnly'] = p_createMeshOnly

	try:
		txt = json.dumps(p_dictSimu, indent = 4, sort_keys=True)
		jsonPath = os.path.join(fullDir, 'parameters.json')
		with open(jsonPath, 'w') as f:
			f.write(txt)
		f.close()
	except:
		return jsonPath + ' could not be created (modes simulation).'
	
	# Copy materials properties files
	try:
		# E pad 1 (nominal macroel, macro2)
		shutil.copyfile(p_dictSimu.get('Emat1'), os.path.join(fullDir, 'E_mat1.csv'))
		if bool_macroEl2_Ph1 and 'Emat1' in p_dictSimu['macroEl2'].keys():
			shutil.copyfile(p_dictSimu['macroEl2'].get('Emat1'), os.path.join(fullDir, 'E_mat1_2.csv'))
		
		# E pad 2 (nominal macroel, macro2)
		shutil.copyfile(p_dictSimu.get('Emat2'), os.path.join(fullDir, 'E_mat2.csv'))
		if bool_macroEl2_Ph1 and 'Emat2' in p_dictSimu['macroEl2'].keys():
			shutil.copyfile(p_dictSimu['macroEl2'].get('Emat2'), os.path.join(fullDir, 'E_mat2_2.csv'))

		# E ballast (nominal macroel, macro2)
		shutil.copyfile(p_dictSimu.get('Ebal'), os.path.join(fullDir, 'E_bal.csv'))
		if bool_macroEl2_Ph1 and 'Ebal' in p_dictSimu['macroEl2'].keys():
			shutil.copyfile(p_dictSimu['macroEl2'].get('Ebal'), os.path.join(fullDir, 'Ebal_2.csv'))
		
		# E USP (nominal macroel, macro2, macro3)
		if p_dictSimu.get('USP_on') == True:
			shutil.copyfile(p_dictSimu.get('EUSP'), os.path.join(fullDir, 'E_USP.csv'))
			if bool_macroEl2_Ph1 and 'EUSP' in p_dictSimu['macroEl2'].keys():
				shutil.copyfile(p_dictSimu['macroEl2'].get('EUSP'), os.path.join(fullDir, 'E_USP_2.csv'))
	except:
		return "Modes simulation: some materials properties files could not be copied to " + fullDir + "."
	
	# Copy mesh files
	try:
		shutil.copyfile(p_dictSimu.get('railMesh'), os.path.join(fullDir, 'rail.med'))
		shutil.copyfile(p_dictSimu.get('padMesh'), os.path.join(fullDir, 'padR.med'))
		shutil.copyfile(p_dictSimu.get('sleeperMesh'), os.path.join(fullDir, 'sleeper.med'))
		shutil.copyfile(os.path.join(p_dictSimu['cwd'], 'Meshes', 'Clamps', 'Clamp.med'), os.path.join(fullDir, 'Clamp.med'))
		if p_dictSimu.get('USP_on') == True:
			shutil.copyfile(p_dictSimu.get('USPMesh'), os.path.join(fullDir, 'USP.med'))
	except:
		return "Modes simulation: some mesh files could not be copied to " + fullDir + "."

	# Export & comm files copy
	try:
		asterFilesPath = os.path.join(p_dictSimu['cwd'], 'DevFiles', 'AsterFiles')
		exportFileName = 'computeModes1.export'
		shutil.copyfile(os.path.join(asterFilesPath, exportFileName), os.path.join(fullDir, exportFileName))
		shutil.copyfile(os.path.join(asterFilesPath, 'computeModes.comm'), os.path.join(fullDir, 'computeModes.comm'))
	except:
		return "Modes simulation: export or comm files could not be copied to " + fullDir + "."
	
	# Export file string replacements	
	exportFiles = os.path.join(fullDir, 'computeModes1.export')	
	
	nCPUs = p_dictSimu.get('phase1CPUs')
	if p_createMeshOnly:
		nCPUs = 1
	memlim = p_dictSimu.get('memLimit')
	reptravroot = p_dictSimu.get('reptrav')
	server = p_dictSimu.get('host')
	
	try:
		os.system('sed -i -E "s!__memjob__!' + str(memlim*1024) + '!" ' + exportFiles)
		os.system('sed -i -E "s!__memlim__!' + str(memlim) + '!" ' + exportFiles)
		os.system('sed -i -E "s!__memjeveux__!' + str(memlim/4) + '!" ' + exportFiles)
		os.system('sed -i -E "s!__ncpus__!' + str(nCPUs) + '!" ' + exportFiles)
		reptrav = os.path.join(reptravroot, 'cae-caesrv1-interactif_0101')
		file = os.path.join(fullDir, 'computeModes1.export')
		os.system('sed -i -E "s!__reptrav__!' + reptrav + '!" ' + file)
		os.system('sed -i -E "s!__server__!' + server + '!" ' + exportFiles)
		os.system('sed -i -E "s!__messagesDir__!' + os.path.join(p_dictSimu['cwd'], 'DevFiles', 'Messages') + '!" ' + exportFiles)

		# E pad 1 files for macroEl 2
		if bool_macroEl2_Ph1 and 'Emat1' in p_dictSimu['macroEl2'].keys():
			os.system('sed -i -E "s!__Emat1_2__!F libr E_mat1_2.csv D  50!" ' + exportFiles)
		else:
			os.system('sed -i -E "s!__Emat1_2__!!" ' + exportFiles)

		# E pad 2 files for macroEl 2
		if bool_macroEl2_Ph1 and 'Emat2' in p_dictSimu['macroEl2'].keys():
			os.system('sed -i -E "s!__Emat2_2__!F libr E_mat2_2.csv D  52!" ' + exportFiles)
		else:
			os.system('sed -i -E "s!__Emat2_2__!!" ' + exportFiles)

		# E ballast files for macroEl 2 + 3
		if bool_macroEl2_Ph1 and 'Ebal' in p_dictSimu['macroEl2'].keys():
			os.system('sed -i -E "s!__Ebal_2__!F libr Ebal_2.csv D  62!" ' + exportFiles)
		else:
			os.system('sed -i -E "s!__Ebal_2__!!" ' + exportFiles)

		if p_dictSimu['USP_on'] == True:
			os.system('sed -i -E "s!__meshUSP__!F libr USP.med D  26!" ' + exportFiles)

			# E USP files for macroEl 1 + 2 + 3
			os.system('sed -i -E "s!__EUSP__!F libr E_USP.csv D  34!" ' + exportFiles)
			if bool_macroEl2_Ph1 and 'EUSP' in p_dictSimu['macroEl2'].keys():
				os.system('sed -i -E "s!__EUSP_2__!F libr E_USP_2.csv D  58!" ' + exportFiles)
			else:
				os.system('sed -i -E "s!__EUSP_2__!!" ' + exportFiles)
		else:
			os.system('sed -i -E "s!__meshUSP__!!" ' + exportFiles)
			os.system('sed -i -E "s!__EUSP__!!" ' + exportFiles)
	except:
		if p_createMeshOnly:
			return "Mesh creation: string replacements (sed) in export files did not run properly."
		else:
			return "Modes simulation: string replacements (sed) in export files did not run properly."
		
	return 0
		


def PrepareFilesPhase2(p_dictSimu):
	# Create empty simulation folder
	fullDir = os.path.join(p_dictSimu.get('simuParentFolder'), p_dictSimu.get('name'))
	fullDirInput = os.path.join(fullDir, 'Inputs')
	fullDirOutput = os.path.join(fullDir, 'Outputs')

	# Phase 1: if different mat props but same mesh (no sleeper shift), and computeModeShapesPh1 False, no need to compute new macroelement mode shapes.
	# True if either: a separate macroEl is requested for macroEl2, or a sleeper shift is set (!=0)
	bool_macroEl2_Ph1 = ('macroEl2' in p_dictSimu.keys()) and ((("computeModeShapesPh1" in p_dictSimu['macroEl2'].keys()) and (p_dictSimu['macroEl2']['computeModeShapesPh1'] is True)) or (("slpShift" in p_dictSimu['macroEl2'].keys()) and (p_dictSimu['macroEl2']['slpShift'] !=0)))

	# With a sleeper shift, the macroelement is not symmetric anymore ; so: need to create another one with -slpShift to make the left side of the track
	bool_macroEl2_slpShift = bool_macroEl2_Ph1 and "slpShift" in p_dictSimu['macroEl2'].keys() and p_dictSimu['macroEl2']['slpShift'] !=0

	# Phase 2: even if mode shapes not computed in Ph1 for macroEl2 or 3, macroEl 2/3 are computed based on nominal mode shapes
	bool_macroEl2_Ph2 = 'macroEl2' in p_dictSimu.keys()

	
	try:
		shutil.rmtree(fullDir)
	except:
		pass
		
	try:
		os.makedirs(fullDir)
	except:
		return "Harmonic simulation: the folder " + fullDir + " could not be created."
	
	os.makedirs(fullDirInput)
	os.makedirs(fullDirOutput)		
		
	# Copy base files
	modesFolder = p_dictSimu.get('modesFolder')
			
	try:
		shutil.copyfile(os.path.join(modesFolder, 'info_modes.txt'), os.path.join(fullDirInput, 'info_modes.txt'))
		if bool_macroEl2_Ph1:
			shutil.copyfile(os.path.join(modesFolder, 'info_modes2.txt'), os.path.join(fullDirInput, 'info_modes2.txt'))

		shutil.copytree(os.path.join(modesFolder, 'base_modes'), os.path.join(fullDirInput, 'base_modes'))
	except:
		return "Problem while copying files from phase 1."
	
	#
	try:
		txt = json.dumps(p_dictSimu, indent = 4, sort_keys=True)
		jsonPath = os.path.join(fullDir, 'parameters.json')
		with open(jsonPath, 'w') as f:
			f.write(txt)
		f.close()
	except:
		return jsonPath + ' could not be created (harmonic simulation).'
	
	# Copy materials properties files
	try:
		# E pad 1
		shutil.copyfile(p_dictSimu.get('Emat1'), os.path.join(fullDirInput, 'E_mat1.csv'))
		if bool_macroEl2_Ph2 and 'Emat1' in p_dictSimu['macroEl2'].keys():
			shutil.copyfile(p_dictSimu['macroEl2'].get('Emat1'), os.path.join(fullDirInput, 'E_mat1_2.csv'))

		# tanD pad 1
		shutil.copyfile(p_dictSimu.get('tanDmat1'), os.path.join(fullDirInput, 'tanD_mat1.csv'))
		if bool_macroEl2_Ph2 and 'tanDmat1' in p_dictSimu['macroEl2'].keys():
			shutil.copyfile(p_dictSimu['macroEl2'].get('tanDmat1'), os.path.join(fullDirInput, 'tanD_mat1_2.csv'))

		# E pad 2
		shutil.copyfile(p_dictSimu.get('Emat2'), os.path.join(fullDirInput, 'E_mat2.csv'))
		if bool_macroEl2_Ph2 and 'Emat2' in p_dictSimu['macroEl2'].keys():
			shutil.copyfile(p_dictSimu['macroEl2'].get('Emat2'), os.path.join(fullDirInput, 'E_mat2_2.csv'))

		# tanD pad 2
		shutil.copyfile(p_dictSimu.get('tanDmat2'), os.path.join(fullDirInput, 'tanD_mat2.csv'))
		if bool_macroEl2_Ph2 and 'tanDmat2' in p_dictSimu['macroEl2'].keys():
			shutil.copyfile(p_dictSimu['macroEl2'].get('tanDmat2'), os.path.join(fullDirInput, 'tanD_mat2_2.csv'))

		# E ballast
		shutil.copyfile(p_dictSimu.get('Ebal'), os.path.join(fullDirInput, 'E_bal.csv'))
		if bool_macroEl2_Ph2 and 'Ebal' in p_dictSimu['macroEl2'].keys():
			shutil.copyfile(p_dictSimu['macroEl2'].get('Ebal'), os.path.join(fullDirInput, 'Ebal_2.csv'))

		# tanD ballast
		shutil.copyfile(p_dictSimu.get('tanDbal'), os.path.join(fullDirInput, 'tanD_bal.csv'))
		if bool_macroEl2_Ph2 and 'tanDbal' in p_dictSimu['macroEl2'].keys():
			shutil.copyfile(p_dictSimu['macroEl2'].get('tanDbal'), os.path.join(fullDirInput, 'tanDbal_2.csv'))
		
		if p_dictSimu.get('USP_on') == True:
			# E USP
			shutil.copyfile(p_dictSimu.get('EUSP'), os.path.join(fullDirInput, 'E_USP.csv'))
			if bool_macroEl2_Ph2 and 'EUSP' in p_dictSimu['macroEl2'].keys():
				shutil.copyfile(p_dictSimu['macroEl2'].get('EUSP'), os.path.join(fullDirInput, 'E_USP_2.csv'))

			# tanD USP
			shutil.copyfile(p_dictSimu.get('tanDUSP'), os.path.join(fullDirInput, 'tanD_USP.csv'))
			if bool_macroEl2_Ph2 and 'tanDUSP' in p_dictSimu['macroEl2'].keys():
				shutil.copyfile(p_dictSimu['macroEl2'].get('tanDUSP'), os.path.join(fullDirInput, 'tanD_USP_2.csv'))
	except:
		return "Harmonic simulation: some materials properties files could not be copied to " + fullDirInput + "."
	
	# Copy mesh files
	try:
		shutil.copyfile(p_dictSimu.get('railMesh'), os.path.join(fullDirInput, 'rail.med'))
		shutil.copyfile(p_dictSimu.get('padMesh'), os.path.join(fullDirInput, 'padR.med'))
		shutil.copyfile(p_dictSimu.get('sleeperMesh'), os.path.join(fullDirInput, 'sleeper.med'))
		shutil.copyfile(os.path.join(p_dictSimu['cwd'], 'Meshes', 'Clamps', 'Clamp.med'), os.path.join(fullDirInput, 'Clamp.med'))
		if p_dictSimu.get('USP_on') == True:
			shutil.copyfile(p_dictSimu.get('USPMesh'), os.path.join(fullDirInput, 'USP.med'))
		
		if p_dictSimu.get('computeAcoustic') == True:
			shutil.copyfile(p_dictSimu.get('acousticMesh'), os.path.join(fullDirInput, 'acousticMesh.med'))
		
	except:
		return "Harmonic simulation: some mesh files could not be copied to " + fullDirInput + "."

	# Frequency files & bands management
	code = PrepareFreqFiles(p_dictSimu)
	if code != 0:
		return code

	# Export & comm files copy
	try:
		nJobs = p_dictSimu.get('nJobs')
		asterFilesPath = os.path.join(p_dictSimu['cwd'], 'DevFiles', 'AsterFiles')
		for i in range(nJobs):
			exportFileName = 'runSimulation_b' + str(i+1) + '.export'
			shutil.copyfile(os.path.join(asterFilesPath, exportFileName), os.path.join(fullDir, exportFileName))
		
		shutil.copyfile(os.path.join(asterFilesPath, 'runSimulation.comm'), os.path.join(fullDir, 'runSimulation.comm'))
	except:
		return "Harmonic simulation: export or comm files could not be copied to " + fullDir + "."
	
	# Export files string replacements	
	exportFiles = os.path.join(fullDir, 'runSimulation_b*.export')	
	
	nCPUs = p_dictSimu.get('nCPUs')
	memlim = p_dictSimu.get('memLimit')
	reptravroot = p_dictSimu.get('reptrav')
	server = p_dictSimu.get('host')
	
	try:
		os.system('sed -i -E "s!__memjob__!' + str(memlim*1024) + '!" ' + exportFiles)
		os.system('sed -i -E "s!__memlim__!' + str(memlim) + '!" ' + exportFiles)
		os.system('sed -i -E "s!__memjeveux__!' + str(memlim/4) + '!" ' + exportFiles)
		os.system('sed -i -E "s!__ncpus__!' + str(nCPUs) + '!" ' + exportFiles)
		os.system('sed -i -E "s!__server__!' + server + '!" ' + exportFiles)
		os.system('sed -i -E "s!__messagesDir__!' + os.path.join(p_dictSimu['cwd'], 'DevFiles', 'Messages') + '!" ' + exportFiles)

		# info modes for macroEl 2
		if bool_macroEl2_Ph1:
			os.system('sed -i -E "s!__infoModes2__!F libr Inputs/info_modes2.txt D  8!" ' + exportFiles)
		else:
			os.system('sed -i -E "s!__infoModes2__!!" ' + exportFiles)

		# E pad 1 files for macroEl 2
		if bool_macroEl2_Ph2 and 'Emat1' in p_dictSimu['macroEl2'].keys():
			os.system('sed -i -E "s!__Emat1_2__!F libr Inputs/E_mat1_2.csv D  50!" ' + exportFiles)
		else:
			os.system('sed -i -E "s!__Emat1_2__!!" ' + exportFiles)

		# tanD pad 1 files for macroEl 2
		if bool_macroEl2_Ph2 and 'tanDmat1' in p_dictSimu['macroEl2'].keys():
			os.system('sed -i -E "s!__tanDmat1_2__!F libr Inputs/tanD_mat1_2.csv D  54!" ' + exportFiles)
		else:
			os.system('sed -i -E "s!__tanDmat1_2__!!" ' + exportFiles)

		# E pad 2 files for macroEl 2
		if bool_macroEl2_Ph2 and 'Emat2' in p_dictSimu['macroEl2'].keys():
			os.system('sed -i -E "s!__Emat2_2__!F libr Inputs/E_mat2_2.csv D  52!" ' + exportFiles)
		else:
			os.system('sed -i -E "s!__Emat2_2__!!" ' + exportFiles)

		# tanD pad 2 files for macroEl 2
		if bool_macroEl2_Ph2 and 'tanDmat2' in p_dictSimu['macroEl2'].keys():
			os.system('sed -i -E "s!__tanDmat2_2__!F libr Inputs/tanD_mat2_2.csv D  56!" ' + exportFiles)
		else:
			os.system('sed -i -E "s!__tanDmat2_2__!!" ' + exportFiles)

		# E ballast files for macroEl 2
		if bool_macroEl2_Ph2 and 'Ebal' in p_dictSimu['macroEl2'].keys():
			os.system('sed -i -E "s!__Ebal_2__!F libr Inputs/Ebal_2.csv D  62!" ' + exportFiles)
		else:
			os.system('sed -i -E "s!__Ebal_2__!!" ' + exportFiles)

		# tanD ballast files for macroEl 2
		if bool_macroEl2_Ph2 and 'tanDbal' in p_dictSimu['macroEl2'].keys():
			os.system('sed -i -E "s!__tanDbal_2__!F libr Inputs/tanDbal_2.csv D  64!" ' + exportFiles)
		else:
			os.system('sed -i -E "s!__tanDbal_2__!!" ' + exportFiles)

		if p_dictSimu['USP_on'] == True:
			os.system('sed -i -E "s!__meshUSP__!F libr Inputs/USP.med D  26!" ' + exportFiles)
			# E USP files for macroEl 1 + 2 + 3
			os.system('sed -i -E "s!__EUSP__!F libr Inputs/E_USP.csv D  34!" ' + exportFiles)
			if bool_macroEl2_Ph2 and 'EUSP' in p_dictSimu['macroEl2'].keys():
				os.system('sed -i -E "s!__EUSP_2__!F libr Inputs/E_USP_2.csv D  58!" ' + exportFiles)
			else:
				os.system('sed -i -E "s!__EUSP_2__!!" ' + exportFiles)

			# tanD USP files for macroEl 1 + 2 + 3
			os.system('sed -i -E "s!__tanDUSP__!F libr Inputs/tanD_USP.csv D  35!" ' + exportFiles)
			if bool_macroEl2_Ph2 and 'tanDUSP' in p_dictSimu['macroEl2'].keys():
				os.system('sed -i -E "s!__tanDUSP_2__!F libr Inputs/tanD_USP_2.csv D  60!" ' + exportFiles)
			else:
				os.system('sed -i -E "s!__tanDUSP_2__!!" ' + exportFiles)

		else:
			os.system('sed -i -E "s!__meshUSP__!!" ' + exportFiles)
			os.system('sed -i -E "s!__EUSP__!!" ' + exportFiles)
			os.system('sed -i -E "s!__tanDUSP__!!" ' + exportFiles)
	
		if p_dictSimu.get('computeAcoustic') == True:
			txt = 'F mmed Inputs' + os.sep + 'acousticMesh.med D  19'
		else:
			txt = ''
		os.system('sed -i -E "s!__acousticMesh__!' + txt + '!" ' + exportFiles)

		for i in range(nJobs):
			reptrav = os.path.join(reptravroot, 'cae-caesrv1-interactif_0102' + str(i+1))
			file = os.path.join(fullDir, 'runSimulation_b' + str(i+1) + '.export')	
			os.system('sed -i -E "s!__reptrav__!' + reptrav + '!" ' + file)
			
	except:
		return "Harmonic simulation: string replacements (sed) in export & comm files did not run properly."
		
	return 0





# Divide arbitrary frequency list into N jobs with lengths as close as possible
def PrepareFreqFiles(p_dictSimu):
	freqs = p_dictSimu['frequencies']
	nJobs = p_dictSimu['nJobs']
	fullDir = os.path.join(p_dictSimu.get('simuParentFolder'), p_dictSimu.get('name'), 'Inputs')
	
	nFreqs = len(freqs)
	freqs = sorted(freqs)
	
	if nFreqs<nJobs or nJobs<1:
		return "Error; more jobs than frequencies (Harmonic simulation)."
	
	# initialize array showing how many frequencies will be in each band
	bands = []*nJobs
	for i in range(nJobs):
		bands.append([])
	
	# initialize frequency bands for later
	freqBands = bands
	
	# fill array with 0 just to know the number of elements per band
	for i in range(len(freqs)):
		jobNo = i % nJobs
		bands[jobNo] += [0]
	
	# fill frequency bands array with actual frequencies
	j = 0
	for i in range(len(bands)):
		band = bands[i]
		freqBands[i] = freqs[j:j+len(band)]
		j += len(band)
		
	for i in range(len(freqBands)):
		bandStr = []
		for item in freqBands[i]:
			bandStr.append(str(item))
	
		file = os.path.join(fullDir, 'f' + str(i+1) + '.txt')
		txt = '\n'.join(bandStr)
		with open(file, 'w') as f:
			f.write(txt)
		f.close()
		
	return 0
		
		
	

	
	
def RunMultiJobs(p_workingDir, p_simFolder, p_job, p_nJobs, p_messageFile, p_debugMode):
	# p_job is the name of the export file (without its number and ".export")
	
	runScript = os.path.join(p_workingDir, 'DevFiles', 'App', 'runAsterJobs.sh')
	code = os.system('bash ' + runScript + ' ' + p_job + ' ' + p_simFolder + ' ' + str(p_nJobs) + ' ' + p_messageFile + ' ' + str(p_debugMode))
	time.sleep(1)
	return code

def SaveBaseFiles(p_dictSimu, p_saveBaseDir, p_simFolder):
	# True if either: a separate macroEl is requested for macroEl2, or a sleeper shift is set (!=0)
	bool_macroEl2_Ph1 = ('macroEl2' in p_dictSimu.keys()) and ((("computeModeShapesPh1" in p_dictSimu['macroEl2'].keys()) and (p_dictSimu['macroEl2']['computeModeShapesPh1'] is True)) or (("slpShift" in p_dictSimu['macroEl2'].keys()) and (p_dictSimu['macroEl2']['slpShift'] !=0)))
	# With a sleeper shift, the macroelement is not symmetric anymore ; so: need to create another one with -slpShift to make the left side of the track
	bool_macroEl2_slpShift = bool_macroEl2_Ph1 and "slpShift" in p_dictSimu['macroEl2'].keys() and p_dictSimu['macroEl2']['slpShift'] !=0

	try:
		shutil.rmtree(p_saveBaseDir)
	except:
		pass
		
	try:
		os.makedirs(p_saveBaseDir)
	except:
		return "The folder " + p_saveBaseDir + " could not be created."
	

	dir1 = os.path.join(p_simFolder, 'base_modes')
	dir2 = os.path.join(p_saveBaseDir, 'base_modes')

	if os.path.exists(dir2):
		shutil.rmtree(dir2)
	
	try:
		shutil.copytree(dir1, dir2)
	except:
		return "Impossible to copy base_modes from " + p_simFolder + " to " + p_saveBaseDir + "."
	
	try:
		shutil.copyfile(os.path.join(p_simFolder, 'info_modes.txt'), os.path.join(p_saveBaseDir, 'info_modes.txt'))
	except:
		return "Impossible to copy " + os.path.join(p_simFolder, 'info_modes.txt') + " to " + os.path.join(p_saveBaseDir, 'info_modes.txt') + "."
	
	if bool_macroEl2_Ph1:
		try:
			shutil.copyfile(os.path.join(p_simFolder, 'info_modes2.txt'), os.path.join(p_saveBaseDir, 'info_modes2.txt'))
		except:
			return "Impossible to copy " + os.path.join(p_simFolder, 'info_modes2.txt') + " to " + os.path.join(p_saveBaseDir, 'info_modes2.txt') + "."
		
	try:
		shutil.copyfile(os.path.join(p_simFolder, 'mesh.med'), os.path.join(p_saveBaseDir, 'mesh.med'))
	except:
		return "Impossible to copy " + os.path.join(p_simFolder, 'mesh.med') + " to " + os.path.join(p_saveBaseDir, 'mesh.med') + "."
	
	try:
		shutil.copyfile(os.path.join(p_simFolder, 'parameters.json'), os.path.join(p_saveBaseDir, 'parameters.json'))
	except:
		return "Impossible to copy " + os.path.join(p_simFolder, 'parameters.json') + " to " + os.path.join(p_saveBaseDir, 'parameters.json') + "."
	
		
	return 0
	
def PostProcessResults(p_dictSimu):

	fullDir = os.path.join(p_dictSimu.get('simuParentFolder'), p_dictSimu.get('name'))
	fullDirOutput = os.path.join(fullDir, 'Outputs')
	cwd = p_dictSimu['cwd']
	nJobs = p_dictSimu['nJobs']
	
	# Concatenate txt result files
	code = ConcatTxtFiles(fullDirOutput, nJobs, 'FRF', 1)
	if code != 0:
		return code
	 
	if p_dictSimu['computeAcoustic'] == True:
		if p_dictSimu['acMeshDim'] == '1D':
			code = ConcatTxtFiles(fullDirOutput, nJobs, 'acousticResults', 1)
			if code != 0:
				return code
			
		elif p_dictSimu['acMeshDim'] == '2D':
			code = ConcatTxtFiles(fullDirOutput, nJobs, 'acousticResults', 2)
			if code != 0:
				return code
	
	if p_dictSimu['writeMED'] == True:
		# Concatenate MED files
		if os.path.exists(os.path.join(fullDirOutput, 'resuHarm_b1.med')) == False:
			return "Harmonic simulation: " + os.path.join(fullDirOutput, 'resuHarm_b1.med') + " does not exist."
		
		# Copy .comm & .export files to simu folder
		try:
			shutil.copyfile(os.path.join(cwd, 'DevFiles', 'AsterFiles', 'postPro_concatMedFiles.comm'), os.path.join(fullDir, 'postPro_concatMedFiles.comm'))
			
			postProExportFile = os.path.join(fullDir, 'postPro_concatMedFiles1.export')
			shutil.copyfile(os.path.join(cwd, 'DevFiles', 'AsterFiles', 'postPro_concatMedFiles1.export'), postProExportFile)
		except:
			return "Harmonic simulation: error copying post-processing export and comm files."
		
		
		# Export & comm files string replacements			
		try:
			nCPUs = p_dictSimu.get('nCPUs')*p_dictSimu.get('nJobs')
			memlim = p_dictSimu.get('memLimit')
			reptravroot = p_dictSimu.get('reptrav')
			server = p_dictSimu.get('host')
			
			os.system('sed -i -E "s!__memjob__!' + str(memlim*1024) + '!" ' + postProExportFile)
			os.system('sed -i -E "s!__memlim__!' + str(memlim) + '!" ' + postProExportFile)
			os.system('sed -i -E "s!__memjeveux__!' + str(memlim/4) + '!" ' + postProExportFile)
			os.system('sed -i -E "s!__ncpus__!' + str(nCPUs) + '!" ' + postProExportFile)
			os.system('sed -i -E "s!__server__!' + server + '!" ' + postProExportFile)
			os.system('sed -i -E "s!__messagesDir__!' + os.path.join(p_dictSimu['cwd'], 'DevFiles', 'Messages') + '!" ' + postProExportFile)
			
			reptrav = os.path.join(reptravroot, 'cae-caesrv1-interactif_0103')
			file = os.path.join(fullDir, 'postPro_concatMedFiles1.export')	
			os.system('sed -i -E "s!__reptrav__!' + reptrav + '!" ' + file)
			
			if p_dictSimu.get('computeAcoustic') == True:
				txt = 'F libr Inputs' + os.sep + 'acousticMesh.med D  7'
			else:
				txt = ''
			os.system('sed -i -E "s!__acousticMesh__!' + txt + '!" ' + postProExportFile)
		except:
			return "String replacements (sed) in post-processing export & comm files did not run properly."
		
		
		
		with open(postProExportFile) as f:
			fileContent = f.read()
		f.close()
		
		for i in range(nJobs):
			fileContent += '\nF mmed Outputs/resuHarm_b' + str(i+1) + '.med D  ' + str(10 + i)
			if p_dictSimu['computeAcoustic'] == True:
				fileContent += '\nF mmed Outputs/resuAcou_b' + str(i+1) + '.med D  ' + str(40 + i)
			fileContent += '\nF libr Inputs/f' + str(i+1) + '.txt D  ' + str(70 + i)
			
		with open(postProExportFile, 'w') as f:
			f.write(fileContent)
		f.close()

		messageFile = os.path.join(cwd, 'DevFiles', 'Messages', 'message_concatMedFiles.mess')
		debugMode = p_dictSimu['debugPh2']

		code = RunMultiJobs(cwd, fullDir, 'postPro_concatMedFiles', 1, messageFile, debugMode)

		try:
			shutil.copyfile(messageFile, os.path.join(fullDirOutput, 'message_concatMedFiles.mess'))
		except:
			return "Could not copy message_concatMedFiles.mess to Phase 2 outputs directory."

		if code == 0:
			for i in range(nJobs):
				try:
					os.remove(os.path.join(fullDirOutput, 'resuHarm_b' + str(i+1) + '.med'))
					if p_dictSimu['computeAcoustic'] == True:
						os.remove(os.path.join(fullDirOutput, 'resuAcou_b' + str(i+1) + '.med'))
				except:
					pass

	# Compute Lw & include it in acousticResults.txt if mesh is 2D
	if p_dictSimu['computeAcoustic'] == True and p_dictSimu['acMeshDim'] == '2D':
	
		file = os.path.join(fullDirOutput, 'acousticResults.txt')
		if os.path.exists(file) == False:
			return "Post-processing: " + file + " does not exist."
		
		with open(file) as f:
			fileContent = f.read()
			lines = fileContent.splitlines()
		f.close()
		
		if len(lines) == 0:
			return "Post-processing: " + file + " is empty."
		
		if lines[0][0:2] == 'Lw':
			return 0

		freqs = []
		acPower = []
		for line in lines:
			try: freq = float(line.split('\t')[0])
			except: continue
			try: power = float(line.split('\t')[1])
			except: continue
			freqs.append(freq)
			acPower.append(power)

		if len(acPower)>=2:
			Lw = 0
			for i in range(len(acPower)-1):
				Lw += (acPower[i] + acPower[i+1])/2*(freqs[i+1] - freqs[i])
			Lw = 10*math.log10(Lw)
		else:
			Lw = 'NaN'

		try:
			fileContent = 'Lw [dB]\t' + str(Lw) + '\n\n' + fileContent
			f = open(file, 'w')
			f.write(fileContent)
			f.close()
		except:
			return "Post-processing: error completing " + file + "."
			
	return code
	
	
	
def ConcatTxtFiles(p_simFolder, p_nJobs, p_fileType, p_dataLineStart):
	newFileContentList = []
	for i in range(p_nJobs):
		file = os.path.join(p_simFolder, p_fileType + '_b' + str(i+1) + '.txt')
		
		if os.path.exists(file) == False:
			return "Harmonic simulation: " + file + " not found."
		
		with open(file) as f:
			fileContent = f.read().splitlines()
		f.close()
		
		if len(fileContent) == 0:
			return "Harmonic simulation: " + file + " is empty."
		
		for j in range(len(fileContent)):
			line = fileContent[j]
			if i>0 and j<p_dataLineStart:
				continue
			newFileContentList.append(line)
		
		try:
			os.remove(file)
		except:
			pass
		
	newFileContent = '\n'.join(newFileContentList)
	
	try:
		newFile = os.path.join(p_simFolder, p_fileType + '.txt')
		with open(newFile, 'w') as f:
			f.write(newFileContent)
		f.close()
	except:
		return "Harmonic simulation: error writing " + newFile + "."
		
	return 0
		
def DeletePycFiles(p_workingDir):
	files = os.listdir(p_workingDir)
	
	if not files:
		return 0
	
	for file in files:
		fullPath = os.path.join(p_workingDir, file)
		
		if os.path.isdir(fullPath) == True:
			continue
			
		extension = os.path.splitext(file)[1]
		if extension == '.pyc':
			try:
				os.remove(fullPath)
			except:
				pass
				
	return 0
			
if __name__ == '__main__':
	pass