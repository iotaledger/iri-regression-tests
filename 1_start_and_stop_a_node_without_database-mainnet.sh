#!/bin/bash
echo "running test 1 mainnet: Start and stop a node without database"
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

bash start_and_stop_a_node.sh $VER $PORT false false 1

