#!/usr/bin/env bash

trap ctrl_c INT

function ctrl_c() {
    echo
    echo "Exit called by user"
    echo "Tearing down cluster"
    python tiab/teardown_cluster.py -t ${UUID} -n ${K8S_NAMESPACE}
    deactivate
    exit
}

UUID="$(uuidgen)"
K8S_NAMESPACE=$(kubectl config get-contexts $(kubectl config current-context) | tail -n+2 | awk '{print $5}')
base_dir=$(pwd)


if [[ ! -d ./tiab/ ]]; then
    echo "Downloading TIAB"
    git clone https://github.com/iotaledger/tiab
fi


if [[ ! -d ./apache-jmeter-5.1.1/ ]]; then
    curl -LO https://www-eu.apache.org/dist//jmeter/binaries/apache-jmeter-5.1.1.tgz
    tar -xf apache-jmeter-5.1.1.tgz
    echo "" >> ./apache-jmeter-5.1.1/bin/user.properties
    echo "jmeter.save.saveservice.output_format=xml" >> ./apache-jmeter-5.1.1/bin/user.properties
    echo "jmeter.save.saveservice.response_data=true" >> ./apache-jmeter-5.1.1/bin/user.properties
fi


cd tiab
git fetch
git pull

echo "Installing python requirements"
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
cd ${base_dir}

cd ../
pip install --upgrade pip
pip install -e .
cd ${base_dir}

echo "Starting TIAB"
python tiab/create_cluster.py -i iotacafe/iri-dev:latest -t ${UUID} -n ${K8S_NAMESPACE} -c ./config.yml -o ./output.yml -d
echo "Cluster created"

python fetchNodeInfo.py

for ADDRESS_FILE in ./*-address; do
    NODE=$(echo ${ADDRESS_FILE} | sed -n "s+./\([a-zA-Z]*\).*+\1+p")
    HOST=$(cat ${ADDRESS_FILE} | sed -n "s/host: \(S*\)/\1/p")
    PORT=$(cat ${ADDRESS_FILE} | sed -n "s/port: \(S*\)/\1/p")

    bash ./startJmeter.sh ${NODE} ${HOST} ${PORT} ${UUID} ${K8S_NAMESPACE}

done

echo "Tearing down cluster"
python tiab/teardown_cluster.py -t ${UUID} -n ${K8S_NAMESPACE}
deactivate
