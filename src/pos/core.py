# coding: utf-8

# ========================================
# Poseidon 2 Core Module
# ========================================

import sys
import socket
import threading

from pos.base import *
from setting import *
from pos.thread import *

# Main Routine and User Management Class
class Core(Base):
    _setting = None
    _userManager = None
    _entityManager = None
    _listenerObject = None
    _listenerThread = None

    # Start Listening
    def __init__(self):
        # Message
        print('Poseidon 2 Ver. {}'.format(Setting().currentVersion))
        try:
            self._setting = Setting()
            self._listenerObject = ListenerThread(Setting().proxyAddress, ClientThread)
            self._listenerThread = threading.Thread(target = self._listenerObject.serve_forever)
            self._listenerThread.daemon = True
            self._listenerThread.start()
        except:
            self._message('Cannot start listening .')
        self._message('Listening started.')

    # Main Loop
    def run(self):
        while self.isRunning:
            pass

    # Messaging
    def _message(self, message):
        print('Poseidon: {}'.format(message))
