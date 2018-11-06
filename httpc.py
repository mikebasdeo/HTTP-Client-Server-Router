#!/usr/bin/env python

# Mike Basdeo - 2018

import socket
import argparse
import re
import sys
from argparse import RawTextHelpFormatter
from packet import Packet
import ipaddress

url_regex = r"^((http?):\/)?\/?([^:\/\s\?]+)\/?([^:\/\s\?]+)?"

def run_client(router_addr, router_port, server_addr, server_port):
    peer_ip = ipaddress.ip_address(socket.gethostbyname(server_addr))
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    timeout = 5
    try:
        p = Packet(packet_type=0,
                   seq_num=1,
                   peer_ip_addr=peer_ip,
                   peer_port=server_port,
                   payload=message.encode("utf-8"))
          
        conn.sendto(p.to_bytes(), (router_addr, router_port))
        print('Send "{}" to router'.format(message))

        # Try to receive a response within timeout
        conn.settimeout(timeout)
        print('Waiting for a response')
        response, sender = conn.recvfrom(1024)
        p = Packet.from_bytes(response)
        print('Router: ', sender)
        print('Packet: ', p)
        print('Payload: ' + p.payload.decode("utf-8"))

    except socket.timeout:
        print('No response after {}s'.format(timeout))
    finally:
        conn.close()


def handshake(router_addr, router_port, server_addr, server_port):
    peer_ip = ipaddress.ip_address(socket.gethostbyname(server_addr))
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    timeout = 5
    try:
        # TODO Change packet type to 1 (SYN). Then have the server recognize the packet_type and return a 2 (SYN-ACK)
        p = Packet(packet_type=1,
                   seq_num=1,
                   peer_ip_addr=peer_ip,
                   peer_port=server_port,
                   payload=message.encode("utf-8"))
          
        conn.sendto(p.to_bytes(), (router_addr, router_port))
        print('Send "{}" to router'.format(message))

        # Try to receive a response within timeout
        conn.settimeout(timeout)
        print('Waiting for a response')
        response, sender = conn.recvfrom(1024)
        p = Packet.from_bytes(response)
        print('Router: ', sender)
        print('Packet: ', p)
        print('PacketType: ' , p.packet_type)
        print('Payload: ' + p.payload.decode("utf-8"))

    except socket.timeout:
        print('No response after {}s'.format(timeout))
    finally:
        conn.close()





# create parser to pull out url from the command line
parser = argparse.ArgumentParser(description='Mike Basdeo - 26788815 \r\nhttpc is a curl-like application but supports HTTP protocol only', add_help=False, formatter_class=RawTextHelpFormatter)
parser.add_argument('--help', action='help', help='show this help message and exit')

# get/post commands are optional(either/or) and don't have dashes
parser.add_argument('mode', choices=['get','post'], help="Executes a HTTP GET or POST request for a given URL with inline data")

# positional requirement (mandatory no dash)
parser.add_argument('url', action="store", help="mandatory uniform resource locator to perform requet on")

# data command (optional)
parser.add_argument('-d', dest="data", action="store", metavar="inline-data", help="associates inline data to the body HTTP POST")
# header command (optional)
parser.add_argument('-h', dest="header", action="store", metavar="inline-data", help="associates headers to HTTP Request with the format")

# read from file command (optional)
parser.add_argument('-f', dest="file", action="store", metavar="inline-data", help="associates the content of a file to the body HTTP POST")

# output to file(optional)
parser.add_argument('-o', dest="output", action="store", metavar="inline-data", help="stores terminal output in a file")

# verbose command (optional)
parser.add_argument('-v','--verbose', action="store_true")

# port command (optional)
parser.add_argument('-p','--port', help="server port", type=int, default=8007)


parser.add_argument("--routerhost", help="router host", default="localhost")
parser.add_argument("--routerport", help="router port", type=int, default=3000)
parser.add_argument("--serverhost", help="server host", default="localhost")
parser.add_argument("--serverport", help="server port", type=int, default=8007)



args = parser.parse_args()

# chop up the found url using regex
matcher = re.search(url_regex, args.url)

server = matcher.group(3)

query_param = ''
if(matcher.group(4)):
    query_param = matcher.group(4)

if(args.port):
    port = args.port

# get request
if(args.mode == 'get'):
    message  = 'GET /'+query_param+' HTTP/1.1\r\n'
    message += 'Host:' +server+':'+str(port)+'\r\n'
    message += 'Connection: close\r\n'
    message += '\r\n'
    print("Message,", message)


# TODO Always perform a handshake before initial request
    handshake(args.routerhost, args.routerport, args.serverhost, args.serverport)

    run_client(args.routerhost, args.routerport, args.serverhost, args.serverport)

# post request
if(args.mode == 'post'):
    if(args.data):
        data = args.data
    if (args.file):
        with open (args.file, "r") as myfile:
            data=myfile.read()
    
    print(data)
    data_bytes = data.encode()
  
    message  = 'POST /'+query_param+' HTTP/1.1\r\n'
    message += 'Content-length:'+str(len(data_bytes))+'\r\n'
    message += 'Host:' +server+':'+str(port)+'\r\n'
    message += 'Connection: close\r\n\r\n'
    message += data+'\r\n'
    run_client(args.routerhost, args.routerport, args.serverhost, args.serverport)

# output to file
# if(args.output):
#     f = open(args.output, 'w')
#     sys.stdout = f
#     connect()
#     f.close()



