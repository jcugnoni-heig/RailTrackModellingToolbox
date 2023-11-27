ASRUNPATH=__path__asRun
ASRUNJOB=$1
SIMUDIR=$2
nCPUs=$3
messFile=$4
debugMode=$5

if [ $debugMode = "True" ]; then
 TERMCMD="xterm -hold -e"
else
 TERMCMD="xterm -e"
fi

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