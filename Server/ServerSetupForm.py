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
        thread = threading.Thread(target=self.startServerThread)
        thread.start()
        
    def stopServer(self,event):
        self.statusLab.SetLabel("No game instance running")
        try:
            self.server.shutdown()
            print("Server shutdown")
        except:
            print ("Server not running")
        
    def startServerThread(self):
        HOST = self.ipBox.Value
        PORT = int(self.portBox.Value)
        try:
            self.server = ThreadedTCPServer((HOST,PORT), Server.TankServer)
            print ("Server running on "+str(HOST)+":"+str(PORT))
            thread_server = threading.Thread(self.server.serve_forever())
            thread_server.daemon = True
            thread_server.start()
        except EndOfGame as ex:
            self.server.shutdown()
            messages.Info(self.parent, "Game has finished")
            self.statusLab.SetLabel("No game instance running")
            self.processEndOfGame(ex)
        except Exception as ex:
            #This is literally the only error that appears here
            print ("Port is not free")
            print ("Technical information: "+str(ex))

    def processEndOfGame(self, stats):
        conn = sqlite3.Connection("LoginDatabase")
        cur = conn.cursor()
        for player in stats:
            username = stats[-1]
            tankName = stats[-2]
            playerId = cur.execute("SELECT UserId FROM UserInfo WHERE Username = ?", [username]).fetchone()[0]
            currentXp = cur.execute()
        conn.close()
app = wx.App(False)

frame = serverForm(None)

frame.Show(True)

app.MainLoop()
