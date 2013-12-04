__author__ = 'harry'


class GameInProgressException(Exception):
    def __init__(self):
        self.message = "Game is in progress"

class HostDisconnectedException(Exception):
    def __init__(self):
        self.message = "The host unexpectedly disconnected"

class NoConnectionException(Exception):
    def __init__(self):
        self.message = "No connection could be made"

class EndOfGame(Exception):
    def __init__(self, message):
        self.message = message