#!/bin/bash

# Run Phase 1 of Harmonic model: generation of model with ties 

## INPUT PARAMETERS
ASRUNPATH=/opt/SalomeMeca/V2019_univ/tools/Code_aster_frontend-20190/bin/as_run
ASRUNJOB="Props_Identification.export"
### run ASTER to generate mesh to MED format 
$ASRUNPATH $ASRUNJOB
