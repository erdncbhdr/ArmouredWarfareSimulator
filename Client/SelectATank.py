#!/usr/bin/env python

import sqlite3

import wx
from pygame import *

import selectGui
import messages
import Errors
import netComms
import games
from Errors import *


def getConfiguration(conf, keyword):
    for a in conf:
        if keyword in a and "#" not in a:
            toRet = a.split("=")
            return toRet[1]


class Buy(selectGui.TankBuy):
    def __init__(self, parent, username, xp, alltanks, owner):
        selectGui.TankBuy.__init__(self, parent)
        self.username = username
        self.alltanks = alltanks
        self.xp = xp
        self.populate()
        self.parent = parent
        self.owner = owner

    def populate(self):
        self.xpBox.SetValue("Select a tank to see XP")
        self.TankBox.SetValue("Select a tank")
        r = open("login.conf", "r")
        config = r.read().split("\n")
        self.ipAddr = getConfiguration(config, "ip_address")
        self.port = getConfiguration(config, "port")
        r.close()
        conn = netComms.networkComms(self.ipAddr, int(self.port))
        conn.send(["OWNED", self.username])
        owned = conn.recieved
        conn.close()
        relaventOwned = owned[1:-2]
        dataconn = sqlite3.Connection("TankStats.db")
        cursor = dataconn.cursor()
        tankname = cursor.execute("SELECT name FROM Tanks;").fetchall()
        tankname = [x[0] for x in tankname]
        dataconn.close()
        conn = netComms.networkComms(self.ipAddr, int(self.port))
        conn.send(["COSTS"])
        self.costs = conn.recieved
        conn.close()
        self.TankBox.Clear()
        for i in range(len(tankname)):
            if relaventOwned[i] == 0:
                self.TankBox.Append(str(tankname[i]))

    def changeTankPrice(self, event):
        self.name = self.TankBox.GetValue()
        tankvalue = self.alltanks.index(self.name)
        self.xpBox.SetValue(str(self.xp[tankvalue - 1]))
        self.priceBox.SetValue(str(self.costs[tankvalue]))

    def buyTank(self, event):
        if int(self.xpBox.Value) >= int(self.priceBox.Value):
            try:
            # buy the tank
                assert (self.TankBox.GetSelection() >= 0)
                conn = netComms.networkComms(self.ipAddr, int(self.port))
                pastTank = self.alltanks[self.alltanks.index(self.name) - 1]
                conn.send(["BUY", self.name, self.username, pastTank])
                a = conn.recieved
                conn.close()
                if a == "DONE":
                    messages.Info(self.parent, "Tank purchased!")
                    self.owner.refresh(self.owner.username)
            except AssertionError:
                messages.Warn(self.parent, "Please select a tank first")
        else:
            messages.Warn(self.parent, "You do not have the XP to purchase this tank")
            self.owner.refresh(self.owner.username)
            self.Show(False)

    def cancel(self, event):
        self.owner.refresh(self.owner.username)
        self.Show(False)


class Upgrade(selectGui.UpgradeForm):
    def __init__(self, parent, tank, xp, username, form):
        selectGui.UpgradeForm.__init__(self, parent)
        #For reference
        self.form = form
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
        self.xpL.SetLabel("XP to spend: " + str(self.xp))
        self.curHP.SetValue(str(self.hp))
        self.curDam.SetValue(str(self.damage))
        self.curArm.SetValue(str(self.armour))
        self.curPen.SetValue(str(self.penetration))
        self.curHTra.SetValue(str(self.hullTraverse))
        self.curTTra.SetValue(str(self.turretTraverse))
        self.curSpe.SetValue(str(self.speed))
        self.curRel.SetValue(str(self.reload))

    def upHP(self, event):
        if self.xp >= 10:
            self.xp -= 10
            self.hp += int(1000 / self.hp)
            self.populateBoxes()

    def upDam(self, event):
        if self.xp >= 10:
            self.xp -= 10
            self.damage += int(300 / self.damage)
            self.populateBoxes()

    def upArm(self, event):
        if self.xp >= 10:
            self.xp -= 10
            self.armour += int(300 / self.armour)
            self.populateBoxes()

    def upPen(self, event):
        if self.xp >= 10:
            self.xp -= 10
            self.penetration += int(450 / self.penetration)
            self.populateBoxes()

    def upHTr(self, event):
        if self.xp >= 10:
            self.hullTraverse += (5 / self.hullTraverse)
            self.xp -= 10
            self.populateBoxes()

    def upTTra(self, event):
        if self.xp >= 10:
            self.xp -= 10
            self.turretTraverse += (5 / self.turretTraverse)
            self.populateBoxes()

    def upRel(self, event):
        if self.xp >= 10:
            self.xp -= 10
            self.reload -= int(self.reload / 20)
            self.populateBoxes()

    def upSp(self, event):
        if self.xp >= 10:
            self.xp -= 10
            self.speed += int(3 / self.speed)
            self.populateBoxes()

    def convertToString(self, lst):
        a = ""
        for b in lst:
            a += str(b) + ":"
        return a

    def getNewStats(self):
        statList = [self.name, self.hp, self.damage, self.penetration, self.reload,
                    self.armour, self.hullTraverse, self.turretTraverse, self.speed]
        a = self.convertToString(statList)
        return a

    def confirmEdit(self, event):
        r = open("login.conf", "r")
        config = r.read().split("\n")
        self.ipAddr = getConfiguration(config, "ip_address")
        self.port = getConfiguration(config, "port")
        r.close()
        conn = netComms.networkComms(self.ipAddr, int(self.port))
        toSend = ["Update", self.username]
        toSend.append(self.getNewStats())
        toSend.append(self.xp)
        if messages.YesNo(self.parent, "Confirm changes?"):
            conn.send(toSend)
            #print "Sent: " + str(toSend)
            messages.Info(self.parent, "Changes sent.")
            conn.close()
            #print "Closed connection to loginserver"
            self.Show(False)
        else:
            pass

    def cancelEdit(self, event):
        self.Show(False)


class Main(selectGui.MainFrame):
    def __init__(self, parent, username, xp, owned):
        selectGui.MainFrame.__init__(self, parent)
        self.a = games.load_sound("res/Sounds/WoT-Garage.ogg")
        self.a.play()
        self.conn = sqlite3.Connection("TankStats.db")
        self.cur = self.conn.cursor()
        #Variables passed from the login form
        self.username = username
        self.progress = xp
        self.parent = parent
        self.owned = owned

        #Set up config
        r = open("login.conf", "r")
        config = r.read().split("\n")
        self.ipAddr = getConfiguration(config, "ip_address")
        self.port = getConfiguration(config, "port")
        r.close()
        #Pull up all known tanks
        self.tanks = self.cur.execute("SELECT * FROM Tanks;").fetchall()
        self.allTanks = self.tanks
        #We only want the tanks that we own
        for i in range(len(owned) - 1, 0, -1):
            if owned[i] == 0:
                self.tanks.pop(i)

        self.conn.close()
        self.tankChoice.Clear()
        for i in range(len(self.tanks)):
            self.tankChoice.Append(self.tanks[i][0])

            self.refresh(self.username)

    def toInt(self, lst):
        for i in range(len(lst)):
            try:
                lst[i] = float(lst[i])
            except Exception:
                pass
        return lst

    def battleThread(self, instance):
        import TankClient
        #TankClient.setupEnv()
        a = TankClient.mainGame(instance)
        return a

    def goToBattle(self, event):
        try:
            self.a.stop()
        except Exception:
            pass
        try:
            assert (self.AddressBox.GetValue() != u"")
            assert (self.tankChoice.GetSelection() >= 0)
            instance = [self.username, self.toInt(self.stats), self.host, self.port]
            #self.Show(False)
            try:
                a = self.battleThread(instance)
            except error as e:
                #TankClient.setupEnv()
                print str(e)
            except games.GamesError as ex:
                games.screen.quit()
                print "Error with pygame: " + str(ex)
        except AssertionError:
            messages.Warn(self.parent, "Please select a tank and enter a host:port combo")

        except EndOfGame as ex:
            #print "EX:" + str(ex.message)
            ex = eval(ex.message)
            self.Show(True)
            win = ex[0]
            xp = ex[1]
            damage = ex[2]
            kills = ex[3]
            if win:
                messages.Info(self.parent, "You have won!\nYou recieved: " + str(xp) + " xp\nDamage dealt: " + str(
                    damage) + " Kills: " + str(kills),
                              "VICTORY")
            else:
                messages.Info(self.parent,
                              "You have been defeated...\nYou recieved: " + str(xp) + " xp\nDamage dealt: " + str(
                                  damage) + " Kills: " + str(kills),
                              "DEFEAT")
            #self.Show(False)
            #del(a)
            #quit()

            #except Exception as e:
            #    messages.Warn(self.parent, "Something went wrong. Exiting.\nError: "+str(e))
            #    sys.exit()

    def setHost(self, event):
        try:
            hostPort = self.AddressBox.Value.split(":")
            self.host = hostPort[0]
            self.port = hostPort[1]
        except Exception:
            pass

    def getStats(self, username, tankName):
        conn = netComms.networkComms(self.ipAddr, int(self.port))
        conn.send(["GET", username, tankName])
        a = (conn.recieved)
        conn.close()
        #print self.tankChoice.GetSelection()
        return a.split(":")


    def doStats(self, event):
        self.sel = self.tankChoice.GetString(self.tankChoice.GetSelection())
        #print "SEL " + self.sel
        self.stats = self.getStats(self.username, self.sel)
        self.statsBox.Value = ("HP: " + str(self.stats[1]) +
                               "\nDamage (HP average): " + str(self.stats[2]) +
                               "\nPenetration (mm): " + str(self.stats[3]) +
                               "\nReload (ticks): " + str(self.stats[4]) +
                               "\nArmour (mm):" + str(self.stats[5]) +
                               "\nHull Traverse Speed: " + str(self.stats[6]) +
                               "\nTurret Traverse Speed: " + str(self.stats[7]) +
                               "\nSpeed: " + str(self.stats[8]))
        self.name = self.sel

    def getAllTanks(self):
        self.conn = sqlite3.Connection("TankStats.db")
        self.cur = self.conn.cursor()
        a = self.cur.execute("SELECT name FROM Tanks").fetchall()
        a = [x[0] for x in a]
        return a

    def doBuy(self, event):
        buyApp = wx.App(False)
        buyFrame = Buy(None, self.username, self.getAllXP(), self.getAllTanks(), self)
        buyFrame.Show(True)
        buyApp.MainLoop()

    def getAllXP(self):
        conn = netComms.networkComms(self.ipAddr, int(self.port))
        conn.send(["ALLXP", self.username])
        return conn.recieved

    def getXP(self, name):
        conn = netComms.networkComms(self.ipAddr, int(self.port))
        conn.send(["XP", str(self.username), str(name)])
        return conn.recieved

    def doUpgrade(self, event):
        try:
            upApp = wx.App(False)
            upFrame = Upgrade(None, self.tank, self.getXP(self.tank[0]), self.username, self)
            upFrame.Show(True)
            upApp.MainLoop()
        except AttributeError as ex:
            messages.Warn(self.parent, "Please select a tank first")

    def refresh(self, username):
        """Reloads all components"""

        #Pull up all known tanks
        self.conn = sqlite3.Connection("TankStats.db")
        self.cur = self.conn.cursor()

        self.tanks = self.cur.execute("SELECT * FROM Tanks;").fetchall()
        #modify the client
        conn = netComms.networkComms(self.ipAddr, int(self.port))
        #print "Connection to loginServer made on " + str(self.ipAddr) + ":" + str(self.port)
        conn.send(["OWNED", self.username])
        self.owned = conn.recieved
        #print "From server: " + str(self.owned)
        conn.close()
        dataconn = sqlite3.Connection("TankStats.db")
        cur = dataconn.cursor()
        self.names = cur.execute("SELECT name FROM Tanks").fetchall()
        dataconn.close()
        self.names = [x[0] for x in self.names]
        #print "All names: " + str(self.names)
        self.tankChoice.Clear()
        for x in range(len(self.owned) - 2, 1, -1):
            if self.owned[x] == 0:
                #print "Pop val is " + str(self.owned[x]) + " " + str(x-1) + ":" + str(self.names[x-1])
                self.names.pop(x - 1)
        for i in self.names:
            self.tankChoice.Append(i)


def main(username, xp, owned):
    app = wx.App(False)
    frame = Main(None, username, xp, owned)
    frame.Show(True)
    app.MainLoop()

