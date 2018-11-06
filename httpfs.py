import socket
import threading
import RequestProcessor
import argparse
from packet import Packet


def run_server(port):
    print("Server RUnning!")
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        conn.bind(('', port))
        print('Echo server is listening at', port)
        while True:
            data, sender = conn.recvfrom(1024)
            handle_client(conn, data, sender)

    finally:
        conn.close()


def handle_client(conn, data, sender):
    try:
        p = Packet.from_bytes(data)
        print("Router: ", sender)
        print("Packet: ", p)

        # TODO Try to send to RequestProcess here?
        
        response_to_return = p.payload.decode("utf-8")

        
        print("PacketType : ", p.packet_type)
        print("Payload : ", type(response_to_return))
        print("Payload : ", response_to_return)
        # Type returned is a string!


        response_to_return_2 = RequestProcessor.parse_request(response_to_return.encode())
        print("Response : ", type(response_to_return_2))
        print("Response : ", response_to_return_2)
        # Type returned is a string?
        p.payload = (response_to_return_2).encode()
        # TODO send payload to RequestProcces
        # problem here?

        # How to send a reply.
        # The peer address of the packet p is the address of the client already.
        # We will send the same payload of p. Thus we can re-use either `data` or `p`.
        conn.sendto(p.to_bytes(), sender)

    except Exception as e:
        print("Error: ", e)

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


