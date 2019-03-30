from os import environ

import matplotlib
if 'DISPLAY' not in environ:
    matplotlib.use('Agg')

import matplotlib.pyplot as plt
import math


def make_graph(num_tests, inputs, file, title, test):
    log_directory = test.get_log_directory()
    y_max = 100
    y_ticks = []
    assert 'iri' in inputs, 'Inputs must contain a list labeled "iri"'
    assert type(inputs['iri']) is list, '"iri" inputs must be in list form'

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
