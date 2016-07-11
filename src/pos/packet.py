# coding: utf-8

# ========================================
# Poseidon 2 Packet Module
# ========================================

import socket
import struct

from pos.base import *
from setting import *

# Packet Structure
class Packet:
    _payload = None
    _type = None
    _length = None

    # Packet Setting
    def __init__(self, packetType, packetPayload, packetFormat = None):
        if not packetFormat:
            self._payload = packetPayload
        else:
            self._payload = struct.pack(packetFormat, *packetPayload)
        self._type = packetType
        self._length = len(packetPayload)

    # Getting Packet Type
    def getType(self):
        return self._type

    # Getting Packet Payload
    def getPayload(self, packetFormat = None, packetLength = None):
        if not packetFormat and not packetLength:
            return self._payload
        elif not packetLength:
            return struct.unpack(packetFormat, self._payload)
        else:
            return struct.unpack(packetFormat, self._payload[0:packetLength])

    # Getting Packet Stream
    def getPacket(self):
        return struct.pack('II{}s'.format(self._length), self._length + 4, self._type, self._payload)

# Packet Stack Class
class PacketStacker(Base):
    _selfSocket = None
    _otherSocket = None
    _packetStack = []

    # Initialize
    def __init__(self, selfSocket, otherSocket):
        # Setting Socket
        self._selfSocket = selfSocket
        self._otherSocket = otherSocket

    # Recieving Stream
    def recieve(self):
        if self.isRunning():
            self._packetStack.clear()
            packetBuffer = self._selfSocket.recv(8192)
            bufferLength = len(packetBuffer)
            offset = 0
            while True:
                # Null Stream
                if not bufferLength:
                    self._message('Packet is null! Exiting.')
                    self.stop()
                    break
                # Until End Of Stream
                elif bufferLength > offset:
                    # Packing Packet
                    try:
                        packetLength = struct.unpack('H', packetBuffer[offset:offset + 2])[0]
                        packetType = struct.unpack('I', packetBuffer[offset + 4:offset + 8])[0]
                        packetPayload = packetBuffer[offset + 8:offset + 8 + packetLength]
                        self._packetStack.append(Packet(packetType, packetPayload))
                        offset += packetLength + 4
                    # Junk Packet
                    except:
                        self._message('Recieved Packet Lossed.')
                        self._packetStack.clear()
                        offset = bufferLength
                # End Of Stream
                elif bufferLength == offset:
                    break
            # Is not packet lossed?
            if not len(self._packetStack):
                self.recieve()
        else:
            self._message('Stopped.')

    # Sending Stream
    def send(self):
        try:
            packetStream = b''
            if self.isRunning():
                for packet in self._packetStack:
                    packetStream += packet.getPacket()
                while not self._otherSocket.send(packetStream) == len(packetStream):
                    self._message('Sended Packet lossed.')
            else:
                self._message('Stopped.')
        except:
            self._message('Packet sending failed.')
            self.stop()

    # Getting Stack
    def getStack(self):
        return self._packetStack

    # Adding Stack
    def addStack(self, packet):
        self._packetStack.append(packet)

    # Deleting Stack
    def delStack(self, packet):
        self._packetStack.remove(packet)
