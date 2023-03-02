pids=$(pgrep aster) && kill -s USR1 $pids
salome killall