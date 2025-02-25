nCPUs=$1
messagePath=$2
log=$3

for (( i=1; i<=$nCPUs; i++ ))
do
 echo "" >> $log
 echo "##############################################" >> $log
 echo "  Harmonic Simulation Batch $i" >> $log
 echo "##############################################" >> $log
 echo "" >> $log
 tail -500 $messagePath/message_harmonicSimu_b$i.mess >> $log
done