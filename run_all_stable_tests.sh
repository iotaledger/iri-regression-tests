#!/usr/bin/env bash

#default version
if [ -z "$1" ];
then VER="1.4.2.4";
else VER=$1;
fi

bash 1_start_and_stop_a_node_without_database-mainnet.sh $VER
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
bash 1_start_and_stop_a_node_without_database-testnet.sh $VER
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
bash 3_create_a_transaction_on_Node_A_and_find_it_in_Node_B.sh $VER
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
