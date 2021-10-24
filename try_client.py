import select
import socket
import sys
import signal
import argparse
import queue
import ssl
import json

from utils import *
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal 

SERVER_HOST = 'localhost'

class ChatClient(QThread):
    """ A command line chat client using select """
    text_signal = pyqtSignal(object)
    usr_signal = pyqtSignal(object)
    def __init__(self, name, port, host=SERVER_HOST): 
        super().__init__()
        self.name = name
        self.connected = False
        self.host = host
        self.port = port
        self.inputs = []
        self.outputs = []
        self.userList = []
        self.msg_queue = queue.Queue()

        # send(self.sock, 'NAME: ' + self.name)
        # data = json.loads(receive(self.sock))
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

        # Initial prompt

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.sock = self.context.wrap_socket(self.sock, server_hostname=self.host)
            self.sock.connect((self.host, self.port))
            print(f'Now connected to chat server@ port {self.port}')
            self.connected = True
            self.inputs.append(self.sock)
            self.outputs.append(self.sock)
        except socket.error as e:
            print(f'Failed to connect to chat server @ port {self.port}')
            sys.exit(1)
    
    def handle_msg(self, msg):
        msg_dict = json.loads(msg)
        if msg_dict['type'] == "SYNC":
            self.userList = msg_dict['data']
            print(self.userList)
            self.usr_signal.emit(self.userList)
        elif msg_dict['type'] == "MSG":
            self.text_signal.emit(msg_dict['data'])

    def cleanup(self):
        """Close the connection and wait for the thread to terminate."""
        self.sock.close()

    def addData(self, msg_type, msg, data):
        send_msg = json.dumps({'type': msg_type, 'msg': msg, 'data': data})
        print(send_msg)
        self.msg_queue.put(send_msg)

    def run(self):
        """ Chat client main loop """
        while self.connected:
            try:
                # Wait for input from stdin and socket
                readable, writeable, exceptional = select.select(
                    self.inputs, self.outputs, [])

                for sock in readable:
                    data = receive(sock)
                    if data:
                        self.handle_msg(data)
                    else:
                        print('Client shutting down.')
                        self.connected = False
                        break
                    # print(self.sock)
                    # if sock == 0: ##client send data
                    #     data = sys.stdin.readline().strip()
                    #     print(data)
                    #     if data:
                    #         send(self.sock, data)
                    #     # else:
                    #     #     print("connection closed.")
                    #     #     self.client.inputs.remove(r)
                    #     #     exit(-1)
                    # elif sock == self.sock:
                    #     data = receive(self.sock)
                    #     print(data)
                    #     if not data:
                    #         print('Client shutting down.')
                    #         self.connected = False
                    #         break
                    #     else:
                    #         sys.stdout.write(data + '\n')
                    #         sys.stdout.flush()
                for w in writeable:
                    if not self.msg_queue.empty():
                        m = self.msg_queue.get_nowait()
                        send(w, m)
            except KeyboardInterrupt:
                print(" Client interrupted. """)
                self.cleanup()
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', action="store", dest="name", required=True)
    parser.add_argument('--port', action="store",
                        dest="port", type=int, required=True)
    given_args = parser.parse_args()

    port = given_args.port
    name = given_args.name

    client = ChatClient(name=name, port=port)
    client.connect()
    client.start()