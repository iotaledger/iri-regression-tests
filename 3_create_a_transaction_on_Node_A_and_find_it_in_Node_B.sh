#!/bin/bash
echo "running test 3 mainnet - Pass transaction from node 1 to node 2"
#default version
if [ -z "$1" ];
then VER="1.4.2.3";
else VER=$1;
fi

#default port
if [ -z "$2" ];
then PORT="14266";
else PORT=$2;
fi

bash start_and_stop_a_node.sh $VER $PORT true false 2 ../pass_tx.py

