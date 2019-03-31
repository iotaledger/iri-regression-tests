#!/usr/bin/env bash
echo "Downloading apt requirments "
sed 's/#.*//' requirements.txt | xargs sudo apt-get install -y

echo "Starting Venv"
python3 -m venv ./venv
base_dir=$(pwd)

cd ./venv/bin/
python_bin=$(pwd)

source ./activate
cd $base_dir
cd ../

echo "Installing python requirements"
pip install --upgrade pip
pip install -e .
cd $base_dir


UUID="$(uuidgen)"
K8S_NAMESPACE=$(kubectl config get-contexts $(kubectl config current-context) | tail -n+2 | awk '{print $5}')

git clone https://github.com/iotaledger/tiab

cd tiab
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
cd ../

echo "Starting TIAB"
python tiab/create_cluster.py -i iotacafe/iri-dev:latest -t ${UUID} -n ${K8S_NAMESPACE} -c ./config.yml -o ./output.yml -d
echo "Cluster created"

echo "Running ZMQ Tests"
python zmqTest.py -o ./SyncOutput

echo "Tearing down cluster"
python tiab/teardown_cluster.py -t $UUID -n $K8S_NAMESPACE

echo "Deactivating"
deactivate