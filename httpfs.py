#!/usr/bin/env python

#    __     __)               ______                     
#   (, /|  /|   , /)         (, /    )          /)       
#     / | / |    (/_   _       /---(  _   _   _(/  _  ___
#  ) /  |/  |__(_/(___(/_   ) / ____)(_(_/_)_(_(__(/_(_) 
# (_/   '                  (_/ (    
                                                                                              
#  ,gggggggggggggg                         ,gg,                                                        
# dP""""""88""""""   ,dPYb,               i8""8i                                                       
# Yb,_    88         IP'`Yb               `8,,8'                                                       
#  `""    88    gg   I8  8I                `88'                                                        
#      ggg88gggg""   I8  8'                dP"8,                                                       
#         88   8gg   I8 dP   ,ggg,        dP' `8a  ,ggg,    ,gggggg,     ggg    gg   ,ggg,    ,gggggg, 
#         88    88   I8dP   i8" "8i      dP'   `Ybi8" "8i   dP""""8I    d8"Yb   88bgi8" "8i   dP""""8I 
#   gg,   88    88   I8P    I8, ,8I  _ ,dP'     I8I8, ,8I  ,8'    8I   dP  I8   8I  I8, ,8I  ,8'    8I 
#    "Yb,,8P  _,88,_,d8b,_  `YbadP'  "888,,____,dP`YbadP' ,dP     Y8,,dP   I8, ,8I  `YbadP' ,dP     Y8,
#      "Y8P'  8P""Y88P'"Y88888P"Y888 a8P"Y88888P"888P"Y8888P      `Y88"     "Y8P"  888P"Y8888P      `Y8
                                                                                                                                                                                                                                                                   
import socket
import threading
import RequestProcessor
import argparse
from packet import Packet


def run_server(port):
    print("[Server] - Server Started.")
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        conn.bind(('', port))

        while True:
            data, sender = conn.recvfrom(1024)
            handle_client(conn, data, sender)

    finally:
        conn.close()


def handle_client(conn, data, sender):
    try:
        p = Packet.from_bytes(data)
        print("[Server] - Request from Client @: ", sender)

        response_to_return = p.payload.decode("utf-8")

        if (p.packet_type == 0):
            print("[Server] - Request : ", p.packet_type)
            print("[Server] - Payload : ", type(response_to_return))
            print("[Server] - Payload : ", response_to_return)

            response_to_return_2 = RequestProcessor.parse_request(response_to_return.encode())

            print("[Server] - Response : ", type(response_to_return_2))
            print("[Server] - Response : ", response_to_return_2)

            p.payload = (response_to_return_2).encode()
            
            conn.sendto(p.to_bytes(), sender)

        # TODO If packet type is 1, then perform a handshake. (done)
        # Client has sent a SYN, so the Server has to send back an SYN-ACK
        if (p.packet_type == 1):
            print("[Server] - PacketType (SYN): ", p.packet_type)
            response_to_return_2 = RequestProcessor.parse_request(response_to_return.encode())

            # response
            p.packet_type = 2
            p.payload = ("SYN Recieved. Here is your SYN-ACK").encode()
            print("[Server] - SYN Recieved. Here is your SYN-ACK")
            conn.sendto(p.to_bytes(), sender)

        if (p.packet_type == 3):

            # response
            response_to_return_2 = RequestProcessor.parse_request(response_to_return.encode())
            p.packet_type = 3
            p.payload = ("ACK Recieved. Here is your ACK.").encode()
            print("[Server] - ACK Recieved. Here is your ACK")
            conn.sendto(p.to_bytes(), sender)

    except Exception as e:
        print("[Server] - Error: ", e)

parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8007)
parser.add_argument('-d', dest="data", action="store", metavar="inline-data", help="Specifies the directory the server will use to read/write. Default is the current directory.")
parser.add_argument('-v','--verbose', action="store_true")

args = parser.parse_args()

# Handles Directory Change
RequestProcessor.setDirectory("data")
if(args.data):
    RequestProcessor.setDirectory(args.data)
if (args.verbose):
    RequestProcessor.setVerbose()
    


run_server(args.port)


