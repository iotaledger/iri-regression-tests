#!/bin/bash

git clone https://github.com/iotaledger/iri.git
cd iri 
#todo add pr
git fetch origin pull/{pr}/head
git checkout -b pullrequest FETCH_HEAD

mvn package
cp -rf target nodeA 
cp -rf target nodeB

cd nodeA 
nohup java -jar iri-1.4.2.3.jar -p 14266 --testnet -u 14266 -n "udp://localhost:14267"&
cd ..

cd nodeB 
nohup java -jar iri-1.4.2.3.jar -p 14267 --testnet -u 14267 -n "udp://localhost:14266"&
cd ..

#give time to the node to init
#TODO instead of sleep sample API untill is up
sleep 40
#file path shouldn't be hardcoded. Should be cloned from git
#install jmeter on travis docker
/home/galrogo/apache-jmeter-4.0/bin/jmeter.sh -n -t /home/galrogo/iri-regression/Jmeter-Spammer/IRI_Basic_Sanity.jmx
