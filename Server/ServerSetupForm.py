import wx
import ServerGui
import threading
import netifaces
import sqlite3
import SocketServer
import Server
import sys
import loginServer
try:
    import wmi
except ImportError:
    #Unix system
    None
global conn

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
        self.opSys = self.getOperatingSystem()
        LoginThread = threading.Thread(target=self.loginThread)
        LoginThread.start()

    def loginThread(self):
        loginServer.main()

    def getOperatingSystem(self):
        try:
            self.testval=sys.winver
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
        #self.statusLab.Label = "Server running"
        HOST = self.ipBox.Value
        PORT = int(self.portBox.Value)
        try:
            self.server = ThreadedTCPServer((HOST,PORT), Server.TankServer)
            print ("Server running on "+str(HOST)+":"+str(PORT))
            thread_server = threading.Thread(self.server.serve_forever())
            thread_server.daemon = True
            thread_server.start()
            conn = sqlite3.Connection("LoginDatabase")
            cur = conn.cursor()
            Server.TankServer.giveDatabaseConnection(cur)
        except Exception as ex:
            print ("Port is not free")
            print ("Technical information: "+str(ex))
            
app = wx.App(False)

frame = serverForm(None)

frame.Show(True)

app.MainLoop()
