
trap ctrl_c INT

function ctrl_c() {
    echo
    echo "Exit called by user"
    echo ${IRI1}
    kill -9 ${IRI1}
    deactivate
    exit
}

echo "Downloading apt requirments "
#sed 's/#.*//' requirements.txt | xargs sudo apt-get install -y

UUID="$(uuidgen)"
K8S_NAMESPACE=$(kubectl config get-contexts $(kubectl config current-context) | tail -n+2 | awk '{print $5}')
base_dir=$(pwd)

echo $UUID
echo $K8S_NAMESPACE
echo $base_dir
 
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
mvn package -DskipTests
cd target 

wget https://s3.eu-central-1.amazonaws.com/iotaledger-dbfiles/dev/SyncTestDB.tar
tar -xf SyncTestDB.tar

cp iri-* $base_dir/iri2 
cp -r $base_dir/TotalTransactions ./ixi/

nohup java -jar iri-1.* -p 14265 -t 15600 --zmq-enabled true --zmq-port 5567 --testnet true --testnet-coordinator EFPNKGPCBXXXLIBYFGIGYBYTFFPIOQVNNVVWTTIYZO9NFREQGVGDQQHUUQ9CLWAEMXVDFSSMOTGAHVIBH --testnet-no-coo-validation true --milestone-start 0 --mwm 1 --remote true --remote-limit-api "" --snapshot ./snapshot.txt -n 'tcp://localhost:15601' &> nodelog.out &
IRI1=$!

cd $base_dir/iri2 

wget https://s3.eu-central-1.amazonaws.com/iotaledger-dbfiles/dev/EmptyDB.tar
tar -xf EmptyDB.tar
cp ../TotalTransactions ./ixi/

nohup java -jar iri-1.* -p 14266 -t 15601 --zmq-enabled true --zmq-port 5777 --zmq-threads 5 --testnet true --testnet-coordinator EFPNKGPCBXXXLIBYFGIGYBYTFFPIOQVNNVVWTTIYZO9NFREQGVGDQQHUUQ9CLWAEMXVDFSSMOTGAHVIBH --milestone-start 0 --mwm 1 --remote true --remote-limit-api "" --snapshot ./snapshot.txt -n 'tcp://localhost:15600' &> nodelog.out &
IRI2=$!

cd $base_dir

sleep 20 
echo "Sending milestone"
python milestone.py -i 1001

echo "Running ZMQ Tests"
python runZMQScans.py -o ./SyncOutput

echo "Killing Iri"
kill -9 $IRI1
kill -9 $IRI2

echo "Deactivating"
deactivate
