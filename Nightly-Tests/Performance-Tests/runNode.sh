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

echo "Clearing any existing IRI implementations"
kill -9 $(ps aux | grep iri- | awk '{print $2}')

echo "Checking for IRI"
if [ ! -d ./iri ]; then
    git clone https://github.com/iotaledger/iri        
fi

cd iri
git fetch
git pull
mvn clean compile
mvn package -DskipTests
cd ../

echo "IRI installed"

if [ -f ./db-* ]; then
    rm db-*
fi

echo "Downloading db"
curl -LO https://dbfiles.iota.org/devnet/1.5.0/db-686252.tar

echo "Unpacking db"
tar -xvf db-*
mv ./testnetdb ./iri/target/
cd ./iri/target/

echo "Starting IRI" 
nohup java -jar iri-* -p 14265 -u 14600 --zmq-enabled true --testnet true --remote-limit-api "" &> ../../nodelog.out & 

IRI_PID=$!
echo $IRI_PID

cd ../../

sleep 5
echo "Startup Scan Started"
nohup python ./runScan.py -i 1 -n 300 -o ./StartupOutput/ &> startupScan.log &

for i in {1..20}
    do 
        sleep 18
        let "a = $i * 5"
        echo "$a%"    
    done

#Give the node time to connect
echo "Performance Scan Started"
nohup python ./runScan.py -i 1 -n 300 -o ./RunningOutput/ &> runningScan.log &

for i in {1..20}
    do 
        sleep 18
        let "a = $i * 5"
        echo "$a%"    
    done
echo "Done Scanning. Killing node process" 
kill -9 $IRI_PID

deactivate


