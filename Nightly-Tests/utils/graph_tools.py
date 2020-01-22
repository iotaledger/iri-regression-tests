from os import environ

import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
import math


def make_graph(num_tests, inputs, file, title, test):
    log_directory = test.get_log_directory()
    class_name = test.__class__.__name__

    if class_name == 'Test':
        make_scan_graphs(num_tests, inputs, log_directory, file, title)
    elif class_name == 'SyncTest':
        furthest_milestone = inputs[0]
        latest_milestone = inputs[-1]
        sync_indexes = (furthest_milestone, latest_milestone)

        node = file.split('-')[0]
        x_axis = test.get_node_index_list_timestamps(node)
        make_sync_graphs(x_axis, inputs, log_directory, file, title, sync_indexes)
        
        transaction_indexes = []
        if len(test.get_transactions(node)) > 1:
            for i in range(len(test.get_transactions(node))):
                transaction_indexes.append(i + 1)
           
            sync_indexes = (0, transaction_indexes[-1])
            make_sync_graphs(test.get_transactions_timestamps(node), transaction_indexes, log_directory, '{}-Transaction-Sync.png'.format(node), 'Transactions Processed', sync_indexes) 
    else:
        raise ValueError('Test class "{}" is not supported'.format(class_name))


def make_scan_graphs(num_tests, inputs, log_directory, file, title):
    assert 'iri' in inputs, 'Inputs must contain a list labeled "iri"'
    assert type(inputs['iri']) is list, '"iri" inputs must be in list form'

    y_max = 100
    y_ticks = []
    x_axis = []

    for x in range(num_tests):
        x_axis.append(x+1)

    plt.plot(x_axis, inputs['iri'], label='IRI')

    if 'total' in inputs:
        plt.plot(x_axis, inputs['total'], label='Total')
        if max(inputs['total']) < 70.0:
            y_max = math.ceil(max(inputs['total']) / 10) * 10

    if max(inputs['iri']) > 100.0:
        y_max = math.ceil(max(inputs['iri'])/50) * 50

    for y in range(10):
        y_ticks.append(math.ceil(y_max/10) * (y+1))

    plt.yticks(y_ticks, y_ticks)

    plt.ylim(0, y_max)
    plt.title(title)
    plt.legend()

    plt.savefig(log_directory + file)
    plt.clf()


def make_sync_graphs(x_axis, inputs, log_directory, file, title, sync_indexes):
    assert len(inputs) > 1, 'Inputs must have length greater than 1'
    assert type(inputs) is list, 'Inputs must be in list form'

    y_min = (sync_indexes[0])
    y_max = (sync_indexes[1] + 10)
    y_ticks = []

    plt.plot(x_axis, inputs, label='Sync Rate')

    for y in range(10):
        y_ticks.append(math.ceil((y_max-y_min)/10) * (y+1) + y_min)

    plt.yticks(y_ticks, y_ticks)

    plt.ylim(y_min, y_max)
    plt.title(title)
    plt.legend()

    plt.savefig(log_directory + file)
    plt.clf()