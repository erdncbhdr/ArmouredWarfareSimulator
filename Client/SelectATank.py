#!/usr/bin/env python

import wx
import selectGui
import sqlite3
import os
import messages
import pickle
import netComms

def getConfiguration(conf, keyword):
    for a in conf:
        if keyword in a and "#" not in a:
            toRet = a.split("=")
            print toRet
            return toRet[1]

class Buy(selectGui.TankBuy):
    def __init__(self, parent):
        selectGui.TankBuy.__init__(self, parent)

class Upgrade(selectGui.UpgradeForm):
    def __init__(self, parent, tank, xp, username):
        selectGui.UpgradeForm.__init__(self, parent)
        #For reference
        self.username = username
        self.parent = parent
        self.name = tank[0]
        self.hp = tank[1]
        self.damage = tank[2]
        self.penetration = tank[3]
        self.reload = tank[4]
        self.armour = tank[5]
        self.hullTraverse = tank[6]
        self.turretTraverse = tank[7]
        self.speed = tank[8]
        #Progress is in form XP for each tank
        self.xp = int(xp)

        self.populateBoxes()
    def populateBoxes(self):
        self.tankL.SetLabel(self.name)
        self.xpL.SetLabel("XP to spend: "+ str(self.xp))
        self.curHP.SetValue(str(self.hp))
        self.curDam.SetValue(str(self.damage))
        self.curArm.SetValue(str(self.armour))
        self.curPen.SetValue(str(self.penetration))
        self.curHTra.SetValue(str(self.hullTraverse))
        self.curTTra.SetValue(str(self.turretTraverse))
        self.curSpe.SetValue(str(self.speed))
        self.curRel.SetValue(str(self.reload))

    def upHP( self, event ):
        if self.xp >= 10:
            self.xp -= 10
            self.hp += 5
            self.populateBoxes()

    def upDam( self, event ):
        if self.xp >= 10:
            self.xp -= 10
            self.damage += 5
            self.populateBoxes()

    def upArm( self, event ):
        if self.xp >= 10:
            self.xp -= 10
            self.armour += 3
            self.populateBoxes()

    def upPen( self, event ):
        if self.xp >= 10:
            self.xp -= 10
            self.penetration += 3
            self.populateBoxes()

    def upHTr( self, event ):
        if self.xp >= 10:
            self.hullTraverse += 0.2
            self.xp -= 10
            self.populateBoxes()

    def upTTra( self, event ):
        if self.xp >= 10:
            self.xp -= 10
            self.turretTraverse += 0.2
            self.populateBoxes()

    def upRel( self, event ):
        if self.xp >= 10:
            self.xp -= 10
            self.reload -= 3
            self.populateBoxes()

    def upSp( self, event ):
        if self.xp >= 10:
            self.xp -= 10
            self.speed += 0.1
            self.populateBoxes()

    def confirmEdit( self, event ):
        r = open("login.conf", "r")
        config = r.read().split("\n")
        self.ipAddr  = getConfiguration(config, "ip_address")
        self.port = getConfiguration(config, "port")
        r.close()
        conn = netComms.networkComms(self.ipAddr, self.port)
        toSend = ["Update", self.username]
        toSend.append(self.tank)
        toSend.append(self.xp)
        if messages.YesNo(self.parent, "Confirm changes?"):
            conn.send(pickle.dumps(toSend))
            messages.Info(self.parent, "Changes sent.")
            self.Show(False)
        else:
            pass

    def cancelEdit( self, event ):
        self.Show(False)


class Main(selectGui.MainFrame):
    def __init__(self, parent, username, xp, owned):
        selectGui.MainFrame.__init__(self, parent)
        self.conn = sqlite3.Connection("TankStats.db")
        self.cur = self.conn.cursor()
        #Variables passed from the login form
        self.username = username
        self.progress = xp
        self.owned = owned
        #Pull up all known tanks
        self.tanks = self.cur.execute("SELECT * FROM Tanks;").fetchall()
        #We only want the tanks that we own
        print "TANKS: "+str(self.tanks)
        print "OWNED: "+str(self.owned)
        for i in range(len(owned)-1, 0, -1):
            if owned[i] == 0:
                print i
                self.tanks.pop(i)

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

    def getStats(self, username, tankName):
        r = open("login.conf", "r")
        config = r.read().split("\n")
        self.ipAddr  = getConfiguration(config, "ip_address")
        self.port = getConfiguration(config, "port")
        r.close()
        conn = netComms.networkComms(self.ipAddr, self.port)
        conn.send(pickle.dumps(["GET", username, tankName]))
        return pickle.loads(conn.recieved).split("/")[:-1]

    def doStats(self,  event):
        self.sel = self.tankChoice.GetCurrentSelection()
        self.tank = self.tanks[self.sel]
        self.stats = self.getStats(self.username, self.tank[0])
        self.statsBox.Value = ("HP: "+str(self.tank[1]) +
                                            "\nDamage (HP average): "+str(self.stats[2])+
                                            "\nPenetration (mm): "+ str(self.stats[3])+
                                            "\nReload (ticks): "+str(self.stats[4])+
                                            "\nArmour (mm):" + str(self.stats[5])+
                                            "\nHull Traverse Speed: "+str(self.stats[6])+
                                            "\nTurret Traverse Speed: "+str(self.stats[7])+
                                            "\nSpeed: "+str(self.stats[8]))
        self.name = self.tanks[self.sel][1]

    def doBuy( self, event ):
        buyApp = wx.App(False)
        buyFrame = Buy(None)
        buyFrame.Show(True)
        buyApp.MainLoop()

    def doUpgrade( self, event ):
        upApp = wx.App(False)
        upFrame = Upgrade(None, self.tank, self.progress[self.tankChoice.GetSelection()], self.username)
        upFrame.Show(True)
        upApp.MainLoop()

        
def main(username, xp, owned):
    app = wx.App(False)
    frame = Main(None, username, xp, owned)
    frame.Show(True)
    app.MainLoop()

