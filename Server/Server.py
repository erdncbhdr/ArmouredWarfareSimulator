import SocketServer
import socket
import sqlite3
import json
import pickle
import math
import threading
from netifaces import interfaces, ifaddresses, AF_INET
from game_calcs import *
import time
import mapGen

#Create a class to make things easier
class Player():
    def __init__(self,  x,  y,  id,  name,  hp, username):
        self.x = x
        self.y = y
        self.id = id
        self.username = username
        self.name = name
        self.hp = hp
        if self.id % 2 == 0:
            self.angle = 90
            self.team = 0
        else:
            self.angle = 270
            self.team = 1
        self.turret_angle = self.angle
    def returnValues(self):
        return [self.x,  self.y,  self.angle,  self.turret_angle,  self.name, self.hp, self.username, self.team]
    
    def set(self,  data):
        self.x = data[0]
        self.y = data[1]
        self.angle = data[2]
        self.turret_angle = data[3]
        self.hp = data[4]
        
    
class Bullet():
    def __init__(self,  x,  y,  angle,  ownerId,  damage,  bulletID, penetration):
        self.x = x
        self.y =y
        self.angle = angle
        self.ded = False
        self.ownerId = ownerId
        self.damage = damage
        self.bulletID = bulletID
        self.penetration = penetration
    def update(self):
        self.x += 5*math.cos(math.radians(self.angle))
        self.y += 5*math.sin(math.radians(self.angle))
        if (self.x < -100 or
            self.y < -100 or
            self.x > 1124 or
            self.y > 880):
                self.ded = True
            
        
    def returnValues(self):
        return [self.x,  self.y,  self.angle,  self.ownerId,  self.damage,  self.ded,  self.bulletID, self.penetration]

class TankServer(SocketServer.BaseRequestHandler):
    """The main game server, executes requests given in string form and
        responds with data or confirmation"""
    #Temporary starting positions
    allow_reuse_address=True
    Start_x = [item for sublist in [[x,x] for x in range(200, 801,200)] for item in sublist]
    Start_y = [100, 700, 100, 700, 100, 700, 100, 700]
    Players = []
    Bullets = []
    toDespawn = []
    NextBulletId = 0
    Countdown = -1
    Map = mapGen.generateMap(1024, 768)

    def giveDatabaseConnection(self, cur):
        self.cur = cur
    def handle(self):
        while 1:
            #Get the data from the socket
            try:
                recv = self.request.recv(1024)
                self.data = pickle.loads(recv)
                #Check what sort of request it is
                if type(self.data[0]) == type("TopKek"):
                    self.toSend = self.stringRequest(self.data)
                else:
                    self.toSend = self.listRequest(self.data)
                self.request.sendall(pickle.dumps(self.toSend))
            except Exception as e:
                pass
            
    def stringRequest(self,  req):
        if "handshake" in req[0] and (TankServer.Countdown > 0 or TankServer.Countdown == -1):
            return self.doHandshake(req[1], req[2], req[3])
        elif TankServer.Countdown == 0:
            return [-1, -1, 0, -1]
        else:
            return "InvalidCommand"
            
    def listRequest(self,  req):
        #This will be 2 lists, one of the client, and the other of the bullets spawned since the last tick (max 1)
        #I will get [id, x, y, angle, turret angle]
        return self.get(req)
    def convertToList(self):
        """This will take Player objects and shove the x,y,angle,turret angle data into a list"""
        self.v = [[x.returnValues() for x in TankServer.Players]]
        self.v.append([y.returnValues() for y in TankServer.Bullets])
        return self.v
        
    def doHandshake(self,  name, hp, username):
        self.newId = len(TankServer.Players)
        TankServer.Players.append(Player(TankServer.Start_x[self.newId],  TankServer.Start_y[self.newId],  self.newId,  name,  hp, username))
        print "Connected: "+name
        if len(TankServer.Players) == 1:
            TankServer.Countdown = 30
            self.countdownThread = threading.Thread(target=self.countdown)
            self.countdownThread.start()
        return [self.newId,  self.convertToListHandShake(), TankServer.Countdown, TankServer.Map]

    def countdown(self):
        while TankServer.Countdown > 0:
            time.sleep(1)
            TankServer.Countdown -= 1
    def convertToListHandShake(self):
        return [x.returnValues() for x in TankServer.Players]
        
    def get(self, req):
        TankServer.Players[req[0]].set(req[1]) 
        #Update the bullets if ID 0 is connected
        for i in req[3]:
            for b in TankServer.Bullets:
                if b.bulletID == i:
                    TankServer.Bullets.remove(b)
        
        if req[0] == 0:
            for b in TankServer.Bullets:
                b.update()
                if b.ded:
                    TankServer.Bullets.remove(b)
       
        #Create a new bullet from x, y, angle information
        if len(req[2]) > 0:
            TankServer.Bullets.append(Bullet(req[2][0],  req[2][1],  req[2][2],  req[2][3],  req[2][4],  TankServer.NextBulletId, req[2][5]))
            TankServer.NextBulletId += 1

        #If bullets don't pen, they should rebound
        if len(req[4]) > 0:
            for bid in req[4]:
                id = bid[0]
                angleOfImpact = bid[1]
                angleOfNormal = bid[2]

                #print "AngleOfImpacta: "+str(angleOfImpact)
                #print "AngleOfNormala: "+str(angleOfNormal)
                if angleOfNormal < 0:
                    angleOfNormal = 360 - angleToNormal
                angleToNormal = angleOfNormal - angleOfImpact
                #print "AngleOfImpactb: "+str(angleOfImpact)
                #print "AngleOfNormalb: "+str(angleOfNormal)
                if angleOfNormal < 0:
                    angleOfNormal = 360 + angleOfNormal
                x1,y1,x2,y2 = bid[3], bid[4], bid[5], bid[6]
                x3,y3,x4,y4 = bid[7], bid[8], bid[9], bid[10]
                mod90 = angleOfNormal % 90
                for b in TankServer.Bullets:
                    if b.bulletID == id:
                        toEdit = b
                v = Vector(x1,x2,y1,y2)
                n = Vector(0,0,0,0)
                n.useAngle(x3, y3, angleOfNormal, 10)
                umult = (v.dotProduct(n) / n.dotProduct(n))
                u = Vector(n.x1 - umult*n.getMagnitude(), n.y1 - umult*n.getMagnitude(), n.x1, n.y1)
                w = v.add(Vector(u.x1, u.y1, u.x1 - u.getDx(),u.y1 - u.getDy()))
                newVel = w.add(Vector(u.x1, u.y1, u.x1 - u.getDx(),u.y1 - u.getDy()))
                toEdit.angle = newVel.angle
                
        return self.convertToList()
