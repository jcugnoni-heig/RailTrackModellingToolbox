TERMCMD="xterm -e"
PYTHONPATH=python
ASRUNPATH=/opt/SalomeMeca/V2019_univ/tools/Code_aster_frontend-20190/bin/as_run
ASRUNJOB=$1
SIMUDIR=$2
nCPUs=$3
messFile=$4

for (( i=1; i<=$nCPUs; i++ ))
do
 myCommand="$TERMCMD $ASRUNPATH $SIMUDIR/$ASRUNJOB$i.export &"
 eval $myCommand
 myString="pid""$i""=""\$!"
 eval $myString
done

for (( i=1; i<=$nCPUs; i++ ))
do
 myCommand="wait ""$""pid"$i
 eval $myCommand
done

lastLine=$(tail -1 $messFile)

if [ "${lastLine: -1}" != "0" ]; then
 exit 1
fi

exit 0