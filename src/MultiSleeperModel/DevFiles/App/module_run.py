# import imp
import os
import shutil
import time
import pickle
import math
#import sys
import json
#import numpy as np

def RunSimulation(p_dictSimu):

	if p_dictSimu.get('runPhase1') == True:
		code = RunPhase1(p_dictSimu)
		if code != 0:
			return code
	
	
	code = RunPhase2(p_dictSimu)
	if code != 0:
		return code
		
	return 0
		

		
		
		
def RunPhase1(p_dictSimu):
	code = PrepareFilesPhase1(p_dictSimu)
	if code != 0:
		return code
	
	cwd = p_dictSimu['cwd']
	simFolder = p_dictSimu['phase1WorkingDir']
	nJobs = p_dictSimu['nJobsPh1']
	saveBaseFile = os.path.join(p_dictSimu['savePhase1To'], p_dictSimu['phase1Name'])
	messageFile = os.path.join(cwd, 'DevFiles', 'Messages', 'message_phase1_b1.mess')
	debugMode = p_dictSimu['debugPh1']
	
	code = RunMultiJobs(cwd, simFolder, 'phase1_computeModesMag_b', nJobs, messageFile, debugMode)
	if code != 0:
		return code
		
	code = SaveBaseFiles(saveBaseFile, simFolder, nJobs)
	if code != 0:
		return code
		
	code = DeletePycFiles(p_dictSimu['appPath'])
	if code != 0:
		return code
	
	return 0
	
def RunPhase2(p_dictSimu):
	code = PrepareFilesPhase2(p_dictSimu)
	if code != 0:
		return code
	
	cwd = p_dictSimu['cwd']
	simFolder = os.path.join(p_dictSimu.get('simuDir'), p_dictSimu.get('name'))
	nJobs = p_dictSimu['nJobs']
	messageFile = os.path.join(cwd, 'DevFiles', 'Messages', 'message_phase2_b1.mess')
	debugMode = p_dictSimu['debugPh2']
		
	code = RunMultiJobs(cwd, simFolder, 'phase2_runSimulation_b', nJobs, messageFile, debugMode)
	if code != 0:
		return code
	
	code = PostProcessResults(p_dictSimu)
	if code != 0:
		return code
	
	code = DeletePycFiles(cwd)
	if code != 0:
		return code
	
	return 0
		
def PrepareFilesPhase1(p_dictSimu):
	# Create empty simulation folder
	fullDir = p_dictSimu.get('phase1WorkingDir')
	
	try:
		shutil.rmtree(fullDir)
	except:
		pass
		
	try:
		os.makedirs(fullDir)
	except:
		return "The folder " + fullDir + " could not be created (Phase 1)."
	
	#
	try:
		txt = json.dumps(p_dictSimu, indent = 4, sort_keys=True)
		jsonPath = os.path.join(fullDir, 'parameters.json')
		with open(jsonPath, 'w') as f:
			f.write(txt)
		f.close()
	except:
		return jsonPath + ' could not be created (Phase 1).'
	
	# Copy materials properties files
	try:
		shutil.copyfile(p_dictSimu.get('Emat1'), os.path.join(fullDir, 'E_mat1.csv'))
		shutil.copyfile(p_dictSimu.get('tanDmat1'), os.path.join(fullDir, 'tanD_mat1.csv'))
		shutil.copyfile(p_dictSimu.get('Emat2'), os.path.join(fullDir, 'E_mat2.csv'))
		shutil.copyfile(p_dictSimu.get('tanDmat2'), os.path.join(fullDir, 'tanD_mat2.csv'))
		shutil.copyfile(p_dictSimu.get('Ebal'), os.path.join(fullDir, 'E_bal.csv'))
		shutil.copyfile(p_dictSimu.get('tanDbal'), os.path.join(fullDir, 'tanD_bal.csv'))
		
		if p_dictSimu.get('USPON') == True:
			shutil.copyfile(p_dictSimu.get('EUSP'), os.path.join(fullDir, 'E_USP.csv'))
			shutil.copyfile(p_dictSimu.get('tanDUSP'), os.path.join(fullDir, 'tanD_USP.csv'))
	except:
		return "Phase 1: some materials properties files could not be copied to " + fullDir + "."
	
	# Copy mesh files
	try:
		meshesDir = os.path.join(p_dictSimu['cwd'], 'Meshes')
		shutil.copyfile(os.path.join(meshesDir, 'sleeper.med'), os.path.join(fullDir, 'sleeper.med'))
		shutil.copyfile(os.path.join(meshesDir, 'rail.med'), os.path.join(fullDir, 'rail.med'))
		if p_dictSimu.get('USPON') == True:
			shutil.copyfile(os.path.join(meshesDir, 'USP.med'), os.path.join(fullDir, 'USP.med'))
		
		shutil.copyfile(p_dictSimu.get('padMesh'), os.path.join(fullDir, 'padR.med'))
	except:
		return "Phase 1: some mesh files could not be copied to " + fullDir + "."

	# Frequency files & bands management
	code = PrepareFreqFiles(p_dictSimu, 1)
	if code != 0:
		return code

	# Export & comm files copy
	try:
		nJobs = p_dictSimu.get('nJobsPh1')
		asterFilesPath = os.path.join(p_dictSimu['cwd'], 'DevFiles', 'AsterFiles')
		for i in range(nJobs):
			exportFileName = 'phase1_computeModesMag_b' + str(i+1) + '.export'
			shutil.copyfile(os.path.join(asterFilesPath, exportFileName), os.path.join(fullDir, exportFileName))
		
		shutil.copyfile(os.path.join(asterFilesPath, 'phase1_computeModesMag.comm'), os.path.join(fullDir, 'phase1_computeModesMag.comm'))
	except:
		return "Phase 1: export or comm files could not be copied to " + fullDir + "."
	
	# Export & comm files string replacements	
	exportFiles = os.path.join(fullDir, 'phase1_computeModesMag_b*.export')	
	
	nCPUs = p_dictSimu.get('phase1CPUs')
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
		if p_dictSimu['USPON'] == True:
			os.system('sed -i -E "s!__meshUSP__!F libr USP.med D  26!" ' + exportFiles)
			os.system('sed -i -E "s!__EUSP__!F libr E_USP.csv D  34!" ' + exportFiles)
			os.system('sed -i -E "s!__tanDUSP__!F libr tanD_USP.csv D  35!" ' + exportFiles)
		else:
			os.system('sed -i -E "s!__meshUSP__!!" ' + exportFiles)
			os.system('sed -i -E "s!__EUSP__!!" ' + exportFiles)
			os.system('sed -i -E "s!__tanDUSP__!!" ' + exportFiles)
		
		for i in range(nJobs):
			reptrav = os.path.join(reptravroot, 'cae-caesrv1-interactif_10000' + str(i+1))
			file = os.path.join(fullDir, 'phase1_computeModesMag_b' + str(i+1) + '.export')	
			os.system('sed -i -E "s!__reptrav__!' + reptrav + '!" ' + file)
	except:
		return "Phase 1: string replacements (sed) in export & comm files did not run properly."
		
	return 0
		


def PrepareFilesPhase2(p_dictSimu):
	# Create empty simulation folder
	fullDir = os.path.join(p_dictSimu.get('simuDir'), p_dictSimu.get('name'))
	fullDirInput = os.path.join(fullDir, 'Inputs')
	fullDirOutput = os.path.join(fullDir, 'Outputs')
	
	try:
		shutil.rmtree(fullDir)
	except:
		pass
		
	try:
		os.makedirs(fullDir)
	except:
		return "Phase 2: the folder " + fullDir + " could not be created."
	
	os.makedirs(fullDirInput)
	os.makedirs(fullDirOutput)		
		
	# Copy base files
	if p_dictSimu.get('runPhase1') == True:
		phase1Folder = os.path.join(p_dictSimu['savePhase1To'], p_dictSimu['phase1Name'])
	else:
		phase1Folder = p_dictSimu['phase1Folder']
			
	try:
		shutil.copyfile(os.path.join(phase1Folder, 'modesNumber.py'), os.path.join(fullDirInput, 'modesNumber.py'))
		shutil.copyfile(os.path.join(phase1Folder, 'modesMag10.txt'), os.path.join(fullDirInput, 'modesMag10.txt'))
		shutil.copyfile(os.path.join(phase1Folder, 'modesMag45.txt'), os.path.join(fullDirInput, 'modesMag45.txt'))
		shutil.copytree(os.path.join(phase1Folder, 'base1_b2'), os.path.join(fullDirInput, 'base1'))
	except:
		return "Some files from phase 1 (base) were not found."
	
	#
	try:
		txt = json.dumps(p_dictSimu, indent = 4, sort_keys=True)
		jsonPath = os.path.join(fullDir, 'parameters.json')
		with open(jsonPath, 'w') as f:
			f.write(txt)
		f.close()
	except:
		return jsonPath + ' could not be created (Phase 2).'
	
	# Copy materials properties files
	try:
		shutil.copyfile(p_dictSimu.get('Emat1'), os.path.join(fullDirInput, 'E_mat1.csv'))
		shutil.copyfile(p_dictSimu.get('tanDmat1'), os.path.join(fullDirInput, 'tanD_mat1.csv'))
		shutil.copyfile(p_dictSimu.get('Emat2'), os.path.join(fullDirInput, 'E_mat2.csv'))
		shutil.copyfile(p_dictSimu.get('tanDmat2'), os.path.join(fullDirInput, 'tanD_mat2.csv'))
		shutil.copyfile(p_dictSimu.get('Ebal'), os.path.join(fullDirInput, 'E_bal.csv'))
		shutil.copyfile(p_dictSimu.get('tanDbal'), os.path.join(fullDirInput, 'tanD_bal.csv'))
		
		if p_dictSimu.get('USPON') == True:
			shutil.copyfile(p_dictSimu.get('EUSP'), os.path.join(fullDirInput, 'E_USP.csv'))
			shutil.copyfile(p_dictSimu.get('tanDUSP'), os.path.join(fullDirInput, 'tanD_USP.csv'))
	except:
		return "Phase 2: some materials properties files could not be copied to " + fullDirInput + "."
	
	# Copy mesh files
	try:
		meshesDir = os.path.join(p_dictSimu['cwd'], 'Meshes')
		shutil.copyfile(os.path.join(meshesDir, 'sleeper.med'), os.path.join(fullDirInput, 'sleeper.med'))
		shutil.copyfile(os.path.join(meshesDir, 'rail.med'), os.path.join(fullDirInput, 'rail.med'))
		shutil.copyfile(p_dictSimu.get('padMesh'), os.path.join(fullDirInput, 'padR.med'))
		
		if p_dictSimu.get('computeAcoustic') == True:
			meshFileName = os.path.basename(p_dictSimu.get('acousticMesh'))
			shutil.copyfile(p_dictSimu.get('acousticMesh'), os.path.join(fullDirInput, meshFileName))
		
		if p_dictSimu.get('USPON') == True:
			shutil.copyfile(os.path.join(meshesDir, 'USP.med'), os.path.join(fullDirInput, 'USP.med'))
		
	except:
		return "Phase 2: some mesh files could not be copied to " + fullDirInput + "."

	# Frequency files & bands management
	code = PrepareFreqFiles(p_dictSimu, 2)
	if code != 0:
		return code

	# Export & comm files copy
	try:
		nJobs = p_dictSimu.get('nJobs')
		asterFilesPath = os.path.join(p_dictSimu['cwd'], 'DevFiles', 'AsterFiles')
		for i in range(nJobs):
			exportFileName = 'phase2_runSimulation_b' + str(i+1) + '.export'
			shutil.copyfile(os.path.join(asterFilesPath, exportFileName), os.path.join(fullDir, exportFileName))
		
		shutil.copyfile(os.path.join(asterFilesPath, 'phase2_runSimulation.comm'), os.path.join(fullDir, 'phase2_runSimulation.comm'))
	except:
		return "Phase 2: export or comm files could not be copied to " + fullDir + "."
	
	# Export & comm files string replacements	
	exportFiles = os.path.join(fullDir, 'phase2_runSimulation_b*.export')	
	
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
		if p_dictSimu['USPON'] == True:
			os.system('sed -i -E "s!__meshUSP__!F libr Inputs/USP.med D  26!" ' + exportFiles)
			os.system('sed -i -E "s!__EUSP__!F libr Inputs/E_USP.csv D  34!" ' + exportFiles)
			os.system('sed -i -E "s!__tanDUSP__!F libr Inputs/tanD_USP.csv D  35!" ' + exportFiles)
		else:
			os.system('sed -i -E "s!__meshUSP__!!" ' + exportFiles)
			os.system('sed -i -E "s!__EUSP__!!" ' + exportFiles)
			os.system('sed -i -E "s!__tanDUSP__!!" ' + exportFiles)
	
		if p_dictSimu.get('computeAcoustic') == True:
			txt = 'F mmed Inputs' + os.sep + meshFileName + ' D  19'
		else:
			txt = ''
		os.system('sed -i -E "s!__acousticMesh__!' + txt + '!" ' + exportFiles)

		for i in range(nJobs):
			reptrav = os.path.join(reptravroot, 'cae-caesrv1-interactif_10100' + str(i+1))
			file = os.path.join(fullDir, 'phase2_runSimulation_b' + str(i+1) + '.export')	
			os.system('sed -i -E "s!__reptrav__!' + reptrav + '!" ' + file)
			
	except:
		return "Phase 2: string replacements (sed) in export & comm files did not run properly."
		
	return 0





# Divide arbitrary frequency list into N jobs with lengths as close as possible
def PrepareFreqFiles(p_dictSimu, p_phase):
	if p_phase == 1:
		freqs = p_dictSimu['phase1Freqs']
		nJobs = p_dictSimu['nJobsPh1']
		fullDir = p_dictSimu.get('phase1WorkingDir')
	elif p_phase == 2:
		freqs = p_dictSimu['frequencies']
		nJobs = p_dictSimu['nJobs']
		fullDir = os.path.join(p_dictSimu.get('simuDir'), p_dictSimu.get('name'), 'Inputs')
	else:
		return "Error using module_run.PrepareFreqFiles()."
	
	nFreqs = len(freqs)
	freqs = sorted(freqs)
	
	if nFreqs<nJobs or nJobs<1:
		return "Error; more jobs than frequencies (phase " + str(p_phase) + ")."
	
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

# Saves under Bases/Base_<padDesign>/vectMag_<excitDir>.txt the vector of modes largest contribution
def SaveBaseFiles(p_saveBaseDir, p_simFolder, p_nJobs):

	try:
		shutil.rmtree(p_saveBaseDir)
	except:
		pass
		
	try:
		os.makedirs(p_saveBaseDir)
	except:
		return "The folder " + p_saveBaseDir + " could not be created."

	
	code = SaveModesMag(p_saveBaseDir, p_simFolder, '10', p_nJobs)
	if code != 0:
		return code
		
	code = SaveModesMag(p_saveBaseDir, p_simFolder, '45', p_nJobs)
	if code != 0:
		return code
	
	try:
		shutil.copyfile(os.path.join(p_simFolder, 'modesNumber.py'), os.path.join(p_saveBaseDir, 'modesNumber.py'))
	except:
		return "Phase 1: impossible to copy " + os.path.join(p_simFolder, 'modesNumber.py') + " to " + os.path.join(p_saveBaseDir, 'modesNumber.py') + "."
	
	done = False
	for i in range(p_nJobs):
		dir1 = os.path.join(p_simFolder, 'base1_b' + str(i+1))
		dir2 = os.path.join(p_saveBaseDir, 'base1_b' + str(i+1))
		
		if os.path.exists(dir2):
			shutil.rmtree(dir2)
		
		try:
			shutil.copytree(dir1, dir2)
			done = True
		except:
			continue
			
	if not done:
		return "Phase 1: impossible to copy base from " + p_simFolder + " to " + p_saveBaseDir + "."
		
	return 0
	
def SaveModesMag(p_saveBaseDir, p_simFolder, p_excitDir, p_nJobs):
	if os.path.exists(p_saveBaseDir) == False or os.path.exists(p_simFolder) == False:
		return "Phase 1: " +  p_saveBaseDir + " or " + p_simFolder + " do not exist."
		
	if p_nJobs < 1:
		return "Phase 1 : no jobs defined."
	
	modeMag = []
	for i in range(p_nJobs):
		modeMag.append([])
		fileVectMag = os.path.join(p_simFolder, 'modeMag' + p_excitDir + '_b' + str(i+1) + '.txt')
		with open(fileVectMag) as f:
			fileContent = f.read().splitlines()
		f.close()
		
		for line in fileContent:
			valListStr = line.split('\t')
			valListFlt = []
			for valStr in valListStr:
				try:
					val=float(valStr)
				except:
					continue
					
				valListFlt.append(val)
			modeMag[i].append(valListFlt)	
	
	nModes = len(modeMag[0])	
	macroElements = len(modeMag[0][0])
	
	if nModes < 1 or macroElements < 2:
		return "Phase 1: error with " + os.path.join(p_simFolder, 'modeMag' + p_excitDir + '_b*.txt') + "."
	
	maxMags = [0]*nModes
	for i in range(len(maxMags)):
		maxMags[i] = [0.0]*macroElements
		
	for i in range(nModes):
		for j in range(macroElements):
			maxVal = 0.0
			for k in range(p_nJobs):
				maxVal = max(maxVal, modeMag[k][i][j])
			maxMags[i][j] = maxVal
			
	maxMagsStr = []
	for i in maxMags:
		myStrList = []
		for j in i:
			myStrList.append(str(j))
		maxMagsStr.append('\t'.join(myStrList))
	
	try:
		fileContent = '\n'.join(maxMagsStr)
		file = open(os.path.join(p_saveBaseDir, 'modesMag' + p_excitDir + '.txt'), 'w')
		file.write(fileContent)
		file.close()
	except:
		return "Phase 1: impossible to create " + os.path.join(p_saveBaseDir, 'modesMag' + p_excitDir + '.txt') + "."
		
	return 0
	
def PostProcessResults(p_dictSimu):

	fullDir = os.path.join(p_dictSimu.get('simuDir'), p_dictSimu.get('name'))
	fullDirInput = os.path.join(fullDir, 'Inputs')
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
	
	# Concatenate MED files
	if os.path.exists(os.path.join(fullDirOutput, 'results_b1.med')) == False:
		return "Phase 2: " + os.path.join(fullDirOutput, 'results_b1.med') + " does not exist."
	
	# Copy .comm & .export files to simu folder
	try:
		shutil.copyfile(os.path.join(cwd, 'DevFiles', 'AsterFiles', 'postPro_concatMedFiles.comm'), os.path.join(fullDir, 'postPro_concatMedFiles.comm'))
		
		postProExportFile = os.path.join(fullDir, 'postPro_concatMedFiles1.export')
		shutil.copyfile(os.path.join(cwd, 'DevFiles', 'AsterFiles', 'postPro_concatMedFiles1.export'), postProExportFile)
	except:
		"Phase 2: error copying post-processing export and comm files."
	
	
	# Export & comm files string replacements	
	exportFile = os.path.join(fullDir, 'postPro_concatMedFiles1.export')	
	
	try:
		nCPUs = p_dictSimu.get('nCPUs')
		memlim = p_dictSimu.get('memLimit')
		reptravroot = p_dictSimu.get('reptrav')
		server = p_dictSimu.get('host')
		
		os.system('sed -i -E "s!__memjob__!' + str(memlim*1024) + '!" ' + exportFile)
		os.system('sed -i -E "s!__memlim__!' + str(memlim) + '!" ' + exportFile)
		os.system('sed -i -E "s!__memjeveux__!' + str(memlim/4) + '!" ' + exportFile)
		os.system('sed -i -E "s!__ncpus__!' + str(nCPUs) + '!" ' + exportFile)
		os.system('sed -i -E "s!__server__!' + server + '!" ' + exportFile)
		os.system('sed -i -E "s!__messagesDir__!' + os.path.join(p_dictSimu['cwd'], 'DevFiles', 'Messages') + '!" ' + exportFile)
		
		reptrav = os.path.join(reptravroot, 'cae-caesrv1-interactif_102001')
		file = os.path.join(fullDir, 'postPro_concatMedFiles1.export')	
		os.system('sed -i -E "s!__reptrav__!' + reptrav + '!" ' + file)
		
		if p_dictSimu.get('computeAcoustic') == True:
			meshFileName = os.path.basename(p_dictSimu.get('acousticMesh'))
			txt = 'F libr Inputs' + os.sep + meshFileName + ' D  7'
		else:
			txt = ''
		os.system('sed -i -E "s!__acousticMesh__!' + txt + '!" ' + exportFile)
	except:
		return "Phase 2: string replacements (sed) in post-processing export & comm files did not run properly."
	
	
	
	with open(postProExportFile) as f:
		fileContent = f.read()
	f.close()
	
	for i in range(nJobs):
		fileContent += '\nF mmed Outputs/results_b' + str(i+1) + '.med D  ' + str(10 + i)
		if p_dictSimu['computeAcoustic'] == True:
			fileContent += '\nF mmed Outputs/resuAcc_b' + str(i+1) + '.res.med D  ' + str(40 + i)
		fileContent += '\nF libr Inputs/f' + str(i+1) + '.txt D  ' + str(70 + i)
		
	with open(postProExportFile, 'w') as f:
		f.write(fileContent)
	f.close()

	messageFile = os.path.join(cwd, 'DevFiles', 'Messages', 'message_concatMedFiles.mess')
	debugMode = p_dictSimu['debugPh2']

	code = RunMultiJobs(cwd, fullDir, 'postPro_concatMedFiles', 1, messageFile, debugMode)
	if code != 0:
		return code
	
	for i in range(nJobs):
		try:
			os.remove(os.path.join(fullDirOutput, 'results_b' + str(i+1) + '.med'))
			if p_dictSimu['computeAcoustic'] == True:
				os.remove(os.path.join(fullDirOutput, 'resuAcc_b' + str(i+1) + '.res.med'))
		except:
			pass
			
		

	# Concatenate pickled python files with acoustic data
	if p_dictSimu['computeAcoustic'] == True:
		dataBands = []
		for i in range(nJobs):
			file = os.path.join(fullDirOutput, 'data_b' + str(i+1))
			if os.path.exists(file) == False:
				return "Phase 2: " + file + " does not exist."
			
			try: 
				pickle_in = open(file,"rb")
				data = pickle.load(pickle_in)
			except: 
				data = None
			dataBands.append(data)
			try: os.remove(file)
			except: pass

		allData = None
		for db in dataBands:
			if db is not None:
				allData = db
				break
				
		if allData is None:
			return "Phase 2: no acoustic results found."
		
		for ndi in allData:
			if ndi == None:
				continue
			for dtb in dataBands:
				if dtb == None:
					continue
				for ndj in dtb:
					if ndi['ID'] == ndj['ID']:
						ndi['freqs'].extend(ndj['freqs'])
						ndi['p_tot_R'].extend(ndj['p_tot_R'])
						ndi['p_tot_I'].extend(ndj['p_tot_I'])
						ndi['p_rails_R'].extend(ndj['p_rails_R'])
						ndi['p_rails_I'].extend(ndj['p_rails_I'])
						ndi['p_sleepers_R'].extend(ndj['p_sleepers_R'])
						ndi['p_sleepers_I'].extend(ndj['p_sleepers_I'])
						ndi['p_ballast_I'].extend(ndj['p_ballast_I'])
						ndi['p_ballast_R'].extend(ndj['p_ballast_R'])

		try:
			allData = sorted(allData, key=lambda k: k['ID'])
		except:
			pass

		pickle_out = open(os.path.join(fullDirOutput, 'acPressData_pythonPickle'),"wb")
		try: pickle.dump(allData, pickle_out, protocol=2)
		except: pickle.dump(None, pickle_out, protocol=2)
		pickle_out.close()


	# Compute Lw & include it in acousticResults.txt if mesh is 2D
	if p_dictSimu['computeAcoustic'] == True and p_dictSimu['acMeshDim'] == '2D':
	
		file = os.path.join(fullDirOutput, 'acousticResults.txt')
		if os.path.exists(file) == False:
			return "Phase 2: " + file + " does not exist."
		
		with open(file) as f:
			fileContent = f.read()
			lines = fileContent.splitlines()
		f.close()
		
		if len(lines) == 0:
			return "Phase 2: " + file + " is empty."
		
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
			return "Phase 2: error completing " + file + "."
			
	return 0
	
	
	
def ConcatTxtFiles(p_simFolder, p_nJobs, p_fileType, p_dataLineStart):
	newFileContentList = []
	for i in range(p_nJobs):
		file = os.path.join(p_simFolder, p_fileType + '_b' + str(i+1) + '.txt')
		
		if os.path.exists(file) == False:
			return "Phase 2: " + file + " not found."
		
		with open(file) as f:
			fileContent = f.read().splitlines()
		f.close()
		
		if len(fileContent) == 0:
			return "Phase 2: " + file + " is empty."
		
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
		return "Phase 2: error writing " + newFile + "."
		
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
	
	
	
	
	
	
	
	
	
	
	
	
	