#!/usr/bin/env python

#    __     __)               ______                     
#   (, /|  /|   , /)         (, /    )          /)       
#     / | / |    (/_   _       /---(  _   _   _(/  _  ___
#  ) /  |/  |__(_/(___(/_   ) / ____)(_(_/_)_(_(__(/_(_) 
# (_/   '                  (_/ (    
                                                                                         
#            ,dPYb,                               I8       I8                              
#            IP'`Yb                               I8       I8                              
#            I8  8I  gg                        88888888 88888888                           
#            I8  8'  ""                           I8       I8                              
#    ,gggg,  I8 dP   gg    ,ggg,    ,ggg,,ggg,    I8       I8   gg    gg    gg   ,ggggg,   
#   dP"  "Yb I8dP    88   i8" "8i  ,8" "8P" "8,   I8       I8   I8    I8    88bgdP"  "Y8ggg
#  i8'       I8P     88   I8, ,8I  I8   8I   8I  ,I8,     ,I8,  I8    I8    8I i8'    ,8I  
# ,d8,_    _,d8b,_ _,88,_ `YbadP' ,dP   8I   Yb,,d88b,   ,d88b,,d8,  ,d8,  ,8I,d8,   ,d8'  
# P""Y8888PP8P'"Y888P""Y8888P"Y8888P'   8I   `Y88P""Y8   8P""Y8P""Y88P""Y88P" P"Y8888P"    
                                                                                                                                         
import socket
import argparse
import re
import sys
from argparse import RawTextHelpFormatter
from packet import Packet
import ipaddress
from thread import myThread

url_regex = r"^((http?):\/)?\/?([^:\/\s\?]+)\/?([^:\/\s\?]+)?"


def syn(router_addr, router_port, server_addr, server_port):
    while True:
        peer_ip = ipaddress.ip_address(socket.gethostbyname(server_addr))
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout = 5
        try:
            p = Packet(packet_type=1,
                    seq_num=1,
                    peer_ip_addr=peer_ip,
                    peer_port=server_port,
                    payload=message.encode("utf-8"))
            
            conn.sendto(p.to_bytes(), (router_addr, router_port))
            print(" \n ")
            print("-------------------BEGINNING HANDSHAKE-----------------")
            print("[CLIENT] - Sending SYN - (PacketType = 1)")
            conn.settimeout(timeout)
            print('[CLIENT] - Waiting For A Response - Should be an SYN-ACK')
            response, sender = conn.recvfrom(1024)
            p = Packet.from_bytes(response)
            print("[CLIENT] - Response Recieved. Is it a SYN-ACK? (Packet Type of 2)")
            print('[CLIENT] - PacketType =  ' , p.packet_type)

            if(p.packet_type == 2):
                print("[CLIENT] - Yes, Got a SYN-ACK back, send back ACK (Packet Type of 3)")
                # just fucking send packet of type 3 send here and don't get anything back.
                return True

        except socket.timeout:
            print('[CLIENT] - No response after %d for Packet %d ' %(timeout, p.seq_num))
        finally:
            conn.close()

def ack(router_addr, router_port, server_addr, server_port):
    while True:
        peer_ip = ipaddress.ip_address(socket.gethostbyname(server_addr))
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout = 5
        try:
            # Packet type to 1 (SYN). Then have the server recognize the packet_type and return a 2 (SYN-ACK)
            p = Packet(packet_type=3,
                    seq_num=1,
                    peer_ip_addr=peer_ip,
                    peer_port=server_port,
                    payload=message.encode("utf-8"))
            print("[CLIENT] - Sending ACK")
            conn.sendto(p.to_bytes(), (router_addr, router_port))
            

            # Receive a response within timeout
            conn.settimeout(timeout)
            print("[CLIENT] - Waiting For A Response -  (Should be an ACK)")
            response, sender = conn.recvfrom(1024)
            p = Packet.from_bytes(response)

            print("[CLIENT] - Response Recieved. Is it a SYN-ACK? (Packet of Type 3)")
            print('[CLIENT] - PacketType = ' , p.packet_type)
            print("[CLIENT] - Yes, Got an ACK back. Proceed with request.")
            return True

        except socket.timeout:
            print('[CLIENT] - No response after %ds for Packet %d ' %(timeout, p.seq_num))
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

def handshake():
    handShake = False
    # Always perform a handshake before initial request.
    while handShake == False:
        sendSyn = False
        sendSyn = syn(args.routerhost, args.routerport, args.serverhost, args.serverport)

        # Only return true when the whole thing comes back. check at each step. 
        if sendSyn == True:
            sendAck = ack(args.routerhost, args.routerport, args.serverhost, args.serverport)
            if sendAck == True:
                print("--------------------HANDSHAKE COMPLETE-----------------")
                handShake = True
    return True



# GET REQUEST
if(args.mode == 'get'):
    message  = 'GET /'+query_param+' HTTP/1.1\r\n'
    message += 'Host:' +server+':'+str(port)+'\r\n'
    message += 'Connection: close\r\n'
    message += '\r\n'

    handShakeComplete = handshake()
    if handShakeComplete == True:

        objs = [myThread(i, "Thread", i, message, args.routerhost, args.routerport, args.serverhost, args.serverport) for i in range(10)]
        for obj in objs:
            obj.start()
        for ojb in objs:
            obj.join()


# POST REQUEST
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
    handShakeComplete = handshake()
    if handShakeComplete == True:
        objs = [myThread(i, "Thread", i, message, args.routerhost, args.routerport, args.serverhost, args.serverport) for i in range(10)]
        for obj in objs:
            obj.start()
        for ojb in objs:
            obj.join()


# TODO Check that this still works.
# if(args.output):
#     f = open(args.output, 'w')
#     sys.stdout = f
#     connect()
#     f.close()



