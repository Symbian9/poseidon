# coding: utf-8

# ========================================
# Poseidon 2 Base Classes
# ========================================

# Base Class
class Base():
    _running = True

    # Is Running?
    def isRunning(self):
        return self._running

    # Stopping Running
    def stop(self):
        self._running = False

    # Messaging
    def _message(self, message):
        print('[{}]{}'.format(self.__class__.__name__, message))

# Singleton Class
class Singleton(object):
    _instance = None

    # Singleton
    def __new__(this, *argarray, **argdict):
        if this._instance is None:
            this._instance = object.__new__(this, *argarray, **argdict)
        return this._instance
