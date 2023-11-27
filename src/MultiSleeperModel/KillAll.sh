pids=$(pgrep aster) && kill -s USR1 $pids
__path__salome killall