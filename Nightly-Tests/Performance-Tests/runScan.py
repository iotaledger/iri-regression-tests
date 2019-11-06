import psutil
from time import sleep
import datetime
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utils.threading_tools import make_thread
import utils.scan_tools as scan
from utils.graph_tools import make_graph
import utils.logger_tools as logging

from utils.test_class import Test


def run_scans(p):
    make_thread(scan.get_cpu, p, test, scan_logger)
    make_thread(scan.get_total_cpu, test, scan_logger)
    make_thread(scan.get_mem, p, test, scan_logger)
    make_thread(scan.get_total_mem, test, scan_logger)
    make_thread(scan.get_io, p, test, scan_logger)
    make_thread(scan.get_network, test, scan_logger)


def graph_results():
    make_graph(num_tests=test.numTests,
               inputs={'iri': test.get_cpu_usage(), 'total': test.get_total_cpu_usage()},
               file='DemoCpu.png',
               title='Demo Cpu Usage',
               test=test)

    make_graph(num_tests=test.numTests,
               inputs={'iri': test.get_mem_usage(), 'total': test.get_total_mem_usage()},
               file='DemoMem.png',
               title='Demo Mem Usage',
               test=test)

    make_graph(num_tests=test.numNetTests,
               inputs={'iri': test.get_net_received_bytes()},
               file='DemoNetRecv.png',
               title='Demo Network Receiver Bytes',
               test=test)

    make_graph(num_tests=test.numNetTests,
               inputs={'iri': test.get_net_sent_bytes()},
               file='DemoNetSent.png',
               title='Demo Network Sent Bytes',
               test=test)

    make_graph(num_tests=test.numIoTests,
               inputs={'iri': test.get_io_read_bytes()},
               file='DemoIORead.png',
               title='Demo IO Read Bytes',
               test=test)

    make_graph(num_tests=test.numIoTests,
               inputs={'iri': test.get_io_write_bytes()},
               file='DemoIOWrite.png',
               title='Demo IO Write Bytes',
               test=test)


def find_iri(proc_list):
    for process in proc_list:
        proc = process.as_dict(attrs=['pid', 'cmdline', 'cpu_percent', 'memory_percent', 'memory_full_info', 'ppid'])

        for index in proc['cmdline']:
            if 'iri-' in index:
                p = psutil.Process(pid=proc['pid'])

                run_scans(p)

                sleep_time = test.numTests/(1/test.interval) + 10
                print("These scans will take {} seconds to complete...".format(sleep_time))
                sleep(sleep_time)

                graph_results()

    return None


print("Beginning Test")

base_output_dir = "./Output/"

test = Test()
test.numTests = 120
test.interval = 0.5
test.numNetTests = 0
test.numIoTests = 0

args = sys.argv

for arg in args:
    if arg == "-o":
        base_output_dir = args[args.index(arg) + 1]
        if not base_output_dir.endswith("/"):
            base_output_dir += "/"

    elif arg == "-i":
        test.interval = float(args[args.index(arg) + 1])

    elif arg == "-n":
        test.numTests = int(args[args.index(arg) + 1])


test.set_base_directory(base_output_dir)
test.set_log_directory(base_output_dir + datetime.datetime.now().date().__str__() + "/")
logging.make_log_directory(test)
raw_logger = logging.get_raw_logger(test)
scan_logger = logging.get_scan_logger(test)

cpu_usage = psutil.cpu_percent()
memory = dict(psutil.virtual_memory()._asdict())
memory_percentage = memory['percent']


procList = psutil.process_iter()
find_iri(procList)

output_string = "Results for: {}\n\nTotal Machine CPU usage: {}\n\n" \
                "Total Machine Memory usage: {}\n\n" \
                "IRI CPU usage: {}\n\nIRI Memory usage: {}\n\n" \
                "Input bytes: {}\n\nOutput bytes: {}\n\n" \
                "Network read: {}\n\nNetwork write: {}\n".format(datetime.datetime.now(), test.get_total_cpu_usage(),
                                                                 test.get_total_mem_usage(), test.get_cpu_usage(),
                                                                 test.get_mem_usage(), test.get_io_read_bytes(),
                                                                 test.get_io_write_bytes(), test.get_net_received_bytes(),
                                                                 test.get_net_sent_bytes())

raw_logger.info(output_string)

print("Done")
    

