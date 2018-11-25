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
        # print("[Server] - Server is listening at, port")
        while True:
            data, sender = conn.recvfrom(1024)
            handle_client(conn, data, sender)

    finally:
        conn.close()


def handle_client(conn, data, sender):
    try:
        p = Packet.from_bytes(data)
        print("[Server] - Request from Client @: ", sender)
        # print("[Server] - Packet Recieved: ", p)


        
        response_to_return = p.payload.decode("utf-8")



        
        # print("[Server] - PacketType : ", p.packet_type)


        # Found the spot
        # if the packet is type 3, then what....


        if (p.packet_type == 0):
            print("[Server] - Request : ", p.packet_type)
            print("[Server] - Payload : ", type(response_to_return))
            print("[Server] - Payload : ", response_to_return)

            response_to_return_2 = RequestProcessor.parse_request(response_to_return.encode())

            print("[Server] - Response : ", type(response_to_return_2))
            print("[Server] - Response : ", response_to_return_2)

            p.payload = (response_to_return_2).encode()
            

            conn.sendto(p.to_bytes(), sender)


        # TODO If packet type is 1, then perform a handshake.
        # Client has sent a SYN, so the Server has to send back an SYN-ACK
        if (p.packet_type == 1):
            print("[Server] - PacketType (SYN): ", p.packet_type)
            # print("[Server] - Payload : ", type(response_to_return))
            # print("[Server] - Payload : ", response_to_return)

            response_to_return_2 = RequestProcessor.parse_request(response_to_return.encode())

            # print("[Server] - Response : ", type(response_to_return_2))
            # print("[Server] - Response : ", response_to_return_2)

            p.packet_type = 2
            p.payload = ("SYN Recieved. Here is your SYN-ACK").encode()
            print("[Server] - SYN Recieved. Here is your SYN-ACK")

            conn.sendto(p.to_bytes(), sender)

        if (p.packet_type == 3):
            # print("[Server] - Payload : ", type(response_to_return))
            # print("[Server] - Payload : ", response_to_return)

            response_to_return_2 = RequestProcessor.parse_request(response_to_return.encode())

            # print("[Server] - Response : ", type(response_to_return_2))
            # print("[Server] - Response : ", response_to_return_2)

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

# handles directory change
RequestProcessor.setDirectory("data")
if(args.data):
    RequestProcessor.setDirectory(args.data)
if (args.verbose):
    RequestProcessor.setVerbose()
    


run_server(args.port)


