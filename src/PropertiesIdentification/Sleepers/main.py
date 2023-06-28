import os
import sys
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

	# Define Folders/files
	workingDir = os.path.dirname(os.path.realpath(__file__))

	# Update iteration
	with open(os.path.join(workingDir, 'iterNo.txt'), 'r') as f:
		content = f.readline()
		iteration = int(content)
	f.close()

	with open(os.path.join(workingDir, 'iterNo.txt'), 'w') as f:
		f.write(str(iteration+1))
	f.close()

	# Append the set of parameters used to the file recording their evolution
	file_paramEvol = os.path.join(workingDir, 'Results','parameters_evolution.txt')
	with open(file_paramEvol, 'a+') as f:
		for param in p_alpha:
			f.write(str(param) + '\t')
		f.write('\n')
	f.close()

	# Save the current parameters to the JSON file, which will be read by Aster
	dictParams = {}
	for i, param in enumerate(argv[0]):
		dictParams[param] = p_alpha[i]

	file_paramInput = os.path.join(workingDir, 'Input','parameters.json')
	try:
		txt = json.dumps(dictParams, indent = 4, sort_keys=True)
		with open(file_paramInput, 'w') as f:
			f.write(txt)
		f.close()
	except:
		return file_paramInput + ' could not be created.'

	# RUN SIMULATION
	os.system('bash runAsterJob.sh')

	# Get numerical modes
	fileNumModes = os.path.join(workingDir, 'Results', 'num_modes.json')
	with open(fileNumModes, 'r') as f:
		txt = f.read()
	f.close()
	num_modes = json.loads(txt)

	# Compute MAC matrix
	exp_modes = argv[1]
	MAC_matrix = np.zeros((len(exp_modes), len(num_modes)))
	
	for iExp in range(len(exp_modes)):
		# Create numpy array for exp mode i
		dictExpMode = exp_modes['Mode ' + str(iExp+1)]
		vectExpMode = []
		for jExp in range(len(dictExpMode)-1): # 0 to 41 if 14 nodes & 3 displ
			iNode = jExp // 3 + 1
			vectExpMode.append(dictExpMode['nMeas'+str(iNode) + '_X'])
			vectExpMode.append(dictExpMode['nMeas'+str(iNode) + '_Y'])
			vectExpMode.append(dictExpMode['nMeas'+str(iNode) + '_Z'])
		vectExpMode = np.array(vectExpMode)
		
		# Compute dot product with all num modes
		for iNum in range(len(num_modes)):
			dictNumMode = num_modes['Mode ' + str(iNum+1)]
			vectNumMode = []
			for jNum in range(len(dictNumMode)-1):
				iNode = jNum // 3 + 1
				vectNumMode.append(dictNumMode['nMeas'+str(iNode) + '_X'])
				vectNumMode.append(dictNumMode['nMeas'+str(iNode) + '_Y'])
				vectNumMode.append(dictNumMode['nMeas'+str(iNode) + '_Z'])
			vectNumMode = np.array(vectNumMode)

	#######################################################################################
	SCALAR PRODUCTS ARE NOT WELL COMPUTED, IDKY...
	BUT BOTH NUM & EXP MODES ARE WELL NORMALIZED
	CHECK WHATS GOING ON HERE BELOW (print vectExpMode, print vectNumMode, analyze...)
	#######################################################################################

			dotProd = np.dot(vectExpMode, vectNumMode)
			MAC_matrix[iExp,iNum] = abs(dotProd)
	#######################################################################################

	if iteration == 1:
		MACfile = os.path.join(workingDir, 'Results', 'MACmatrix_iter' + str(iteration) + '.csv')
		np.savetxt(MACfile, MAC_matrix, delimiter=",")

	# Identify modes and define residuals
	modalID = {}
	for key in exp_modes.keys():
		modalID[key] = {'freqExp': exp_modes[key]['freq'], 'freqNum': -1, 'iModeNum': -1, 'residual': 0, 'correspondance': -1}

	expModeAvailable = [True]*len(exp_modes)

	for iNum in range(len(num_modes)):
		keyNum = 'Mode ' + str(iNum+1)
		vect = MAC_matrix[:,iNum]
		maxVal = max(vect[expModeAvailable])
		iModeExp = 0

		if maxVal < 0.5:
			continue

		if sum(vect[expModeAvailable]>0.9*maxVal) > 1:
			freqNum = num_modes[keyNum]['freq']
			smallestDelta = 1e12
			
			for iExp in range(len(exp_modes)):
				keyExp = 'Mode ' + str(iExp+1)
				freqExp = exp_modes[keyExp]['freq']
				if abs(freqExp-freqNum) < smallestDelta:
					smallestDelta = abs(freqExp-freqNum)
					iModeExp = iExp+1

		else:
			iModeExp = np.where(abs(vect - maxVal)<1e-9)
			iModeExp = iModeExp[0][0] + 1
		
		if expModeAvailable[iModeExp-1] == False: #  modalID['Mode ' + str(iModeExp)]['iModeNum'] != -1:
			continue # experimental mode already identified
				
		expModeAvailable[iModeExp-1] = False
		modalID['Mode ' + str(iModeExp)]['iModeNum'] = iNum+1
		modalID['Mode ' + str(iModeExp)]['freqNum'] = num_modes[keyNum]['freq']
		modalID['Mode ' + str(iModeExp)]['residual'] = abs(modalID['Mode ' + str(iModeExp)]['freqNum'] - modalID['Mode ' + str(iModeExp)]['freqExp'])/modalID['Mode ' + str(iModeExp)]['freqExp']
		modalID['Mode ' + str(iModeExp)]['correspondance'] = vect[iModeExp-1]

	if iteration == 1:
		temp = os.path.join(workingDir, 'Results', 'modalID_iter' + str(iteration) + '.json')
		txt = json.dumps(modalID, indent = 4, sort_keys=True)
		with open(temp, 'w') as f:
			f.write(txt)
		f.close() 

	# Append the modes to the file recording their evolution
	file_modesEvol = os.path.join(workingDir, 'Results','modes_evolution.txt')
	with open(file_modesEvol, 'a+') as f:
		for iMode in range(len(num_modes)):
			freq = num_modes['Mode '+str(iMode+1)]['freq']
			f.write(str(freq) + '\t')
		f.write('\n')
	f.close()

	# Append residuals to the file recording their evolution
	residuals = []
	for iMode in range(len(modalID)):
		mode = modalID['Mode '+str(iMode+1)]
		r = mode['residual']
		residuals.append(r)

	# for param in p_alpha:
	# 	residuals.extend(len(expModes)*[penalize(param, [0.2, 5.0], 0.1)])

	file_residEvol = os.path.join(workingDir, 'Results','residuals_evolution.txt')
	with open(file_residEvol, 'a+') as f:
		for r in residuals:
			f.write(str(r) + '\t')
		f.write('\n')
	f.close()

	print(residuals)

	return residuals


###################################################################################
# DEFINE PARAMETERS
###################################################################################
expModesFileName = 'exp_modes.txt'
nModes = 17
properties = ['E_L', 'G_LT', 'NU_LT',    'E_T', 'G_LT']
# to make the material remain transverse isotropic, consider choosing E_T over E_N
# (E_N will be set equal to it), G_LT over G_LN (idem), and NU_LT over NU_LN (idem)

###################################################################################
# PREPARE FILES
###################################################################################
workingDir = os.path.dirname(os.path.realpath(__file__))
resultsDir = os.path.join(workingDir, 'Results')
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
file_paramEvol = os.path.join(workingDir, 'Results','parameters_evolution.txt')
with open(file_paramEvol, 'w') as f:
	txt = ''
	for prop in properties:
		txt += str(prop) + '\t'
	txt += '\n'
	f.write(txt)
f.close()

# Print modes evolution file header
file_modesEvol = os.path.join(workingDir, 'Results','modes_evolution.txt')
with open(file_modesEvol, 'w') as f:
	txt = ''
	for i in range(nModes):
		txt += 'Mode ' + str(i+1) + '\t'
	txt += '\n'
	f.write(txt)
f.close()

# Print residuals evolution file header
file_residEvol = os.path.join(workingDir, 'Results','residuals_evolution.txt')
with open(file_residEvol, 'w') as f:
	txt = ''
	for i in range(nModes):
		txt += 'Mode ' + str(i+1) + '\t'
	# for i in range(nModes):
	# 	txt += 'Penalty ' + str(i+1) + '\t'
	txt += '\n'
	f.write(txt)
f.close()

###################################################################################
# IMPORT EXPERIMENTAL MODES
###################################################################################
exp_modes = {}
fileExpModes = os.path.join(workingDir, 'Input', expModesFileName)

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
				dictMode['nMeas'+str(iNode) + '_X'] = float(splittedLine[iCol])
				dictMode['nMeas'+str(iNode) + '_Y'] = float(splittedLine[iCol+1])
				dictMode['nMeas'+str(iNode) + '_Z'] = float(splittedLine[iCol+2])
				iCol += 3
			except:
				break
		
		exp_modes['Mode '+str(iMode)] = dictMode
		
		iMode += 1
f.close()

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

temp = os.path.join(workingDir, 'Input', 'exp_modes.json')
txt = json.dumps(exp_modes, indent = 4, sort_keys=True)
with open(temp, 'w') as f:
	f.write(txt)
f.close()

###################################################################################
# RUN FUNCTION ALONE OR IN OPTIMIZATION (LEAST_SQUARE)
###################################################################################
params = [1.0]*len(properties)

vect_err = GetResidualsVect(params, properties, exp_modes)
print(vect_err)

# xopt = least_squares(GetResidualsVect, params, method='lm', xtol=1e-4, ftol=1e-4, gtol=1e-4, max_nfev=100, verbose=1, args=(properties, exp_modes))
# print("Optimal solution:")
# print(str(xopt))
