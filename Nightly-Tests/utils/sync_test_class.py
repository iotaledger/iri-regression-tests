class SyncTest:

    base_directory = "./"
    log_directory = "./"

    latest_milestone = 0
    furthest_milestone = {'node': None, 'index': 0}

    nodes = {}

    zmq_addresses = {}
    api_addresses = {}

    node_starting_indexes = {}
    node_index_timestamps = {}
    node_indexes = {}
    node_synced = {}

    transactions = {}
    transactions_timestamps = {}
    
    num_transactions = {}

    def __init__(self, nodes):
        # Nodes in cluster, pulled from output.yml
        self.set_nodes(nodes)

    def get_nodes(self):
        return self.nodes

    def set_nodes(self, nodes):
        self.nodes = nodes
        self.set_zmq_addresses()
        self.set_api_addresses()
        self.setup_index_lists()

    def set_zmq_addresses(self):
        for node in self.nodes:
            host = self.nodes[node]['host']
            port = self.nodes[node]['ports']['zmq-feed']
            address = "tcp://{}:{}".format(host, port)
            self.zmq_addresses[node] = address

    def set_api_addresses(self):
        for node in self.nodes:
            host = self.nodes[node]['host']
            port = self.nodes[node]['ports']['api']
            address = "http://{}:{}".format(host, port)
            self.api_addresses[node] = address

    def setup_index_lists(self):
        for node in self.nodes:
            self.node_indexes[node] = []
            self.node_index_timestamps[node] = []
            self.transactions[node] = []
            self.num_transactions[node] = 0
            self.transactions_timestamps[node] = []
            self.node_synced[node] = False





    def get_zmq_address(self, node):
        if node in self.zmq_addresses:
            return self.zmq_addresses[node]
        else:
            raise IndexError("No ZMQ address found for {}".format(node))


    def get_api_address(self, node):
        if node in self.api_addresses:
            return self.api_addresses[node]
        else:
            raise IndexError("No API address found for {}".format(node))




    ## Node Sync
    def get_node_sync_list(self):
        return self.node_synced

    def set_node_sync_status(self, node, value):
        self.node_synced[node] = value

    def get_node_sync_status(self, node):
        return self.node_synced[node]




    def add_index(self, node, index, time):
        if node in self.node_indexes:
            self.node_indexes[node].append(index)
            self.node_index_timestamps[node].append(time)
            current_index = self.get_latest_milestone()

            if current_index == 0 and node == 'nodeA':
                self.set_latest_milestone(index)

            if index < self.furthest_milestone['index'] or self.furthest_milestone['node'] is None:
                self.set_furthest_milestone(node, index)

            if index > self.furthest_milestone['index'] and node == self.furthest_milestone['node']:
                self.set_furthest_milestone(node, index)

            if self.node_indexes[node][-1] == self.get_latest_milestone():
                self.node_synced[node] = True

        else:
            raise IndexError("{} has no stored indexes".format(node))


    def get_node_indexes(self):
        return self.node_indexes

    def get_node_index_list(self, node):
        return self.node_indexes[node]

    def get_node_index_list_timestamps(self, node):
        return self.node_index_timestamps[node]

    def get_index_list_length(self, node):
        return len(self.node_indexes[node])




    def get_latest_milestone(self):
        return self.latest_milestone

    def set_latest_milestone(self, index):
        self.latest_milestone = index

    def set_furthest_milestone(self, node, index):
        self.furthest_milestone['node'] = node
        self.furthest_milestone['index'] = index

    def get_furthest_milestone(self):
        return self.furthest_milestone

    def get_transactions(self, node):
        return self.transactions[node]

    def get_transactions_timestamps(self, node):
        return self.transactions_timestamps[node]

    def add_transaction(self, node, tx, time):
        if node in self.node_indexes:
            self.transactions[node].append(tx)
            self.transactions_timestamps[node].append(time)
            self.num_transactions[node] += 1

    def get_num_transactions(self, node):
        return self.num_transactions[node]

    def set_num_transactions(self, node, num_transactions, time):
        if self.num_transactions[node] < num_transactions:
            self.transactions_timestamps[node].append(time)
            self.num_transactions[node] = num_transactions
            for x in range(num_transactions - len(self.transactions[node])):
                self.transactions[node].append('N/A')
            for y in range(num_transactions - len(self.transactions_timestamps[node])):
                self.transactions_timestamps[node].append(time)


    def get_log_directory(self):
        return self.log_directory

    def set_log_directory(self, directory):
        self.log_directory = directory

    def get_base_directory(self):
        return self.base_directory

    def set_base_directory(self, dir):
        self.base_directory = dir

