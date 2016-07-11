# coding: utf-8

# ========================================
# Poseidon 2 Settings
# ========================================

from pos.base import *

# Settings
class Setting(Base, Singleton):
    # Current Version
    currentVersion = '0.5'

    # Poseidon's IP and Port
    proxyAddress = ('', 50005)
    # YSFLIGHT's IP and Port
    serverAddress = ('localhost', 7915)
