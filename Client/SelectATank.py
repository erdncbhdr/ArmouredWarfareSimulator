#!/usr/bin/env python

import wx
import selectGui
import sqlite3
import os

class Main(selectGui.MainFrame):
    def __init__(self, parent):
        selectGui.MainFrame.__init__(self,parent)
        self.conn = sqlite3.Connection("TankStats.db")
        self.cur = self.conn.cursor()
        self.tanks = self.cur.execute("SELECT * FROM Tanks;").fetchall()
        self.conn.close()
        self.tankChoice.Clear()
        for i in range(len(self.tanks)):
            self.tankChoice.Append(self.tanks[i][0])
    def goToBattle(self,  event):
        import TankClient
        inst = TankClient.main(self.tank,  self.host,  self.port)
        
    def setHost(self,  event):
        try:
            hostPort = self.AddressBox.Value.split(":")
            self.host = hostPort[0]
            self.port = hostPort[1]
        except Exception:
            pass
    def doStats(self,  event):
        self.sel = self.tankChoice.GetCurrentSelection()
        self.tank = self.tanks[self.sel]
        self.statsBox.Value = ("HP: "+str(self.tank[1]) +
                                            "\nDamage (HP average): "+str(self.tank[2])+
                                            "\nPenetration (mm): "+ str(self.tank[3])+
                                            "\nReload (ticks): "+str(self.tank[4])+
                                            "\nArmour (mm):" + str(self.tank[5])+
                                            "\nHull Traverse Speed: "+str(self.tank[6])+
                                            "\nTurret Traverse Speed: "+str(self.tank[7])+
                                            "\nSpeed: "+str(self.tank[8]))
        self.name = self.tanks[self.sel][1]
        
def main():
    app = wx.App(False)
    frame = Main(None)
    frame.Show(True)
    app.MainLoop()

main()
