import threading
import time
import socket
import argparse
import re
import sys
from argparse import RawTextHelpFormatter
from packet import Packet
import ipaddress
# Master Branch Change

exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter, message, routerhost, routerport, serverhost, serverport):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.message = message
      self.routerhost = routerhost
      self.routerport = routerport
      self.serverhost = serverhost
      self.serverport = serverport

   def run(self):
      print ("Starting " + self.name)
      # print_time(self.name, self.counter, 5)
      run_client(self.routerhost, self.routerport, self.serverhost, self.serverport, self.threadID, self.message)
      print ("Exiting " + self.name)


def run_client(router_addr, router_port, server_addr, server_port, sequence_number, message):
    print("Hello World")
    while True:
        peer_ip = ipaddress.ip_address(socket.gethostbyname(server_addr))
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout = 5
        try:
            p = Packet(packet_type=0,
                    seq_num=sequence_number,
                    peer_ip_addr=peer_ip,
                    peer_port=server_port,
                    payload=message.encode("utf-8"))
            
            conn.sendto(p.to_bytes(), (router_addr, router_port))
            #print('Send "{}" to rout234er'.format(message))
            print("[CLIENT] - Sending request to Router. Sequence Number = ", p.seq_num)
            # Try to receive a response within timeout
            conn.settimeout(timeout)
            # print('Waiting for a response')
            response, sender = conn.recvfrom(1024)
            p = Packet.from_bytes(response)
            # print('Router: ', sender)
            # print('Packet: ', p)
            print('[CLIENT] - Payload from Packet: ', p.seq_num, ' - ', p.payload.decode("utf-8"))
            return True

        except socket.timeout:
            print('[CLIENT] - No response after {}s'.format(timeout))
        finally:
            conn.close()
