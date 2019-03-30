from yaml import load, Loader
import zmq
import sys
from time import time, sleep
from iota import Iota


def set_machine_config():
    global machine
    yaml_path = './output.yml'
    stream = open(yaml_path,'r')
    yaml_file = load(stream,Loader=Loader)

    nodes = {}
    keys = yaml_file.keys()
    for key in keys:
        if key != 'seeds' and key != 'defaults':
            nodes[key] = yaml_file[key]

        machine = nodes


def get_latest_solid_milestone(node):
    api_host = machine['nodes'][node]['host']
    api_port = machine['nodes'][node]['ports']['api']
    api = Iota('http://' + api_host + ":" + str(api_port))

    response = api.get_node_info()
    index = response.get('latestSolidSubtangleMilestoneIndex')
    return index



machine = {}
set_machine_config()
port = machine['nodes']['nodeA']['ports']['zmq-feed']
port2 = machine['nodes']['nodeB']['ports']['zmq-feed']
port3 = machine['nodes']['nodeC']['ports']['zmq-feed']
host = machine['nodes']['nodeA']['host']
host2 = machine['nodes']['nodeB']['host']
host3 = machine['nodes']['nodeC']['host']

lmsi_index = get_latest_solid_milestone('nodeA')
print("Latest milestone index: {}".format(lmsi_index))
nodeB_lmsi = get_latest_solid_milestone('nodeB')
nodeC_lmsi = get_latest_solid_milestone('nodeC')
print(nodeB_lmsi)
print(nodeC_lmsi)
lmsi_list = {'nodeA': lmsi_index, 'nodeB': nodeB_lmsi, 'nodeC': nodeC_lmsi}

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://" + host + ":" + str(port))

socket2 = context.socket(zmq.SUB)
socket2.connect("tcp://" + host2 + ":" + str(port2))

socket3 = context.socket(zmq.SUB)
socket3.connect("tcp://" + host3 + ":" + str(port3))

print("Connecting to {} on ports: {}, {}, {}".format(host, port, port2, port3))

socket.setsockopt(zmq.SUBSCRIBE, b"lmsi")
socket2.setsockopt(zmq.SUBSCRIBE, b"lmsi")
socket3.setsockopt(zmq.SUBSCRIBE, b"lmsi")
#socket.setsockopt(zmq.SUBSCRIBE, b"tx")

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)
poller.register(socket2, zmq.POLLIN)
poller.register(socket3, zmq.POLLIN)


start = time()
iteration = 0
indexes = {'nodeA': 0, 'nodeB': 0, 'nodeC': 0}
synced = {'nodeA': False, 'nodeB': False, 'nodeC': False}
raw_indexes = {'nodeA': [], 'nodeB': [], 'nodeC': []}


for node in lmsi_list.keys():
    index = lmsi_list[node]
    indexes[node] = index
    if index == lmsi_index:
        synced[node] = True

print(indexes)
print(synced)

while True:
    socks = dict(poller.poll())
    iteration += 1

    if socket in socks and socks[socket] == zmq.POLLIN:
        data = socket.recv().split()[2]
        indexes['nodeA'] = data
        raw_indexes['nodeA'].append(data)
        #print("NodeA: %s \n" % data)
        if data == lmsi_index:
            print("NodeA Synced")
            synced['nodeA'] = True

    if socket2 in socks and socks[socket2] == zmq.POLLIN:
        data = socket2.recv().split()[2]
        indexes['nodeB'] = data
        raw_indexes['nodeB'].append(data)
        #print("NodeB: %s \n" % data)
        if data == lmsi_index:
            print("NodeB Synced")
            synced['nodeB'] = True

    if socket3 in socks and socks[socket3] == zmq.POLLIN:
        data = socket3.recv().split()[2]
        indexes['nodeC'] = data
        raw_indexes['nodeC'].append(data)
        #print("NodeC: {}/{} \n".format(data, lmsi_index))
        if int(data) == lmsi_index:
            print("NodeC Synced")
            synced['nodeC'] = True

    now = time()
    if iteration % 10 == 0 or all(synced[state] is True for state in synced):
        print("Node states: {}".format(indexes))
        print(synced)

    if all(synced[state] is True for state in synced):
        print("Done")
        print("Syncing took: {} seconds".format(now-start))
        for node in raw_indexes:
            if raw_indexes[node].__len__() > 0:
                print(raw_indexes[node])
        sys.exit()

