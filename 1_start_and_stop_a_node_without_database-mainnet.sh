#!/bin/bash
cp -rf target node 

cd node 
#TODO read version from config
java -jar iri-$1.jar -p 14266 -u 14266 &> iri.log & 
echo $! > iri.pid
cd ..

#give time to the node to init
#TODO instead of sleep sample API untill is up
sleep 30

#stop node
#TODO kill
kill `cat node/iri.pid`
wait `cat node/iri.pid`

#Check log for errors
grep -i "error" node/iri.log
