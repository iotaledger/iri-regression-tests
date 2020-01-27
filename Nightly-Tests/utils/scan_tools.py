import psutil
from time import sleep
import math


def get_total_cpu(test, logger):
    usage = []
    average_usage = 0
    for i in range(test.numTests):
        if (i+1) % 100 == 0:
            print("Sample {}".format(i+1))
        interval_usage = psutil.cpu_percent(interval=test.interval)
        usage.append(interval_usage)
        average_usage += interval_usage

    test.set_total_cpu_usage(usage)
    logger.info("Average Total cpu usage: {}".format(average_usage/test.numTests))


def get_cpu(p, test, logger):
    usage = []
    average_usage = 0
    for i in range(test.numTests):
        interval_usage = p.cpu_percent(interval=test.interval)/psutil.cpu_count()
        usage.append(interval_usage)
        average_usage += interval_usage

    test.set_cpu_usage(usage)
    logger.info("Average IRI cpu usage: {}".format(average_usage/test.numTests))


def get_total_mem(test, logger):
    usage = []
    average_usage = 0
    for i in range(test.numTests):
        mem = psutil.virtual_memory()._asdict()
        usage.append(mem['percent'])
        average_usage += mem['percent']
        sleep(test.interval)

    test.set_total_mem_usage(usage)
    logger.info("Average Total memory usage: {}".format(average_usage/test.numTests))


def get_mem(p, test, logger):
    usage = []
    average_usage = 0
    for i in range(test.numTests):
        interval_usage = float('%.1f'%(p.memory_percent()))
        usage.append(interval_usage)
        average_usage += interval_usage
        sleep(test.interval)

    test.set_mem_usage(usage)
    logger.info("Average IRI memory usage: {}".format(average_usage/test.numTests))


def get_io(p, test, logger):
    io_count = p.io_counters()
    starting_io_read = io_count.read_bytes
    starting_io_write = io_count.write_bytes
    average_io_read = 0
    average_io_write = 0
    io_read = []
    io_write = []
    sleep(1)

    io_iteration_max = int(math.ceil(test.numTests/(1/test.interval)))
    test.numIoTests = io_iteration_max
    for call in range(io_iteration_max):
        new_io_count = p.io_counters()
        new_read = new_io_count.read_bytes - starting_io_read
        new_write = new_io_count.write_bytes - starting_io_write
        io_read.append(new_read)
        io_write.append(new_write)

        average_io_read += new_read
        average_io_write += new_write
        starting_io_read += new_read
        starting_io_write += new_write

        sleep(1)

    test.set_io_read_bytes(io_read)
    test.set_io_write_bytes(io_write)

    logger.info("Average Input: " + str(float('%.3f'%(average_io_read/io_iteration_max/1024.00))) + "kB/s")
    logger.info("Average Output: " + str(float('%.3f'%(average_io_write/io_iteration_max/1024.00))) + "kB/s")


def get_network(test, logger):
    net_count = psutil.net_io_counters()
    starting_net_recv = net_count.bytes_recv
    starting_net_send = net_count.bytes_sent

    net_recv = test.get_net_received_bytes()
    net_sent = test.get_net_sent_bytes()

    average_net_read = 0
    average_net_write = 0
    sleep(1)

    net_iteration_max = int(math.ceil(test.numTests/(1/test.interval)))
    test.numNetTests = net_iteration_max
    for call in range(net_iteration_max):
        new_net_count = psutil.net_io_counters()
        new_recv = new_net_count.bytes_recv - starting_net_recv
        new_sent = new_net_count.bytes_sent - starting_net_send
        net_recv.append(new_recv)
        net_sent.append(new_sent)

        average_net_read += new_recv
        average_net_write += new_sent
        starting_net_recv += new_recv
        starting_net_send += new_sent

        sleep(1)

    logger.info("Network Received: " + str(float('%.3f'%(average_net_read/net_iteration_max/1024.00))) + "kB/s")
    logger.info("Network Sent: " + str(float('%.3f'%(average_net_write/net_iteration_max/1024.00))) + "kB/s")
