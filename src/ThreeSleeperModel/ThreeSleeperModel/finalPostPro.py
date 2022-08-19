import pickle
import os
import math
import sys

dir = os.getcwd()

file = dir + '/data_b1'
try: 
    pickle_in = open(file,"rb")
    data_b1 = pickle.load(pickle_in)    
except: 
    print('No data available')
    sys.exit()

file = dir + '/data_b2'
try: 
    pickle_in = open(file,"rb")
    data_b2 = pickle.load(pickle_in)
except: 
    data_b2 = None

file = dir + '/data_b3'
try: 
    pickle_in = open(file,"rb")
    data_b3 = pickle.load(pickle_in)
except: 
    data_b3 = None

file = dir + '/data_b4'
try: 
    pickle_in = open(file,"rb")
    data_b4 = pickle.load(pickle_in)
except: 
    data_b4 = None

allData = data_b1
dataBands = [data_b2, data_b3, data_b4]

for ndi in allData:
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
            
allData = sorted(allData, key=lambda k: k['ID'])

pickle_out = open(dir + '/allPressureDataPickled',"wb")
try: pickle.dump(allData, pickle_out, protocol=2)
except: pickle.dump(None, pickle_out, protocol=2)
pickle_out.close()


##########################################################################


file = dir + '/power_concat.txt'
with open(file) as f:
    fileContent = f.read()
    lines = fileContent.splitlines()
f.close()

freqs = []
acPower = []

for line in lines:
    try: freq = float(line.split('\t')[0])
    except: continue
    try: power = float(line.split('\t')[1])
    except: continue

    freqs.append(freq)
    acPower.append(power)

# acPowerPerHz = []
# for i in range(len(freqs)-1):
    # temp = acPower[i]/(freqs[i+1] - freqs[i])
    # acPowerPerHz.append(temp)

if len(acPower)>=2:
    Lw = 0
    for i in range(len(acPower)-1):
        Lw += (acPower[i] + acPower[i+1])/2*(freqs[i+1] - freqs[i])
    Lw = 10*math.log10(Lw)
else:
    Lw = 'NaN'

fileContent = 'Lw [dB]\t' + str(Lw) + '\n\n' + fileContent
f = open(file, 'w')
f.write(fileContent)
f.close()