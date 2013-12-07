import SocketServer
import pickle
import threading
import time

from game_calcs import *
from Errors import *
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
        self.isOnWinning = False
        self.xpGained = 100
        self.damage = 0
        self.kills = 0
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
    Start_x = [item for sublist in [[x,x] for x in range(200, 801, 200)] for item in sublist]
    Start_y = [100, 700, 100, 700, 100, 700, 100, 700]
    Players = []
    Bullets = []
    toDespawn = []
    NextBulletId = 0
    Countdown = -1
    DeadPlayers = 0
    GameInProgress = True
    EndGameMessage = []
    Map = mapGen.generateMap(1024, 768)
    EndGameIds = []
    def giveDatabaseConnection(self, cur):
        self.cur = cur
    def handle(self):
        """Do something with the request"""

        while 1:
            if TankServer.GameInProgress:
                #Get the data from the socket
                recv = self.request.recv(1024)
                self.data = pickle.loads(recv)
                if recv == "" or self.data == "":
                    break
                #Check what sort of request it is
                if type(self.data[0]) == type("TopKek"):
                    self.toSend = self.stringRequest(self.data)
                else:
                    self.toSend = self.listRequest(self.data)
                self.request.sendall(pickle.dumps(self.toSend))

            else:
                try:
                    recv = pickle.loads(self.request.recv(1024))
                    if recv == "":
                        break
                    TankServer.EndGameIds.pop(TankServer.EndGameIds.index(recv[0]))
                    a = ["EndGame"]
                    a.append(TankServer.EndGameMessage[recv[0]])
                    print "END OF GAME: "+str(a)
                    self.request.sendall(pickle.dumps(a))
                    if len(TankServer.EndGameIds) == 0:
                        raise EndOfGame(TankServer.EndGameMessage)
                    if TankServer.Countdown == 0:
                        raise EndOfGame(TankServer.EndGameMessage)
                        break
                except Exception as ex:
                    print ex
                    if TankServer.Countdown == 0:
                        raise  EndOfGame(TankServer.EndGameMessage)
                        break
        self.finish()

    def getVictor(self):
        team0 = 0
        team1 = 0
        for p in TankServer.Players:
            if p.team == 0 and p.hp == 0:
                team0 += 1
            elif p.team == 1 and p.hp == 0:
                team1 += 1
        if team0 > team1:
            return 0
        else:
            return 1

    def stringRequest(self,  req):
        """Takes a string and outputs accordingly"""

        if "handshake" in req[0] and (TankServer.Countdown > 0 or TankServer.Countdown == -1):
            return self.doHandshake(req[1], req[2], req[3])
        elif TankServer.Countdown == 0:
            return [-1, -1, 0, -1]
        elif "Disconnect" in req[0]:
            for p in TankServer.Players:
                if p.id == req[1]:
                    p.hp = 0
                    p.username = "Disconnected"
            self.DeadPlayers += 1
            TankServer.EndGameIds.pop(TankServer.EndGameIds.index(req[1]))
            if self.isEndOfGame():
                self.endGame()
        else:
            return "InvalidCommand"
            
    def listRequest(self,  req):
        """Redirect method for requests in the form of a list"""

        return self.get(req)

    def isEndOfGame(self):
        team1Alive = 0
        team2Alive = 0
        for p in TankServer.Players:
            if p.hp > 0:
                if p.team == 0:
                    team1Alive += 1
                else:
                    team2Alive += 1
        if team1Alive == 0:
            self.victor = 1
            return  True
        if team2Alive == 0:
            self.victor =  0
            return True
        return False


    def convertToList(self):
        """This will take Player objects and shove the x,y,angle,turret angle data into a list"""
        self.v = [[x.returnValues() for x in TankServer.Players]]
        self.v.append([y.returnValues() for y in TankServer.Bullets])
        return self.v
        
    def doHandshake(self,  name, hp, username):
        """Add the new player to arrays and get going"""

        self.newId = len(TankServer.Players)
        TankServer.Players.append(Player(TankServer.Start_x[self.newId],  TankServer.Start_y[self.newId],  self.newId,  name,  hp, username))
        TankServer.EndGameIds.append(self.newId)
        print "Connected: "+name
        if len(TankServer.Players) == 1:
            TankServer.Countdown = 30
            self.countdownThread = threading.Thread(target=self.countdown)
            self.countdownThread.start()
        return [self.newId,  self.convertToListHandShake(), TankServer.Countdown, TankServer.Map]

    def countdown(self):
        """Create a 30 second timer at the start of the game"""

        while TankServer.Countdown > 0:
            time.sleep(1)
            TankServer.Countdown -= 1

    def convertToListHandShake(self):
        """Initial return value"""

        return [x.returnValues() for x in TankServer.Players]
        
    def get(self, req):
        """Acts as a 'getter', returns every other player's information and sends it in a handy list"""

        TankServer.Players[req[0]].set(req[1])
        #Check if the player is dead
        if TankServer.Players[req[0]].hp == 0:
            TankServer.DeadPlayers += 1
            if self.isEndOfGame():
                self.endGame()
        #Update the bullets if ID 0 is connected
        for i in req[3]:
            for b in TankServer.Bullets:
                if b.bulletID == i:
                    TankServer.Bullets.remove(b)
        
        if req[0] == 0:
            for b in TankServer.Bullets:
                if self.isCollidedWithMap(b):
                    #b.ded = True
                    None
                else:
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
                angleOfBullet = bid[11]
                anglePointingAway = (angleOfBullet + 180) % 360
                angleToNormal = angleOfNormal - angleOfBullet
                newAngle = (angleOfNormal + angleToNormal + 180) % 360
                for b in TankServer.Bullets:
                    if b.bulletID == id:
                        toEdit = b
                        toEdit.angle = newAngle

        if len(req[5]) > 0:
            for item in req[5]:
                newHp = req[1][4]
                ownerId = int(item[1])
                for player in TankServer.Players:
                    if player.id == ownerId:
                        player.damage += int(item[0])
                        player.xpGained += 20
                        if newHp <= 0:
                            player.kills += 1
                            player.xpGained += 200
        
                
        return self.convertToList()

    def isCollidedWithMap(self, b):
        """Self-explanatory, returns true if the bullet is collided with terrain"""
        return False

    def endGame(self):
        TankServer.Countdown = 3
        self.countdownThread = threading.Thread(target=self.countdown)
        victor = self.victor
        #Get a 1.5x XP boost if you win
        for p in TankServer.Players:
            if p.id == victor:
                p.xpGained *= 1.5
                p.isOnWinning = True
        TankServer.EndGameMessage = [[p.isOnWinning, p.xpGained, p.damage, p.kills, p.name, p.username] for p in TankServer.Players]
        TankServer.GameInProgress = False