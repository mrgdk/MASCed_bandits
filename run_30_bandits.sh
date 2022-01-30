#!/bin/bash
MAINSIMDIR=../../src/
MAINSIMEXEC=swim

if [ $# -lt 1 ]; then
	echo "usage: $0 config"
	echo example:
	echo "  "$0 Reactive 0..2
	exit 1
fi

INIFILE="bandits_sa.ini"

for i in `seq 0 29`
do
    opp_runall -j1 $MAINSIMDIR/$MAINSIMEXEC $INIFILE -u Cmdenv -c $1 -n ..:$MAINSIMDIR:../../../queueinglib:../../src -lqueueinglib -r $i 
done
