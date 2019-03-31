from yaml import load, Loader
import zmq
import sys
from time import time, sleep
from iota import Iota
import os
import datetime

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


def get_latest_solid_milestones(test):
    for node in test.get_nodes():
        api = Iota(test.get_api_address(node))
        response = api.get_node_info()
        index = response.get('latestSolidSubtangleMilestoneIndex')
        if test.get_latest_milestone() == 0:
            index = response.get('latestMilestoneIndex')

        test.add_index(node, index, 0)


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
            data = socket.recv().split()[2]
            test.add_index(node, int(data), (now-start))

            if int(data) == test.get_latest_milestone():
                logger.info("NodeA Synced")
                test.set_node_sync_status(node, True)

            return node, data


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

logger.info('Setting Syncing Milestone')
get_latest_solid_milestones(test)

context = zmq.Context()
sockets = {}

logger.info("Generating Sockets")
for node in test.get_nodes():
    sockets[node] = context.socket(zmq.SUB)
    socket = sockets[node]
    socket.connect(test.get_zmq_address(node))
    socket.setsockopt(zmq.SUBSCRIBE, b"lmsi")
    logger.info("Created Socket {}".format(node))

poller = zmq.Poller()

for node in sockets:
    socket = sockets[node]
    poller.register(socket, zmq.POLLIN)

logger.info("Starting Test")
start = time()
iteration = 0
logger.info(test.get_node_indexes())
logger.info(test.get_node_sync_list())

while True:
    socket_poll = dict(poller.poll(10))
    iteration += 1
    data = ('nodeA', test.get_furthest_milestone())
    now = time()

    if socket_poll:
        data = scan_sockets(test, sockets, socket_poll)
        node = data[0]
        indexes = test.get_node_index_list(node)

    sync_list = test.get_node_sync_list()


    if iteration % 10 == 0 or all(sync_list[node] is True for node in sync_list):
        logger.info("Node states: {}".format(sync_list))
        logger.info("Node index: {}".format(data[1]))

    if all(sync_list[state] is True for state in sync_list):
        logger.info("Done")
        logger.info("Syncing took: {} seconds".format(now-start))
        make_graphs()

        sys.exit()

