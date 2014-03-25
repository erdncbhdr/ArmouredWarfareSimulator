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
    """Read the config file and get the specified option"""
    for a in conf:
        if keyword in a and "#" not in a:
            toRet = a.split("=")
            return toRet[1]


class Buy(selectGui.TankBuy):
    """A class to handle the tank purchase GUI"""
    def __init__(self, parent, username, xp, alltanks, owner):
        selectGui.TankBuy.__init__(self, parent)
        self.username = username
        self.alltanks = alltanks
        self.xp = xp
        self.populate()
        self.parent = parent
        self.owner = owner

    def populate(self):
	"""Put the tank names into the list"""
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
	"""Show the correct price of the selected tank"""
        self.name = self.TankBox.GetValue()
        tankvalue = self.alltanks.index(self.name)
        self.xpBox.SetValue(str(self.xp[tankvalue - 1]))
        self.priceBox.SetValue(str(self.costs[tankvalue]))

    def buyTank(self, event):
	"""Button press event to send the command to buy the tank"""
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
	"""Close the GUI"""
        self.owner.refresh(self.owner.username)
        self.Show(False)


class Upgrade(selectGui.UpgradeForm):
    """A class to handle the tank upgrade GUI"""
    def __init__(self, parent, tank, xp, username, form):
        selectGui.UpgradeForm.__init__(self, parent)
        #For reference
        self.form = form
        self.username = username
        self.parent = parent
        self.name = tank[0]
        self.hp = int(tank[1])
        self.damage = int(tank[2])
        self.penetration = int(tank[3])
        self.reload = int(tank[4])
        self.armour = int(tank[5])
        self.hullTraverse = float(tank[6])
        self.turretTraverse = float(tank[7])
        self.speed = float(tank[8])
        #Progress is in form XP for each tank
        self.xp = int(xp)

        self.populateBoxes()

    def populateBoxes(self):
	"""Put the selected tank stats into the boxes"""
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
	"""Button press event to upgrade HP"""
        if self.xp >= 10:
            self.xp -= 10
            self.hp += int(1000 / self.hp)
            self.populateBoxes()

    def upDam(self, event):
	"""Button press event to upgrade damage"""
        if self.xp >= 10:
            self.xp -= 10
            self.damage += int(300 / self.damage)
            self.populateBoxes()

    def upArm(self, event):
	"""Button press event to upgrade armour"""
        if self.xp >= 10:
            self.xp -= 10
            self.armour += int(300 / self.armour)
            self.populateBoxes()

    def upPen(self, event):
	"""Button press event to upgrade penetration"""
        if self.xp >= 10:
            self.xp -= 10
            self.penetration += int(450 / self.penetration)
            self.populateBoxes()

    def upHTr(self, event):
	"""Button press event to upgrade hull traverse"""
        if self.xp >= 10:
            self.hullTraverse += (5 / self.hullTraverse)
            self.xp -= 10
            self.populateBoxes()

    def upTTra(self, event):
	"""Button press event to upgrade turret traverse"""
        if self.xp >= 10:
            self.xp -= 10
            self.turretTraverse += (5 / self.turretTraverse)
            self.populateBoxes()

    def upRel(self, event):
	"""Button press event to upgrade reload"""
        if self.xp >= 10:
            self.xp -= 10
            self.reload -= int(self.reload / 20)
            self.populateBoxes()

    def upSp(self, event):
	"""Button press event to upgrade speed"""
        if self.xp >= 10:
            self.xp -= 10
            self.speed += int(3 / self.speed)
            self.populateBoxes()

    def convertToString(self, lst):
	"""Convert a list of stats into a string"""
        a = ""
        for b in lst:
            a += str(b) + ":"
        return a

    def getNewStats(self):
	"""Put the upgraded stats into a server-readable format"""
        statList = [self.name, self.hp, self.damage, self.penetration, self.reload,
                    self.armour, self.hullTraverse, self.turretTraverse, self.speed]
        a = self.convertToString(statList)
        return a

    def confirmEdit(self, event):
	"""Ask the user if they are really sure they want to upgrade"""
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
	"""Close the GUI without changing anything"""
        self.Show(False)


class Main(selectGui.MainFrame):
    """A class to handle the tank selection GUI"""
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
	"""Convert a list of floats to ints"""
        for i in range(len(lst)):
            try:
                lst[i] = float(lst[i])
            except Exception:
                pass
        return lst

    def battleThread(self, instance):
	"""Start the main battle thread"""
        import TankClient
        #TankClient.setupEnv()
        a = TankClient.mainGame(instance)
        return a

    def goToBattle(self, event):
	"""Set up the client to launch the game engine and then run the game"""
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

        except NoConnectionException:
            messages.Warn(self.parent, "There is no server on this port, please double check and try again.")
            self.Show(True)

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
	"""Take the user input of the host and store it""" 
        try:
            hostPort = self.AddressBox.Value.split(":")
            self.host = hostPort[0]
            self.port = hostPort[1]
        except Exception:
            pass

    def getStats(self, username, tankName):
	"""Get the users stats for that specific tank"""
        conn = netComms.networkComms(self.ipAddr, int(self.port))
        conn.send(["GET", username, tankName])
        a = (conn.recieved)
        conn.close()
        #print self.tankChoice.GetSelection()
        return a.split(":")


    def doStats(self, event):
	"""Update the text box with the tanks stats"""
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
	"""Return all possible tanks"""
        self.conn = sqlite3.Connection("TankStats.db")
        self.cur = self.conn.cursor()
        a = self.cur.execute("SELECT name FROM Tanks").fetchall()
        a = [x[0] for x in a]
        return a

    def doBuy(self, event):
	"""Open the tank purchase GUI"""
        buyApp = wx.App(False)
        buyFrame = Buy(None, self.username, self.getAllXP(), self.getAllTanks(), self)
        buyFrame.Show(True)
        buyApp.MainLoop()

    def getAllXP(self):
	"""Get the users progress on all tanks from the server"""
        conn = netComms.networkComms(self.ipAddr, int(self.port))
        conn.send(["ALLXP", self.username])
        return conn.recieved

    def getXP(self, name):
	"""Get the users progress on one specific tank from the server"""
        conn = netComms.networkComms(self.ipAddr, int(self.port))
        conn.send(["XP", str(self.username), str(name)])
        return conn.recieved

    def doUpgrade(self, event):
	"""Open the upgrade GUI"""
        try:
            upApp = wx.App(False)
            upFrame = Upgrade(None, self.getStats(self.username, self.sel), self.getXP(self.sel), self.username, self)
            upFrame.Show(True)
            upApp.MainLoop()
        except Exception as ex:
            messages.Warn(self.parent, "Please select a tank first")
            messages.Warn(self.parent, str(ex))

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
    """Main method to open the GUI"""
    app = wx.App(False)
    frame = Main(None, username, xp, owned)
    frame.Show(True)
    app.MainLoop()

