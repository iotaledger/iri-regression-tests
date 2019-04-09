#!/usr/bin/env bash

NODE=$1
HOST=$2
PORT=$3
UUID=$4
NAMESPACE=$5

DATE=$(date +'%m-%d-%Y')

CWD=$(pwd)
BASE_DIRECTORY="$CWD/Output/"
DATE_DIRECTORY="$BASE_DIRECTORY$DATE/"
LOG_DIRECTORY="$DATE_DIRECTORY$NODE"
echo ${LOG_DIRECTORY}

if ! [[ -d ${BASE_DIRECTORY} ]];then
    mkdir ${BASE_DIRECTORY}
fi

if ! [[ -d ${DATE_DIRECTORY} ]];then
    mkdir ${DATE_DIRECTORY}
fi

if [[ -d ${LOG_DIRECTORY} ]]; then
    rm -r ${LOG_DIRECTORY}
    mkdir ${LOG_DIRECTORY}
else
    mkdir ${LOG_DIRECTORY}
fi

cd ${LOG_DIRECTORY}

for FILE in ${CWD}/apiData/*.txt; do
    FILENAME=$(basename ${FILE} .txt)

    mkdir ${FILENAME}
    cd ${FILENAME}

    LOG_FILE="$NODE.jtl"
    RUNLOG_FILE="runlog.log"
    OUTPUT="testLog.out"

    echo "Starting Single Thread test for $FILENAME on $NODE"

    mkdir "./SingleThread/"
    cd "./SingleThread/"

    bash ${CWD}/apache-jmeter-5.1.1/bin/jmeter.sh -n -t ${CWD}/iriRequests.jmx -l ${LOG_FILE} \
    -j ${RUNLOG_FILE} -Jhost ${HOST} -Jport ${PORT} -Jfile ${FILE} -JnumThreads 1 \
    -JnumLoops 100 >> ${OUTPUT}

    echo "Starting MultiThread test for $FILENAME on $NODE"

    cd ../
    mkdir "./MultiThread/"
    cd "./MultiThread/"

    bash ${CWD}/apache-jmeter-5.1.1/bin/jmeter.sh -n -t ${CWD}/iriRequests.jmx -l ${LOG_FILE} \
    -j ${RUNLOG_FILE} -Jhost ${HOST} -Jport ${PORT} -Jfile ${FILE} -JnumThreads 100 \
    -JnumLoops 1 >> ${OUTPUT}

    cd ${LOG_DIRECTORY}
done 

