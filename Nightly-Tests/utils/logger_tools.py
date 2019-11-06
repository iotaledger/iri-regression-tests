import logging
import os
import shutil


def get_scan_logger(test):
    log_file = test.log_directory + "scanner.log"
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler(log_file)
    scan_logger = logging.getLogger("Averages")
    scan_logger.addHandler(handler)
    return scan_logger


def get_raw_logger(test):
    log_file = test.log_directory + "raw.log"
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler(log_file)
    raw_logger = logging.getLogger("Raw")
    raw_logger.addHandler(handler)
    return raw_logger


def make_log_directory(test):
    directories = [test.get_base_directory(), test.get_log_directory()]
    for directory in directories:
        if os.path.exists(directory):
            if directory == test.get_base_directory():
                pass
            else:
                try:
                    shutil.rmtree(directory)
                    os.mkdir(directory)
                except OSError as err:
                    raise "Error deleting and resetting log directory: {}".format(err)
        else:
            try:
                os.mkdir(directory)
            except OSError as err:
                print("Error making directory: '{}'.".format(directory))
                print(err)

