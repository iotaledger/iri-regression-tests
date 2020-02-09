set -x

trap ctrl_c INT

function ctrl_c() {
    echo -e "\nExit called by user"
    for pod in $(kubectl get pods -o jsonpath='{.items[*].metadata.name}');do
        echo "Pulling node logs..." 
        kubectl logs $pod > ./SyncOutput/$DATE/$(kubectl get pod $pod -o jsonpath='{.metadata.labels.nodenum}').log
    done

    timeout 10 tiab/teardown_cluster.py -t $UUID -n $K8S_NAMESPACE
    deactivate
    exit
}

if [ "$#" -ne 1 ]; then
    echo "Please specify an image to test"
    exit 1
fi

set -x

echo "Downloading apt requirments "
sed 's/#.*//' requirements.txt | xargs apt-get install -y

UUID="$(uuidgen)"
K8S_NAMESPACE=$(kubectl config get-contexts $(kubectl config current-context) | tail -n+2 | awk '{print $5}')
base_dir=$(pwd)
IMAGE=${SYNC_IMAGE:-"iotacafe/iri-dev"}
DATE=$(date '+%Y-%m-%d')

if [ ! -d tiab ]; then
  git clone --depth 1 https://github.com/iotaledger/tiab tiab
fi
 
virtualenv -p python2 venv
source ./venv/bin/activate 

cd tiab
git fetch
git pull
echo "tiab revision: "; git rev-parse HEAD
pip install -r requirements.txt
cd $base_dir/../

echo "Installing python requirements"
pip install --upgrade pip
pip install -e .
cd $base_dir

ERROR=0

python tiab/create_cluster.py -i $IMAGE -t $UUID -n $K8S_NAMESPACE -c config.yml -o output.yml -x $base_dir -e "apt update && apt install unzip && wget http://search.maven.org/remotecontent\?filepath\=org/jacoco/jacoco/0.8.4/jacoco-0.8.4.zip -O jacoco.zip && mkdir /opt/jacoco && unzip jacoco.zip -d /opt/jacoco" -d

if [ $? -ne 0 ]; then
    ERROR=1
    python <<EOF
import yaml
for (key,value) in yaml.load(open('output.yml'))['nodes'].iteritems():
  if value['status'] == 'Error':
    print(value['log'])
EOF
fi

if [ $ERROR -eq 0 ]; then
  sleep 20
  echo "Sending milestone"
  python milestone.py -i 2006

  echo "Running ZMQ Tests"
  python runZMQScans.py -o ./SyncOutput

  for pod in $(kubectl get pods -o jsonpath='{.items[*].metadata.name}');do
    echo $pod
    kubectl logs $pod > ./SyncOutput/$DATE/$(kubectl get pod $pod -o jsonpath='{.metadata.labels.nodenum}').log
  done
fi

echo "Tearing down cluster" 
timeout 10 tiab/teardown_cluster.py -t $UUID -n $K8S_NAMESPACE

echo "Deactivating"
deactivate

exit $ERROR
