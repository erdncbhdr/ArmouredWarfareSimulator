__author__ = 'harry'

class GameInProgressException(Exception):
    def __init__(self):
        self.message = "Game is in progress"

class HostDisconnectedException(Exception):
    def __init__(self):
        self.message = "The host unexpectedly disconnected"