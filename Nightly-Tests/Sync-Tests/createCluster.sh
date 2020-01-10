
trap ctrl_c INT

function ctrl_c() {
    echo -e "\nExit called by user"
    kill -9 ${IRI1}
    kill -9 ${IRI2}
    deactivate
    exit
}

echo "Downloading apt requirments "
#sed 's/#.*//' requirements.txt | xargs sudo apt-get install -y

UUID="$(uuidgen)"
K8S_NAMESPACE=$(kubectl config get-contexts $(kubectl config current-context) | tail -n+2 | awk '{print $5}')
base_dir=$(pwd)
DATE=$(date '+%Y-%m-%d')

echo $UUID
echo $K8S_NAMESPACE
 
virtualenv venv
source ./venv/bin/activate 
cd ../
echo "Installing python requirements"
pip install --upgrade pip
pip install -e .
cd $base_dir

if [[ -d 'iri1' ]]; then 
    rm -rf iri1 
fi
if [[ -d 'iri2' ]]; then 
    rm -rf iri2
fi
 

mkdir iri1
mkdir iri2
mkdir iri2/ixi/

cd iri1
git clone https://github.com/iotaledger/iri
cd iri
#git checkout experimental-milestone-stage
mvn package -DskipTests
cd target 

wget https://s3.eu-central-1.amazonaws.com/iotaledger-dbfiles/dev/SyncTestsDbComplete.tar
tar -xf SyncTestsDbComplete.tar
mkdir ./ixi/

cp iri-* $base_dir/iri2 
cp -rf $base_dir/TotalTransactions/ ./ixi/

echo "Starting iri"
nohup java -jar iri-1.* -p 14265 -t 15600 -u 14600 --zmq-enable-tcp true --zmq-port 5555 --testnet true --testnet-coordinator KSAFREMKHHYHSXNLGZPFVHANVHVMKWSGEAHGTXZCSQMXTCZXOGBLVPCWFKVAEQYDJMQALKZRKOTWLGBSC  --testnet-no-coo-validation true --milestone-start 0 --mwm 1 --remote true --testnet-no-coo-validation true --remote-limit-api "" --snapshot ./snapshot.txt -n 'tcp://localhost:15601' &> Node1.out &
IRI1=$!
echo "IRI started ${IRI1}"

cd $base_dir/iri2 

wget https://s3.eu-central-1.amazonaws.com/iotaledger-dbfiles/dev/EmptyDB.tar
tar -xf EmptyDB.tar
cp -rf ../TotalTransactions ./ixi/

nohup java -jar iri-1.* -p 14267 -t 15601 --zmq-enable-tcp true --zmq-port 5556 --testnet true --testnet-coordinator KSAFREMKHHYHSXNLGZPFVHANVHVMKWSGEAHGTXZCSQMXTCZXOGBLVPCWFKVAEQYDJMQALKZRKOTWLGBSC --milestone-start 0 --mwm 1 --remote true --testnet-no-coo-validation true --remote-limit-api "" --snapshot ./snapshot.txt -n 'tcp://localhost:15600' &> Node2.out &
IRI2=$!

cd $base_dir

sleep 20 
echo "Sending milestone"
python milestone.py -i 2005

echo "Running ZMQ Tests"
python runZMQScans.py -o ./SyncOutput

cp iri1/iri/target/Node1.out SyncOutput/${DATE}
cp iri2/Node2.out SyncOutput/${DATE} 

echo "Killing Iri"
kill -9 $IRI1
kill -9 $IRI2

echo "Deactivating"
deactivate
