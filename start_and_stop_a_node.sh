#!/bin/bash
#$1 - IRI version
#$2 - port
#$3 - is testnet?
#$4 - unpack DB?
#$5 - python script
cd iri/

cp -rf target node

cd node
#TODO host mainnet/testnet DB somewhere
if $4;
then
    if $3;
    then
    echo "unpack testnet DB"
    tar -xzf ../../testnetdb.tar.gz;
    else
    echo "unpack mainnet DB"
    tar -xzf ../../mainnetdb.tar.gz;
    fi
fi

#TODO read version from config
if $3;
then
echo "start node.. testnet"
java -jar iri-$1.jar -p $2 -u $2 --testnet &> iri.log &
else
echo "start node.. mainnet"
java -jar iri-$1.jar -p $2 -u $2 &> iri.log &
fi
echo $! > iri.pid
cd ..

#give time to the node to init
#TODO instead of sleep sample API until is up
sleep 40
if [ -n "$5" ];
then
echo "start python script.."
python $5 $2
fi

#stop node
echo "stop node.."
kill `cat node/iri.pid`
wait `cat node/iri.pid`

#Check log for errors
grep -i "error" node/iri.log

#clear
echo "clear.."
rm -rf node