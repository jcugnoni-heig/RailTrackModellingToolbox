#!/bin/bash
source setEnvMFRONT.sh
mfront-3.2.1 --obuild --interface=aster GeneralizedMaxwell.mfront
cp ./src/libAsterBehaviour.so .
