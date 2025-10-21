#!/bin/bash
# Usage :
# ./run_jobs.sh ASRUNJOB SIMUDIR nJobs messFile debugMode cpuPerJob memPerJob(Mo)

ASRUNPATH=__path__asRun

ASRUNJOB=$1      # Base name for .export files
SIMUDIR=$2       # Directory containing .export files
nJobs=$3         # Total number of jobs
messFile=$4      # Message file to check
debugMode=$5     # True/False
cpuPerJob=$6     # Number of CPUs per job
memPerJob=$7     # RAM per job in MB

# --- Terminal mode
if [ "$debugMode" = "True" ]; then
    TERMCMD="xterm -hold -e"
else
    TERMCMD="xterm -e"
fi

# --- Machine resources
totalCPU=$(nproc)
totalMem=$(free -m | awk '/Mem:/ {print $2}')

# --- Maximum allowed jobs
maxJobsCPU=$(( totalCPU / cpuPerJob ))
maxJobsMEM=$(( totalMem / memPerJob ))
if [ $maxJobsCPU -lt $maxJobsMEM ]; then
    maxJobs=$maxJobsCPU
else
    maxJobs=$maxJobsMEM
fi

echo "[INFO] Machine: $totalCPU CPU, $totalMem MB RAM"
echo "[INFO] Constraint: $cpuPerJob CPU/j, $memPerJob MB/j"
echo "[INFO] Maximum parallel capacity: $maxJobs jobs"
echo "[INFO] Total requested: $nJobs jobs"

running=0
pids=()

for i in $(seq 1 $nJobs); do
    # Wait if too many jobs are running
    while [ $running -ge $maxJobs ]; do
        wait -n   # wait for a job to finish
        running=$((running-1))
    done

    # Launch a new job
    $TERMCMD $ASRUNPATH $SIMUDIR/${ASRUNJOB}${i}.export &
    pid=$!
    pids+=($pid)
    running=$((running+1))
    echo "[INFO] Job $i launched (PID=$pid)"
done

# Wait for all jobs to finish
wait

# Check last message file
lastLine=$(tail -1 $messFile)
if [ "${lastLine: -1}" != "0" ]; then
    dateAndTime=$(date +"%D %T")
    last50Lines=$(tail -50 $messFile)
    echo "[$dateAndTime] Error in module_run.py during job : $ASRUNJOB, in the folder : $SIMUDIR"
    echo "Here are the last 50 lines of the message file :"
    echo "$last50Lines"
    exit 1
fi

exit 0
