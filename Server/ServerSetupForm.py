#!/usr/bin/env python
# coding=utf-8

import wx
import threading
import SocketServer
import sys
import ServerGui
import Server
import loginServer
import os
import sys

sys.path.append(os.getcwd())
try:
    import wmi
except ImportError:
    #Unix system
    try:
        import netifaces
    except ImportError:
        None
from Errors import *
import messages
import sqlite3
import pickle


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
            
class serverForm(ServerGui.Mainframe):
    """Initialise the main GUI for server setup."""
    def __init__(self, parent):
        try:
            ServerGui.Mainframe.__init__(self,parent)
        except:
            print("GUI failed __init__")
        self.interfaceChoice.Clear()
        self.parent = parent
        self.opSys = self.getOperatingSystem()
        self.loginThread()

    def loginThread(self):
        loginServer.main()

    def getOperatingSystem(self):
        try:
            self.testval = sys.winver
            #No exception thrown, we must be on windows
            for nic in wmi.WMI ().Win32_NetworkAdapterConfiguration (IPEnabled=1):
                self.interfaceChoice.Append(nic.caption[11:])
            return "Win"
        except AttributeError:
            #We're running on unix system
            for ifaceName in netifaces.interfaces():
                self.interfaceChoice.Append(ifaceName)
            return "Unix"
    def changeInterface(self,event):
        if self.opSys ==  "Unix":
            ints = netifaces.interfaces()
            selected_int = ints[self.interfaceChoice.GetCurrentSelection()]
            try:
                self.ipBox.Value = netifaces.ifaddresses(selected_int)[2][0]['addr']
            except Exception:
                self.ipBox.Value = "Not connected"
        elif self.opSys == "Win":
            ints = [nic for nic in wmi.WMI ().Win32_NetworkAdapterConfiguration (IPEnabled=1)]
            self.ipBox.Value = ints[self.interfaceChoice.GetCurrentSelection()].IPAddress[0]

    def startServer(self,event):
        self.statusLab.SetLabel("Game instance is running")
        self.startServerThread()
        f = open("Stats.dat", "r")
        ex = pickle.load(f)
        messages.Info(self.parent, "Game has finished")
        self.statusLab.SetLabel("No game instance running")
        try:
            self.processEndOfGame(ex)
        except Exception:
            #No stats to process
            pass
        
    def stopServer(self,event):
        self.statusLab.SetLabel("No game instance running")
        try:
            self.server.shutdown()
            print("Server shutdown")
        except Exception:
            print ("Server not running")

    def beginTheSatanHailing(self):
        while True:
                a =self.server.handle_request()
                #All glory to overlord satan
                print str(a)
        
    def startServerThread(self):
        HOST = self.ipBox.Value
        PORT = int(self.portBox.Value)
        try:
            self.server = SocketServer.ThreadingTCPServer((HOST,PORT), Server.TankServer)
            self.endEvent = threading.Event()
            Server.TankServer.Event = self.endEvent
            print ("Server running on "+str(HOST)+":"+str(PORT))
            serverThread = threading.Thread(target=self.beginTheSatanHailing)
            #serverThread.setDaemon(False)
            serverThread.start()
        except Exception as ex:
            #This is literally the only error that appears here
            print ("Port is not free")
            print ("Technical information: "+str(ex))


    def processEndOfGame(self, stats):
        conn = sqlite3.Connection("LoginDatabase")
        cur = conn.cursor()
        print "Running update on data: " + str(stats)
        for player in stats:
            print "Update info: " + str(player)
            username = stats[-1]
            tankName = stats[-2]
            xpGained = stats[2]
            print "Got stats needed"
            playerId = cur.execute("SELECT UserId FROM UserInfo WHERE Username = ?", [username]).fetchone()[0]
            currentXp = int(cur.execute("SELECT "+tankName+" UserProgress WHERE UserId  = ?", [player]).fetchone()[0])
            print "Init sql queries done"
            currentXp += xpGained
            cur.execute("UPDATE UserProgress SET "+tankName+" = ? WHERE UserId = ?", [currentXp, playerId])
            print "UPDATED ID "+str(playerId)+" TO XP "+str(currentXp)
        conn.commit()
        conn.close()
        os.remove("Stats.dat")
app = wx.App(False)

frame = serverForm(None)

frame.Show(True)

app.MainLoop()
