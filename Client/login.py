import hashlib
import os
import sys

import wx

import games
import loginGui
import netComms
import messages
import SelectATank
from Errors import *


def getConfiguration(conf, keyword):
    for a in conf:
        if keyword in a and "#" not in a:
            toRet = a.split("=")
            return toRet[1]


class NewAccountForm(loginGui.newAccount):
    """A class to handle the account creation screen"""

    def __init__(self, parent):
        loginGui.newAccount.__init__(self, parent)
        self.parent = parent

    def createAccount(self, event):
        """Asks the login server to add the account"""
        #Open the config
        try:
            r = open("login.conf", "r")
        except IOError:
            messages.Warn("Could not open login.conf from directory %s", str(os.getcwd()))
            sys.exit()

        config = r.read().split("\n")

        #This is stored in the config file
        self.ipAddr = getConfiguration(config, "ip_address")
        self.port = getConfiguration(config, "port")

        r.close()
        if len(self.passB.Value) < 5:
            messages.Warn(self.parent, "Passwords must be at least 5 characters long")
        elif self.userBox.Value != "" and self.passB.Value != "":
            conn = netComms.networkComms(self.ipAddr, self.port)
            conn.send(["CREATE", [self.userBox.Value.lower(), hashlib.sha1(self.passB.Value).hexdigest()]])
            self.process(conn.recieved)
            conn.close()
        else:
            #show a warning
            messages.Warn(self.parent, "Please enter both a username and password to create an account")

    def process(self, message):
        """Processes the server response"""
        if message == "UsernameException":
            messages.Info(self.parent, "That username is in use. Please choose another.")
        if message == "LoginFailure":
            messages.Warn(self.parent, "Login failed. Wrong username/password.")
        if message == "COMPLETE":
            messages.Info(self.parent, "Account created. Please log in.")
            self.Show(False)
        if type((0, 0)) == type(message):
            self.loginComplete(message)


class LoginForm(loginGui.MainFrame):
    """A class to handle the main login GUI"""

    def __init__(self, parent):
        loginGui.MainFrame.__init__(self, parent)
        self.parent = parent
        self.readConfig()
        self.a = games.load_sound("res/Sounds/WoT-Main-Theme.ogg")
        self.a.play()

    def readConfig(self):
        """Reads the configuration file for ip address and port"""

        #the client will provide a configuration file
        try:
            r = open("login.conf", "r")
        except IOError:
            thing = str("Could not locate login.conf in directory {0}".format(str(os.getcwd())))
            messages.Warn(self.parent, thing)
            sys.exit([7])

        config = r.read().split("\n")
        self.ipAddr = getConfiguration(config, "ip_address")
        self.port = getConfiguration(config, "port")
        r.close()

    def suchSending(self, event):
        """Send the login credentials to the server"""
        try:
            self.conn = netComms.networkComms(self.ipAddr, self.port)
            self.conn.send(["LOGIN", [self.userBox.Value.lower(), hashlib.sha1(self.passBox.Value).hexdigest()]])

        except NoConnectionException:
            thing = "Could not connect to login server at {0}".format(str(self.ipAddr) + ":" + str(self.port))
            messages.Warn(self.parent, thing)
            sys.exit([7])
        recv = self.conn.recieved
        self.conn.close()
        self.process(recv)

    def soClear(self, event):
        """Clear the username/password boxes"""
        self.userBox.Value = ""
        self.passBox.Value = ""

    def doCreate(self, event):
        """Start the creation window"""
        appyapp = wx.App(False)
        framey = NewAccountForm(None)
        framey.Show(True)
        appyapp.MainLoop()

    def process(self, message):
        """Process the server's response"""
        if message == "UsernameException":
            messages.Info(self.parent, "That username is in use. Please choose another.")
        if message == "LoginFailure":
            messages.Warn(self.parent, "Login failed. Wrong username/password.")
        if message == "COMPLETE":
            messages.Info(self.parent, "Account created. Please log in.")
        if type((0, 0)) == type(message):
            self.loginComplete(message)

    def loginComplete(self, message):
        """Server has logged us in, proceed to next screen"""
        username = str(message[0])
        progressXPs = message[2:9]
        owned = message[10:]
        self.Show(False)
        self.a.stop()
        while True:
            try:
                SelectATank.main(username, progressXPs, owned)
            except Exception as ex:
                import sys
                sys.exit()


def startLogin():
    """The main method for starting the GUI"""
    app = wx.App(False)
    frame = LoginForm(None)
    frame.Show(True)
    app.MainLoop()
