import os
from scipy.optimize import least_squares
import shutil
import json
import numpy as np

def penalize(x,bounds,tol,n=2):
   '''smooth penalty function to enforce bounds
     bounds=[min,max]=penalty start being significant (=softerror)
     n is the power of the asymptotic response of the penalty
     for x in [min+tol,max-tol] penalty is null
     with n=2, when x equal min or max, penalty=1.0
     when x equal min-tol or max+tol penalty is 6.4
     when x equal min-2*tol or max+2*tol penalty ~ 50 
     penalty function = 2*xp^(n+2)/(x^2+1) with xp=(x-(max-tol))/tol
   '''
   xmin1=bounds[0]
   xmax1=bounds[1]
   rng=xmax1-xmin1
   dx=tol
   xmin0=xmin1+dx
   xmax0=xmax1-dx
   xmin2=xmin1-dx
   xmax2=xmax1+dx
   dist=0.
   if x<xmin0:
     dist=abs(x-xmin0)/tol
   if x>xmax0:
     dist=abs(x-xmax0)/tol
   penalty=2*pow(dist,n+2)/(pow(dist,2)+1);
   return penalty


def GetResidualsVect(p_alpha, *argv):

	bounds = [0.05, 2.5]
	tolerance = 0.05

	# Define Folders/files
	mainDir = os.path.dirname(os.path.realpath(__file__))
	inputDir = os.path.join(mainDir, 'Inputs')
	workingDir = os.path.join(mainDir, 'Working_Directory')
	resultsDir = os.path.join(mainDir, 'Results')

	# Update iteration
	with open(os.path.join(workingDir, 'iterNo.txt'), 'r') as f:
		content = f.readline()
		iteration = int(content)
	f.close()

	with open(os.path.join(workingDir, 'iterNo.txt'), 'w') as f:
		f.write(str(iteration+1))
	f.close()

	# Append the set of parameters used to the file recording their evolution
	file_paramEvol = os.path.join(resultsDir,'evol_parameters.txt')
	with open(file_paramEvol, 'a+') as f:
		for param in p_alpha:
			f.write(str(param) + '\t')
		f.write('\n')
	f.close()

	# Save the current parameters to the JSON file, which will be read by Aster
	dictParams = {}
	for i, param in enumerate(argv[0]):
		dictParams[param] = p_alpha[i]
		# ex. dictParams["E_L"] = 1.027

	file_paramInput = os.path.join(workingDir, 'parameters.json')
	try:
		txt = json.dumps(dictParams, indent = 4, sort_keys=True)
		with open(file_paramInput, 'w') as f:
			f.write(txt)
		f.close()
	except:
		return file_paramInput + ' could not be created.'
	
	# Duplicate export file, because the one that is run always end up having absolute paths written
	shutil.copyfile(os.path.join(workingDir, 'Props_Identification_template.export'), os.path.join(workingDir, 'Props_Identification.export'))

	# RUN SIMULATION
	os.system('cd ' + workingDir + '\nbash runAsterJob.sh')

	# Copy results to result directory
	shutil.copyfile(os.path.join(workingDir, 'num_modes.med'), os.path.join(resultsDir, 'num_modes.med'))
	if iteration == 1:
		shutil.copyfile(os.path.join(workingDir, 'message.mess'), os.path.join(resultsDir, 'message_iter1.mess'))
	else:
		shutil.copyfile(os.path.join(workingDir, 'message.mess'), os.path.join(resultsDir, 'message_lastIter.mess'))
	
	# Get numerical modes as JSON
	fileNumModes = os.path.join(workingDir, 'num_modes.json')
	with open(fileNumModes, 'r') as f:
		txt = f.read()
	f.close()
	num_modes = json.loads(txt)

	## Compute MAC matrix
	exp_modes = argv[1]
	MAC_matrix = np.zeros((len(exp_modes), len(num_modes)))
	
	# Create numpy array for exp mode iExp
	for iExp in range(len(exp_modes)):
		dictExpMode = exp_modes['Mode ' + str(iExp+1)]
		vectExpMode = []
		for iNode in range((len(dictExpMode)-1)/3): # 0 to 14
			vectExpMode.append(dictExpMode['n'+str(iNode+1) + '_X'])
			vectExpMode.append(dictExpMode['n'+str(iNode+1) + '_Y'])
			vectExpMode.append(dictExpMode['n'+str(iNode+1) + '_Z'])
		vectExpMode = np.array(vectExpMode)

		# Create numpy array for num mode iNum
		for iNum in range(len(num_modes)):
			dictNumMode = num_modes['Mode ' + str(iNum+1)]
			vectNumMode = []
			for iNode in range((len(dictNumMode)-1)/3):
				vectNumMode.append(dictNumMode['n'+str(iNode+1) + '_X'])
				vectNumMode.append(dictNumMode['n'+str(iNode+1) + '_Y'])
				vectNumMode.append(dictNumMode['n'+str(iNode+1) + '_Z'])
			vectNumMode = np.array(vectNumMode)

			dotProd = np.dot(vectExpMode, vectNumMode)
			MAC_matrix[iExp,iNum] = abs(dotProd)

	if iteration == 1:
		MACfile = os.path.join(resultsDir, 'MACmatrix_iter' + str(iteration) + '.csv')
		np.savetxt(MACfile, MAC_matrix, delimiter=",")

	# Identify modes and define residuals
	modalID = {}
	numModeAvailable = [True]*len(num_modes)	

	for iExp in range(len(exp_modes)):
		keyExp = 'Mode ' + str(iExp+1)
		modalID[keyExp] = {'freqExp': exp_modes[keyExp]['freq'], 'freqNum': -1, 'iModeNum': -1, 'residual': 0, 'MAC': -1}
		maxVal = np.max(MAC_matrix[iExp,:][numModeAvailable])
		iMax = np.where(numModeAvailable, MAC_matrix[iExp,:], 0).argmax() # replace MAC values of not available modes by 0 to search argmax() among available ones and still have the right index
		

		if maxVal < 0.5:
			print('max MAC value for exp mode ' + str(iExp+1) + ' = ' + str(maxVal) + ' (num mode ' + str(iMax) + ')')
			MACfile = os.path.join(resultsDir, 'MACmatrix_iter' + str(iteration) + '.csv')
			np.savetxt(MACfile, MAC_matrix, delimiter=",")
			continue

		iMax = np.where(numModeAvailable, MAC_matrix[iExp,:], 0).argmax() # replace MAC values of not available modes by 0 to search argmax() among available ones and still have the right index
		keyNum = 'Mode ' + str(iMax+1)
		
		modalID[keyExp]['iModeNum'] = iMax + 1
		modalID[keyExp]['freqNum'] = num_modes[keyNum]['freq']
		modalID[keyExp]['MAC'] = maxVal
		modalID[keyExp]['residual'] = abs(modalID[keyExp]['freqNum'] - modalID[keyExp]['freqExp'])/modalID[keyExp]['freqExp']
		numModeAvailable[iMax] = False



	if iteration == 1:
		temp = os.path.join(resultsDir, 'modalID_iter' + str(iteration) + '.json')
		txt = json.dumps(modalID, indent = 4, sort_keys=True)
		with open(temp, 'w') as f:
			f.write(txt)
		f.close()


	# Append the modes to the file recording their evolution
	file_modesEvol = os.path.join(resultsDir, 'evol_modesFreqs.txt')
	with open(file_modesEvol, 'a+') as f:
		for iMode in range(len(exp_modes)):
			freq = modalID['Mode ' + str(iMode+1)]['freqNum']
			f.write(str(freq) + '\t')
		f.write('\n')
	f.close()

	# Append residuals to the file recording their evolution
	residuals = []
	for iMode in range(len(modalID)):
		mode = modalID['Mode ' + str(iMode+1)]
		r = mode['residual']
		residuals.append(r)

	for param in p_alpha:
		residuals.extend(len(exp_modes)*[penalize(param, bounds, tolerance)])

	file_residEvol = os.path.join(resultsDir, 'evol_residuals.txt')
	with open(file_residEvol, 'a+') as f:
		for r in residuals:
			f.write(str(r) + '\t')
		f.write('\n')
	f.close()

	# print(residuals)

	return residuals






###################################################################################
# DEFINE PARAMETERS
###################################################################################
sleeperMesh = 'sleeper_RpIV.med'
expModesFileName = 'exp_modes_RpIV_opti.txt'
nModesExp = 10
properties = ['E_L', 'E_N', 'E_T', 'NU_LT', 'NU_LN', 'NU_TN', 'G_LT', 'G_LN', 'G_TN']
params = [1.0]*len(properties)
firstIterOnly = False

# 1	'E_L'
# 2	'E_N'
# 3	'E_T'
# 4	'NU_LT'
# 5	'NU_LN':
# 6	'NU_TN'
# 7	'G_LT'
# 8	'G_LN':
# 9	'G_TN'

# to make the material remain transverse isotropic, consider choosing E_T over E_N
# (E_N will be set equal to it), G_LT over G_LN (idem), and NU_LT over NU_LN (idem)

###################################################################################
# PREPARE FILES
###################################################################################
mainDir = os.path.dirname(os.path.realpath(__file__))
inputDir = os.path.join(mainDir, 'Inputs')
workingDir = os.path.join(mainDir, 'Working_Directory')
resultsDir = os.path.join(mainDir, 'Results')

try:
	shutil.rmtree(resultsDir)
except:
	pass
os.makedirs(resultsDir)

# Print current iteration to file
with open(os.path.join(workingDir, 'iterNo.txt'), 'w') as f:
	f.write('1')
f.close()

# Print parameter evolution file header
file_paramEvol = os.path.join(resultsDir,'evol_parameters.txt')
with open(file_paramEvol, 'w') as f:
	txt = ''
	for prop in properties:
		txt += str(prop) + '\t'
	txt += '\n'
	f.write(txt)
f.close()

# Print modes evolution file header
file_modesEvol = os.path.join(resultsDir,'evol_modesFreqs.txt')
with open(file_modesEvol, 'w') as f:
	txt = ''
	for i in range(nModesExp):
		txt += 'Mode ' + str(i+1) + '\t'
	txt += '\n'
	f.write(txt)
f.close()

# Print residuals evolution file header
file_residEvol = os.path.join(resultsDir,'evol_residuals.txt')
with open(file_residEvol, 'w') as f:
	txt = ''
	for i in range(nModesExp):
		txt += 'Mode ' + str(i+1) + '\t'
	# for i in range(nModes):
	# 	txt += 'Penalty ' + str(i+1) + '\t'
	txt += '\n'
	f.write(txt)
f.close()

###################################################################################
# COPY SLEEPER TO WORKING DIRECTORY
###################################################################################
src = os.path.join(inputDir, sleeperMesh)
dst = os.path.join(workingDir, 'sleeper.med')
shutil.copyfile(src, dst)

###################################################################################
# IMPORT EXPERIMENTAL MODES
###################################################################################
exp_modes = {}
fileExpModes = os.path.join(inputDir, expModesFileName)

with open(fileExpModes, 'r') as f:
	iMode = 1
	lines = f.readlines()
	for line in lines:
		splittedLine = line.split('\t')
		
		try:
			freq = float(splittedLine[0])
		except:
			continue

		dictMode = {'freq' : freq}
		iCol = 1
		while(True):
			try:
				iNode = (iCol-1) // 3 + 1
				dictMode['n'+str(iNode) + '_X'] = float(splittedLine[iCol])
				dictMode['n'+str(iNode) + '_Y'] = float(splittedLine[iCol+1])
				dictMode['n'+str(iNode) + '_Z'] = float(splittedLine[iCol+2])
				iCol += 3
			except:
				break
		
		exp_modes['Mode '+str(iMode)] = dictMode
		
		iMode += 1
f.close()

###################################################################################
# NORMALIZE EXPERIMENTAL MODES
###################################################################################

for key1 in exp_modes.keys():

	norm = 0
	for key2 in exp_modes[key1].keys():
		if key2 != 'freq':
			norm += exp_modes[key1][key2]**2
	norm = norm**(1/2.0)

	if norm == 0:
		continue

	for key2 in exp_modes[key1].keys():
		if key2 != 'freq':
			exp_modes[key1][key2] /= norm

# Write normalized exp_modes.json to working directory and to results (they can be reused to be visualized)
f1 = os.path.join(workingDir, 'exp_modes.json')
f2 = os.path.join(resultsDir, 'exp_modes.json')
txt = json.dumps(exp_modes, indent = 4, sort_keys=True)
with open(f1, 'w') as f:
	f.write(txt)
f.close()
with open(f2, 'w') as f:
	f.write(txt)
f.close()

###################################################################################
# RUN FUNCTION ALONE OR IN OPTIMIZATION (LEAST_SQUARE)
###################################################################################
if firstIterOnly:
	vect_err = GetResidualsVect(params, properties, exp_modes)
	print(vect_err)
else:
	xopt = least_squares(GetResidualsVect, params, method='lm', xtol=1e-5, ftol=1e-5, gtol=1e-5, max_nfev=1000, verbose=1, args=(properties, exp_modes))
	print("Optimal solution:")
	print(str(xopt))
