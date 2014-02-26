__author__ = 'harry'


class GameInProgressException(Exception):
    """Is called when a player tries to joina game in progress"""
    def __init__(self):
        self.message = "Game is in progress"

class HostDisconnectedException(Exception):
    """Called if the host goes offline"""
    def __init__(self):
        self.message = "The host unexpectedly disconnected"

class NoConnectionException(Exception):
    """Called if there is no connection to the server"""
    def __init__(self):
        self.message = "No connection could be made"

class EndOfGame(Exception):
    """Called to end the game"""
    def __init__(self, message):
        self.message = message

class AHHHHHHHHHHH(Exception):
    """OH GOD SOMETHING BAD HAPPENED HALP"""
    def __init__(self, message):
        self.message = message
