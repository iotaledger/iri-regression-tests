#!/usr/bin/env bash
bash 1_start_and_stop_a_node_without_database-mainnet.sh
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
bash 1_start_and_stop_a_node_without_database-testnet.sh
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
bash 3_create_a_transaction_on_Node_A_and_find_it_in_Node_B.sh
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
