#!/bin/bash
cp -rf target node 

cd node 
#load mainnet DB
#TODO host mainnet DB somewhere
if [ -z "$2" ]; 
then
tar -xzf ../../mainnetdb.tar.gz
else
tar -xzf ../../testnetdb.tar.gz;
fi

#TODO read version from config
java -jar iri-$1.jar -p 14266 -u 14266 $2 &> iri.log & 
echo $! > iri.pid
cd ..

#give time to the node to init
#TODO instead of sleep sample API untill is up
sleep 30
python ../solid.py 14266 

#stop node
#TODO kill
kill `cat node/iri.pid`
wait `cat node/iri.pid`

#Check log for errors
grep -i "error" node/iri.log
