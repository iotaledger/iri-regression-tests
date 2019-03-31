#!/usr/bin/env bash

UUID="$(uuidgen)"
K8S_NAMESPACE=$(kubectl config get-contexts $(kubectl config current-context) | tail -n+2 | awk '{print $5}')
echo $UUID
echo $K8S_NAMESPACE

git clone https://github.com/iotaledger/tiab

#cd tiab
#virtualenv venv
#source ./venv/bin/activate
#pip install -r requirements.txt
#cd ../
pip install pyzmq --user
echo "Starting TIAB"
ls tiab
python tiab/create_cluster.py -i iotacafe/iri-dev:latest -t ${UUID} -n ${K8S_NAMESPACE} -c ./config.yml -o ./output.yml -d
echo "Cluster created"
echo "Running ZMQ Tests"

python zmqTest.py

echo "Tearing down cluster"
echo $UUID
echo $K8S_NAMESPACE
python tiab/teardown_cluster.py -t $UUID -n $K8S_NAMESPACE

echo "Deactivating"
deactivate