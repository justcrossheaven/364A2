import select
import socket
import sys
import signal
import argparse
import json
import queue
import ssl

from utils import *

SERVER_HOST = 'localhost'


class ChatServer(object):
    """ An example chat server using select """

    def __init__(self, port, backlog=5):
        self.clients = 0
        self.clientmap = [[],[]] # 0 for socket, 1 for name
        self.inputs = []
        self.outputs = []  # list output sockets
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain(certfile="cert.pem", keyfile="cert.pem")
        self.context.load_verify_locations('cert.pem')
        self.context.set_ciphers('AES128-SHA')
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        self.server.listen(backlog)
        self.msg_queues = {}
        self.chatroom = [] # [['john','lol','what the fuck'], ['sda', 'sdaad', 'asda']]
        # Catch keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)
        self.inputs.append(self.server)
        self.inputs.append(sys.stdin)

        print(f'Server listening to port: {port} ...')

    def sighandler(self, signum, frame):
        """ Clean up client outputs"""
        print('Shutting down server...')

        # Close existing client sockets
        for output in self.outputs:
            output.close()

        self.server.close()
    
    def construct_msg(self, msg_type, msg, data):
        return json.dumps({'type': msg_type, 'msg': msg, 'data': data})

    def sync_data(self):
        for user_name in self.clientmap[1]:
            group_index = []
            group_all = []
            group_member = []
            for group in self.chatroom:
                group_all.append(self.chatroom.index(group))
                group_member.append(group)
                if user_name in group:
                    group_index.append(self.chatroom.index(group))
            data = {'groups': group_index, 'users': self.clientmap[1], 'groupsall': group_all, 'group_mem':self.chatroom}
            msg = self.construct_msg('SYNC', '', data)
            send_sock = self.clientmap[0][self.clientmap[1].index(user_name)]
            self.msg_queues[send_sock].put(msg)
    
    def handle_msg(self, msg, sock):
        msg_dict = json.loads(msg)
        if msg_dict['type'] == "NEW_USR":
            name = msg_dict['data']
            self.clientmap[1].append(name)
            self.clientmap[0].append(sock)
            self.sync_data()
        elif msg_dict['type'] == "JOIN":
            data = msg_dict['data']
            index = data['ind']
            name = data['name']
            if msg_dict['msg'] == 'CREATE':
                self.chatroom.append([name])
            elif msg_dict['msg'] == 'JOIN':
                self.chatroom[index].append(name)
            self.sync_data()
        elif msg_dict['type'] == "MSG":
            data = msg_dict['data']
            if data['msg_to'] in self.clientmap[1]:
                send_to_data = {
                    'msg_from': self.clientmap[1][self.clientmap[0].index(sock)],
                    'msg': data['msg']
                }
                msg = self.construct_msg('MSG', '', send_to_data)
                send_to_sock = self.clientmap[0][self.clientmap[1].index(data['msg_to'])]
                self.msg_queues[send_to_sock].put(msg)
            else:
                index = data['msg_to']
                send_to_data = {
                    'msg_from': index,
                    'user': self.clientmap[1][self.clientmap[0].index(sock)],
                    'msg': data['msg']
                }
                msg = self.construct_msg('MSG', '', send_to_data)
                for user in self.chatroom[index]:
                    send_to_sock = self.clientmap[0][self.clientmap[1].index(user)]
                    self.msg_queues[send_to_sock].put(msg)

            

    def get_client_name(self, client):
        """ Return the name of the client """
        info = self.clientmap[str(client)]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def run(self):
        while True:
            try:
                readable, writeable, exceptional = select.select(self.inputs, self.outputs, [])
            except select.error as e:
                print("is this an error??")
                break
            for sock in readable:
                if sock == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    print(
                        f'Chat server: got connection {client.fileno()} from {address}')
                    # Read the login name
                    print("this is very weird")
                    self.inputs.append(client)
                    self.outputs.append(client)
                    self.clients += 1
                    self.msg_queues[client] = queue.Queue()
                    print("the if statement is over")
                else:
                    # handle all other sockets
                    print("does this entered???")
                    try:
                        data = receive(sock)
                        if data:
                            self.handle_msg(data, sock)
                        else:
                            print(f'Chat server: {sock.fileno()} hung up')
                            self.clients -= 1
                            sock.close()
                            self.inputs.remove(sock)
                            self.outputs.remove(sock)
                            index = self.clientmap[0].index(sock)
                            name = self.clientmap[1][index]
                            self.clientmap[0].remove(self.clientmap[0][index])
                            self.clientmap[1].remove(self.clientmap[1][index])
                            for chatroom in self.chatroom:
                                if name in chatroom:
                                    chatroom.remove(name)
                                if len(chatroom) == 0:
                                    self.chatroom.remove(chatroom)
                            self.sync_data()
                            # # Sending client leaving information to others
                            # msg = f'\n(Now hung up: Client from {self.get_client_name(sock)})'

                            # for output in self.outputs:
                            #     send(output, msg)
                    except socket.error as e:
                        # Remove
                        self.inputs.remove(sock)
                        self.outputs.remove(sock)   
            for w in writeable:
                if not self.msg_queues[w].empty():
                    data = self.msg_queues[w].get_nowait()
                    send(w, data)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Socket Server Example with Select')
    parser.add_argument('--name', action="store", dest="name", required=True)
    parser.add_argument('--port', action="store",
                        dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    name = given_args.name

    server = ChatServer(port)
    server.run()
