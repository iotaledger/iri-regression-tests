#!/usr/bin/env bash
echo "Downloading apt requirments "
sed 's/#.*//' requirements.txt | xargs sudo apt-get install -y

UUID="$(uuidgen)"
K8S_NAMESPACE=$(kubectl config get-contexts $(kubectl config current-context) | tail -n+2 | awk '{print $5}')
base_dir=$(pwd)

git clone https://github.com/iotaledger/tiab

cd tiab
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
cd ../../


echo "Installing python requirements"
pip install --upgrade pip
pip install -e .
cd $base_dir


echo "Starting TIAB"
python tiab/create_cluster.py -i iotacafe/iri-dev:latest -t ${UUID} -n ${K8S_NAMESPACE} -c ./config.yml -o ./output.yml -d
echo "Cluster created"


echo "Running ZMQ Tests"
python zmqTest.py -o ./SyncOutput

echo "Tearing down cluster"
python tiab/teardown_cluster.py -t $UUID -n $K8S_NAMESPACE

echo "Deactivating"
deactivate