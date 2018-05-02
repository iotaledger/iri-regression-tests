#!/usr/bin/env bash
if [ ! -d "iri" ]; then
  echo "please first clone IRI, exiting..."
  exit -1
fi
cd iri
git fetch origin pull/$1/head
git checkout -b pr/$1 FETCH_HEAD

if [ -z "$2" ]
then
    echo version is missing!
    exit -1
else
    VER=$2
fi

mvn package

cd ..

bash 1_start_and_stop_a_node_without_database-mainnet.sh $VER
bash 1_start_and_stop_a_node_without_database-testnet.sh $VER
bash 2_start_and_stop_a_node_known_database-mainnet.sh $VER
bash 2_start_and_stop_a_node_known_database-testnet.sh $VER
