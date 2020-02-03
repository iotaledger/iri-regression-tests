from yaml import load, Loader
import zmq
import sys
from time import time
from iota import Iota
import os
import datetime
import json
import urllib3


sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utils.sync_test_class import SyncTest
from utils import logger_tools as logging
from utils import graph_tools as graphing


def set_machine_config():
    yaml_path = './output.yml'
    stream = open(yaml_path,'r')
    yaml_file = load(stream,Loader=Loader)

    nodes = {}
    keys = yaml_file.keys()
    for key in keys:
        if key == 'nodes':
            for node in yaml_file[key]:
                nodes[node] = {}
                for node_key in yaml_file[key][node]:
                    if node_key != 'log':
                        nodes[node][node_key] = []
                        nodes[node][node_key] = yaml_file[key][node][node_key]

    sync_test = SyncTest(nodes)
    return sync_test



def get_latest_solid_milestones(test, time_elapsed):
    for node in test.get_nodes():
        api = Iota(test.get_api_address(node))
        response = api.get_node_info()
        index = response.get('latestSolidSubtangleMilestoneIndex')
        if test.get_latest_milestone() == 0:
            index = response.get('latestMilestoneIndex')
            if node == 'nodeC':
                index = 0
        logger.info("Node: {}  Index: {}".format(node, index))
        test.add_index(node, index, time_elapsed)



def get_total_transactions(test, node):
    headers = {
        'content-type': 'application/json',
        'X-IOTA-API-Version': '1'
    }
    
    command = {'command': 'TotalTransactions.getTotalTransactions'}
    command_string = json.dumps(command)

    logger.info("Sending command")
    http = urllib3.PoolManager()
    request = http.request("POST", test.get_api_address(node), body=command_string, headers=headers)
    data = json.loads(request.data.decode('utf-8'))
    total = data['ixi']['total']
    if total > test.get_num_transactions(node):
        logger.info("Filling {}".format(total - test.get_num_transactions(node)))
        test.set_num_transactions(node, total, time_elapsed)    

    return total


def get_args(args):
    global base_output_dir
    for arg in args:
        if arg == "-o":
            base_output_dir = args[args.index(arg) + 1]
            if not base_output_dir.endswith("/"):
                base_output_dir += "/"


def scan_sockets(test, socket_list, socket_poll):
    for node in socket_list:
        socket = socket_list[node]
        if socket in socket_poll and socket_poll[socket] == zmq.POLLIN:
            received = socket.recv().split()
            if received[0] == "lmsi":
                data = received[2]
                test.add_index(node, int(data), time_elapsed)
                if int(data) == test.get_latest_milestone():
                    logger.info("{} Synced".format(node))
                    test.set_node_sync_status(node, True)
                return {'node': node, 'index': data}        
             
            elif received[0] == "tx" or received[0] == b"tx":
                test.add_transaction(node, received[1], time_elapsed)
               
            return test.get_furthest_milestone()
            

def make_graphs():
    nodes = test.get_nodes()
    for node in nodes:
        if test.get_index_list_length(node) > 1:
            graphing.make_graph(num_tests=test.get_index_list_length(node),
                                inputs=test.get_node_index_list(node),
                                file='{}-Sync.png'.format(node),
                                title='{} Sync Graph'.format(node),
                                test=test)
        else:
            logger.info('No graph was made for {}'.format(node))


base_output_dir = './Output/'

test = set_machine_config()

get_args(sys.argv)

print("Setting up logs")
test.set_base_directory(base_output_dir)
test.set_log_directory(base_output_dir + datetime.datetime.now().date().__str__() + "/")
logging.make_log_directory(test)

logger = logging.get_sync_logger(test)
file_logger = logging.get_raw_logger(test)

logger.info('Setting Syncing Milestone')
get_latest_solid_milestones(test, 0)

context = zmq.Context()
sockets = {}

logger.info("Generating Sockets")
poller = zmq.Poller()

for node in test.get_nodes():
    sockets[node] = context.socket(zmq.SUB)
    socket = sockets[node]
    socket.connect(test.get_zmq_address(node))
    socket.setsockopt(zmq.SUBSCRIBE, b"lmsi")
    socket.setsockopt(zmq.SUBSCRIBE, b"tx")
    logger.info("Created Socket {} on {}".format(node, test.get_zmq_address(node)))
    poller.register(socket, zmq.POLLIN)

logger.info("Starting Test")
start = time()
iteration = 0

while True:
    iteration += 1
    socket_poll = dict(poller.poll(500))
    data = test.get_furthest_milestone()
    node = 'nodeC'

    time_elapsed = time() - start
    if len(socket_poll) != 0:
        data = scan_sockets(test, sockets, socket_poll)
        node = data['node']
        indexes = test.get_node_index_list(node)

    sync_list = test.get_node_sync_list()

    if len(test.get_transactions(node)) % 1000 == 0 or all(sync_list[node] is True for node in sync_list) or time_elapsed % 60 < 1 or iteration % 1000 == 0:
        logger.info("")        
        logger.info("Time elapsed: {}".format(int(time_elapsed)))        
        logger.info("Node states: {}".format(sync_list))
        logger.info("{} index: {}/{}\n".format(data['node'], data['index'], test.get_latest_milestone()))
        logger.info("{} / {} transactions processed".format(get_total_transactions(test, 'nodeC'), get_total_transactions(test,'nodeA')))
        get_latest_solid_milestones(test, time_elapsed)

    if all(sync_list[state] is True for state in sync_list):
        logger.info("Done")
        logger.info(sync_list)
        logger.info("Syncing took: {} seconds".format(time_elapsed))
        make_graphs()

        file_logger.info("nodeC\nindexes: \n{}\nindex timestamps: \n{}\ntransactions arrival timestamps: \n{}\n".format(test.get_node_index_list('nodeC'), test.get_node_index_list_timestamps('nodeC'), test.get_transactions_timestamps('nodeC')))

        sys.exit()

