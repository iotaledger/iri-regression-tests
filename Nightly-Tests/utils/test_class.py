class Test:
    base_directory = "./"
    log_directory = "./"

    def __init__(self):
        self.cpu_usage = []
        self.total_cpu = []
        self.total_mem = []
        self.mem_usage = []
        self.net_recv = []
        self.net_sent = []
        self.io_read = []
        self.io_write = []

    def get_cpu_usage(self):
        return self.cpu_usage

    def set_cpu_usage(self, usage):
        self.cpu_usage = usage

    def get_total_cpu_usage(self):
        return self.total_cpu

    def set_total_cpu_usage(self, usage):
        self.total_cpu = usage

    def get_mem_usage(self):
        return self.mem_usage

    def set_mem_usage(self, usage):
        self.mem_usage = usage

    def get_total_mem_usage(self):
        return self.total_mem

    def set_total_mem_usage(self, usage):
        self.total_mem = usage

    def get_net_received_bytes(self):
        return self.net_recv

    def set_net_received_bytes(self, bytes_received):
        self.net_recv = bytes_received

    def get_net_sent_bytes(self):
        return self.net_sent

    def set_net_sent_bytes(self, bytes_sent):
        self.net_sent = bytes_sent

    def get_io_read_bytes(self):
        return self.io_read

    def set_io_read_bytes(self, bytes_read):
        self.io_read = bytes_read

    def get_io_write_bytes(self):
        return self.io_write

    def set_io_write_bytes(self, bytes_written):
        self.io_write = bytes_written

    def get_log_directory(self):
        return self.log_directory

    def set_log_directory(self, directory):
        self.log_directory = directory

    def get_base_directory(self):
        return self.base_directory

    def set_base_directory(self, dir):
        self.base_directory = dir



