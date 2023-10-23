1. Create text file Input/exp_modes.txt as:

freq1 node1_X node1_Y node1_Z node2_X ...... node14_Z
freq2 node1_X ...                            node14_Z
freqN ....

2. Create sleeper mesh in ./Inputs/ with groups:
  - nodes 'n1' to 'n14' (refer to existing meshes)
  - volume 'sleepere'

3. In main.py:
  - define the parameters at the beginning of the script
  - adjust the parameters bounds and tolerances at the beginning of GetResidualsVect()

4. In Props_Identification: 
  - set allSlpProps to the desired initial properties values
  - define nModes (numerical)
  - check node groups in nodesForDispl ('n1', ..., 'n14')




5. Run "python main.py"

  - dict exp_modes is created and passed to GetResidualVect() in argument

  At each iteration (in GetResidualVect()):
  - ./Working_Directory/iterNo.txt is updated to communicate the iteration number
  - ./Working_Directory/parameters.json is updated
  - ./Results/evol_parameters.txt is updated

  - Aster is run via ./runAsterJob.sh
     - If E_N, G_LN & NU_LN are not parameters, they are set equal to E_T, G_LT & NU_LT st the material is transverse isotropic
     - Initial properties are updated wrt ./Working_Directory/parameters.json
     - ./Results/num_modes.med is printed
     - ./Results/num_modes.json is written with normalized modes

  - np.array MAC_matrix is built using dictionaries exp_modes & num_modes
  - dict modalID assigns the best-matching numerical mode to each experimental mode (MAC>0.5)
  - residuals are computed, as well as additionnal residuals to penalize out-of-bound parameters
  - ./Results/MACmatrix_iter1.csv and ./Results/modalID_iter1.json are written at 1st iteration
  - ./Results/evol_modesFreqs.txt is updated
  - ./Results/evol_residuals.txt is updated