# coding: utf-8

# ========================================
# Poseidon 2 Thread Module
# ========================================

import socket
import threading
import socketserver

from pos.base import *
from setting import *
from pos.packet import *

# Listener Thread
class ListenerThread(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

# Connect to Client Thread
class ClientThread(socketserver.BaseRequestHandler, Base):
    _clientSocket = None
    _serverSocket = None
    _clientPacketStacker = None
    _serverPacketStacker = None
    _serverThread = None

    # Client Setting
    def setup(self):
        # Define
        self._clientSocket = self.request
        self._serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Launch Packet Stack
        self._clientPacketStacker = PacketStacker(self._clientSocket, self._serverSocket)
        self._serverPacketStacker = PacketStacker(self._serverSocket, self._clientSocket)
        # Connect to Server
        self._serverSocket.connect(Setting().serverAddress)
        self._serverThread = ServerThread(self._serverPacketStacker)
        self._serverThread.daemon = True
        self._serverThread.start()

    # Client Main Routine
    def handle(self):
        while self.isRunning() and self._clientPacketStacker.isRunning():
            self._clientPacketStacker.recieve()
            self._clientPacketStacker.send()

    # Close Process
    def finish(self):
        self._serverSocket.close()
        self._clientSocket.close()
        self._message('Client connection closed')

# Connect to Server Thread
class ServerThread(threading.Thread, Base):
    _serverSocket = None
    _clientSocket = None
    _packetStacker = None

    # Server Setting
    def __init__(self, packetStacker):
        super(ServerThread, self).__init__()
        # Launch Packet Stack
        self._packetStacker = packetStacker

    # Server Main Routine
    def run(self):
        while self.isRunning() and self._packetStacker.isRunning():
            self._packetStacker.recieve()
            self._packetStacker.send()
        self._message('Server connection closed')

# User Thread
class UserThread(threading.Thread, Base):
    pass
