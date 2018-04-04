#!/bin/bash
#$1 - IRI version
#$2 - port
#$3 - is testnet?
#$4 - python script
cd iri/

cp -rf target node

cd node
#TODO host mainnet/testnet DB somewhere
if $3;
then
tar -xzf ../../mainnetdb.tar.gz
else
tar -xzf ../../testnetdb.tar.gz;
fi

#TODO read version from config
java -jar iri-$1.jar -p $2 -u $2 $3 &> iri.log &
echo $! > iri.pid
cd ..

#give time to the node to init
#TODO instead of sleep sample API until is up
sleep 40
if [ -n "$4" ];
then
python $4 $2
fi

#stop node
#TODO kill
kill `cat node/iri.pid`
wait `cat node/iri.pid`

#Check log for errors
grep -i "error" node/iri.log

#clear
rm -rf node