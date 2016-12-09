#coding=utf-8

import socket
class LOCAL():

    def __init__(self):
        self.name = socket.getfqdn(socket.gethostname())
        self.office_server_ip = "10.210.180.43"
        self.home_server_ip = "192.168.3.10"
        self.local_ip = "localhost"
    def server_ip(self):
        if self.name == "WXJD-61222177.cq.airchina.com.cn":
            return self.office_server_ip
        elif self.name == "HUGE":
            return self.home_server_ip
        else:
            return self.local_ip
