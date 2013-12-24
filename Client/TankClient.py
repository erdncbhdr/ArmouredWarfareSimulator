from threading import Thread
from pygame import *
import time
import color as colour
import games
import netComms
from game_calcs import *
from Errors import *

try:
    games.init(screen_width = 1024, screen_height = 768, fps = 30)
except Exception:
    games.screen.quit()
    quit()
    games.init(screen_width = 1024, screen_height = 768, fps = 30)

def setupEnv():
    games.init(screen_width = 1024, screen_height = 768, fps = 30)

class superSquare(games.Sprite):
    def __init__(self, enemy, x, y):
        if enemy:
            image = games.load_image("res/Enemy.png")
        else:
            image = games.load_image("res/Friendly.png")
        super(superSquare, self).__init__(image=image, x=x, y=y)
    def updatePos(self, x, y):
        self.x = x
        self.y = y

class Player(games.Sprite):
    """ The main player class. """
    def __init__(self, x, y,  angle,  name,  hp, username, turret, team, clientteam):
        """ Initialize player sprite. """
        image = games.load_image("res/" + name + "_body.png")
        super(Player, self).__init__(image = image, x = x, y = y, angle = angle)
        self.name = name
        self.username = username
        self.team = team
        self.clientTeam = clientteam
        if self.team == self.clientTeam:
            self.square = superSquare(False, self.x, self.y-80)
        else:
            self.square = superSquare(True, self.x, self.y-80)

        self.hp = int(hp)
        self.userTag = games.Text(value = self.username, x=x, y=y-90, color=colour.black, size=20)
        self.nametag = games.Text(value = name+" "+str(self.hp), x = x,  y = y-70,  color=colour.black,  size=20)
        games.screen.add(self.nametag)
        games.screen.add(self.square)
        games.screen.add(self.userTag)
        self.maxHp = hp
        self.state = 0
        self.turret = turret
        print "NAME: "+self.name
        print "HP: "+str(self.hp)
    def update(self):
        self.nametag.value = self.name + " " + str(int(self.hp))
        if int(self.hp) < int(self.maxHp) / 2 and self.state == 0:
            self.image = games.load_image("res/" + self.name + "_body_damaged.png")
            self.turret.image = games.load_image("res/"+self.name+"_turret_damaged.png")
            self.state = 1
        self.square.x = self.x
        self.square.y = self.y-80

class Turret(games.Sprite):
    def __init__(self, x, y,  angle,  name):
        image = games.load_image("res/"+name+"_turret.png")
        super(Turret,  self).__init__(image=image, x = x, y = y , angle = angle)
        self.name = name
                
class Bullet(games.Sprite):
    image = games.load_image("res/Bullet_Sprite.png")
    def __init__(self,  x,  y,  angle,  ownerId,  damage,  bulletID, penetration):
        super(Bullet,  self).__init__(image = Bullet.image, x = x, y = y, angle = angle)
        self.ownerId = ownerId
        self.damage = damage
        self.bulletID = bulletID
        self.ded = False
        self.penetration = penetration

    def getx1x2(self):
        return self.x, self.y, self.x+5*math.cos(math.radians(self.angle)), self.y+5*math.sin(math.radians(self.angle))

    def returnValues(self):
        return [self.x,  self.y,  self.angle,  self.ownerId,  self.damage,  self.bulletID, self.penetration]
            
    def getVector(self):
        x1,y1,x2,y2 = self.getx1x2()
        return Vector(x1,y1,x2,y2)

class LocalPlayer(games.Sprite):
    def __init__(self, x, y,  angle,  turret,  speed,  hull_traverse,  hp,  reload,  armour,  name,  id,  damage, penetration, username, team):
        image  =games.load_image("res/"+str(name)+"_body.png")
        super(LocalPlayer,  self).__init__(image=image, x=x, y=y, angle=angle)
        self.name = name
        self.team = team
        self.turret = turret
        self.penetration = penetration
        self.bullets = []
        self.newBullets = None
        self.username = username
        self.reload = reload
        self.damage = damage
        self.id = id
        self.va = []
        self.fire = games.load_sound("res/Sounds/ms-1-45mm.ogg")
        self.idle = games.load_sound("res/Sounds/idle.ogg")
        self.moving = games.load_sound("res/Sounds/moving.ogg")
        self.canMove = False
        self.turret.canMove = False
        self.speed = speed
        self.hull_traverse = hull_traverse
        self.hp = int(hp)
        self.maxHp = self.hp
        self.reload_counter = self.reload
        self.armour = armour
        self.userTag = games.Text(value = self.username, x=x, y=y-90, color=colour.black, size=20)
        self.nametag = games.Text(value = str(self.name) + " " + str(self.hp),
                                  x = x,
                                  y = y-70,
                                  color=colour.black,
                                  size=20)
        self.reloadText = games.Text(value = "Reload in: " + str(self.reload_counter), x = 0, y = 0, color = colour.red, size = 30)
        self.orig_height = self.height-30
        self.orig_width = self.width
        games.screen.add(self.userTag)
        games.screen.add(self.reloadText)
        games.screen.add(self.nametag)

    def update(self):
        #Check for keyboard input
        if self.canMove:
            self.last_x = self.x
            self.last_y = self.y
            self.turret.last_x = self.turret.x
            self.turret.last_y = self.turret.y
            self.last_a = self.angle
            if games.keyboard.is_pressed(games.K_w):
                self.x += self.speed * math.cos(math.radians(self.angle))
                self.y += self.speed * math.sin(math.radians(self.angle))
                self.turret.x += self.speed * math.cos(math.radians(self.angle))
                self.turret.y += self.speed * math.sin(math.radians(self.angle))
                try:
                    self.idle.stop()
                except Exception:
                    pass
                #self.moving.play(loops=-1)

            elif games.keyboard.is_pressed(games.K_s):
                self.x -= self.speed * math.cos(math.radians(self.angle))
                self.y -= self.speed * math.sin(math.radians(self.angle))
                self.turret.x -= self.speed * math.cos(math.radians(self.angle))
                self.turret.y -= self.speed * math.sin(math.radians(self.angle))
                self.idle.stop()
                #self.moving.play(loops=-1)
            else:
                try:
                    self.moving.stop()
                except Exception:
                    pass
                #self.idle.play(loops=-1)

            if games.keyboard.is_pressed(games.K_a):
                self.angle -= self.hull_traverse
                self.turret.angle -= self.hull_traverse

            if games.keyboard.is_pressed(games.K_d):
                self.angle += self.hull_traverse
                self.turret.angle += self.hull_traverse

            if games.keyboard.is_pressed(games.K_SPACE):
                if self.reload_counter == 0:
                    self.newBullets = Bullet(self.x + self.getBulletOffsetX(),  self.y + self.getBulletOffsetY(),  self.turret.angle,  self.id,  self.damage,  -1, self.penetration)
                    self.reload_counter = self.reload
                    self.fire.play()
            self.reload_counter = int(self.reload_counter)
            if self.reload_counter > 0:
                #print "RELOAD: "+str(self.reload_counter)
                self.reload_counter -= 1
                self.reloadText.set_value("Reload in: " + str(self.reload_counter))

            if self.reload_counter == 0:
                self.reloadText.set_value("Ready to fire!")
                self.reloadText.set_color(colour.black)
            else:
                self.reloadText.set_color(colour.red)
            
        self.nametag.x = self.x
        self.nametag.y = self.y-70
        self.nametag.value = self.name + " "+str(int(self.hp))
        self.userTag.x = self.x
        self.userTag.y = self.y - 90
        if self.hp < self.maxHp / 2:
            self.image = games.load_image("res/"+self.name+"_body_damaged.png")
            self.turret.image = games.load_image("res/"+self.name+"_turret_damaged.png")
        if self.hp <= 0:
            self.hp = 0
            self.canMove = False
            self.turret.canMove = False


    def getBulletValues(self):
        try:
            #print "bullets: "+str(self.newBullets)
            self.va =[self.newBullets.x,  self.newBullets.y,  self.newBullets.angle,  self.newBullets.ownerId,  self.newBullets.damage, self.penetration]
            self.newBullets = None
            return self.va
        except Exception as e:
            #print e
            return []
            
    def getBulletOffsetX(self):
        return ((0.5 * self.turret.get_width())*math.cos(math.radians(self.turret.angle)))
        
    def getBulletOffsetY(self):
        return ((0.5*self.turret.get_height())*math.sin(math.radians(self.turret.angle)))
            
class LocalTurret(games.Sprite):
    def __init__(self, x, y,  angle,  turret_traverse,  name):
        image = games.load_image("res/"+name+"_turret.png")
        super(LocalTurret,  self).__init__(image=image, x=x, y=y, angle=angle)
        self.name = name
        self.canMove = False
        self.turret_traverse  = turret_traverse
    def update(self):
        if self.canMove:
            if games.keyboard.is_pressed(games.K_LEFT):
                self.angle -= self.turret_traverse

            elif games.keyboard.is_pressed(games.K_RIGHT):
                self.angle += self.turret_traverse

class Building(games.Sprite):
    def __init__(self, x, y, size):
        if size == 1:
            image = games.load_image("res/singleBuilding.png")
        elif size == 2:
            image = games.load_image("res/doubleBuilding.png")
        super(Building, self).__init__(image=image, x = x, y = y)
        self.setBounds(x, y, self.get_width(), self.get_height())

    def setBounds(self, x, y, width, height):
        TopLeft = [self.x, self.y]
        TopRight = [self.x + width, self.y]
        BottomLeft = [self.x, self.y + height]
        BottomRight = [self.x + width, self.y + height]
        TopSide = Vector(TopLeft[0], TopLeft[1], TopRight[0], TopRight[1])
        LeftSide = Vector(TopLeft[0], TopLeft[1], BottomLeft[0], BottomLeft[1])
        BottomSide = Vector(BottomLeft[0], BottomLeft[1], BottomRight[0], BottomRight[1])
        RightSide = Vector(TopRight[0], TopRight[1], BottomRight[0], BottomRight[1])
        self.myVectors = [TopSide, LeftSide, RightSide, BottomSide]

    def isCollided(self, b):
        vec = b.getVector()
        for v in self.myVectors:
            if intersect(v, vec):
                return True
        return False

class GameController(games.Sprite):
    """This is the main class-  it will col all network comms and update the players as required"""

    image = games.load_image("res/conn.jpg")
    
    def __init__(self,  stats,  host,  port, username):
        super(GameController,  self).__init__(image=GameController.image,  x=0,  y=0,  angle=0)
        #Create a connection
        self.connection = netComms.networkComms(host,  int(port))
        self.stats = stats
        self.username = username
        #Open resources
        self.fire = games.load_sound("res/Sounds/ms-1-45mm.ogg")
        self.idle = games.load_sound("res/Sounds/marder-idle.ogg")
        self.moskau = games.load_sound("res/Sounds/Moskau.ogg")
        self.moving = games.load_sound("res/Sounds/marder-moving.ogg")
        self.loadingSongs = [games.load_sound("res/Sounds/WoT-Opening-1.ogg"),
                             games.load_sound("res/Sounds/WoT-Opening-2.ogg"),
                             games.load_sound("res/Sounds/WoT-Opening-3.ogg")]
        self.battleSongs = [games.load_sound("res/Sounds/WoT-Battle-1.ogg"),
                            games.load_sound("res/Sounds/WoT-Battle-2.ogg"),
                            games.load_sound("res/Sounds/WoT-Battle-3.ogg"),
                            games.load_sound("res/Sounds/WoT-Battle-4.ogg"),
                            games.load_sound("res/Sounds/WoT-Battle-5.ogg")]

        self.despawnToServer = []
        self.damageDone = []
        name = self.stats[0]
        hp = self.stats[1]
        damage = self.stats[2]
        penetration = self.stats[3]
        reload = self.stats[4]
        armour = self.stats[5]
        hull_traverse = self.stats[6]
        turret_trav = self.stats[7]
        speed = self.stats[8]
        self.bg = games.load_image("background.png")
        self.update_ticks = 100
        self.bulletType = Bullet(0, 0, 0, 0, 0, 0, 0)

        #Create local instances of player and turret
        #First we have to handshake

        self.connection.send(["handshake", name, hp, self.username])

        #This will return us the currently connected players and our ID
        #print "RECV: "+str(self.connection.recieved)

        self.id = self.connection.recieved[0]

        if int(self.id)%2 == 0:
            self.team = 0
        else:
            self.team = 1

        self.serverPlayers = self.connection.recieved[1]

        #Start countdown to the game
        self.countdown = self.connection.recieved[2]

        #Add a timer
        self.timerTop = games.Text(value= "Game will start in:", x=400, y=300, size=50, color=colour.white)
        self.timerMain = games.Text(value= str(self.countdown), x=400, y=400, size= 50, color=colour.white)

        if self.countdown == 0:
            self.close()
        #Set the map
        self.map = self.connection.recieved[3]
        self.drawMap(self.map)


        #Create these players, excluding us, as our movement is handled locally
        #Add us
        #We will get the data in the form [x,y,angle,turret angle]
        self.clientTurret = LocalTurret(self.serverPlayers[self.id][0], self.serverPlayers[self.id][1],self.serverPlayers[self.id][3],  turret_trav,  name)
        self.client = LocalPlayer(self.serverPlayers[self.id][0], self.serverPlayers[self.id][1], self.serverPlayers[self.id][2],  self.clientTurret,  speed,
                                  hull_traverse,  hp,  reload,  armour,  name,  self.id,  damage, penetration, self.username, self.team)

        #Start the countdown
        self.countdownThread = Thread(target=self.countingDown)
        self.countdownThread.start()

        #Add us to the screen
        games.screen.add(self.client)
        games.screen.add(self.clientTurret)
        games.screen.add(self.timerTop)
        games.screen.add(self.timerMain)
        #We have handled us, remove us from the list
        self.serverPlayers.pop(self.id)
        #Create some variables to hold the players
        self.serverInstances = []
        self.serverInstancesTurret = []
        self.bullets = []
        self.toDespawn = []
        self.toRebound = []
        #Add everyone
        for p in self.serverPlayers:
            #Add a new turret instance
            self.serverInstancesTurret.append(Turret(p[0], p[1], p[3], p[4]))
            #Add a new player instance
            self.serverInstances.append(Player(p[0], p[1], p[2], p[4],  p[5], p[6], self.serverInstancesTurret[-1], p[7], self.client.team))
            #add them
            games.screen.add(self.serverInstances[-1])
            games.screen.add(self.serverInstancesTurret[-1])

            
        #Ok we cool

    def drawMap(self, map):
        print "MAP: "+str(map)
        width = games.screen.get_width()
        height = games.screen.get_height()
        print "Width:"+str(width)
        print "Height:"+str(height)
        #Split the screen into 50px blocks
        toplefts_x = [x for x in range(0, width+1, 100)]
        toplefts_y = [x for x in range(150, (height+1)-150, 100)]
        self.buildings = []
        for block in map:
            newBuilding = Building(toplefts_x[block[0]], toplefts_y[block[1]], block[2])
            self.buildings.append(newBuilding)
            games.screen.add(self.buildings[-1])
        return None

    def countingDown(self):
        import random
        if self.client.name == "KV1" or self.client.name == "T34":
            toPlay = self.moskau
        else:
            toPlay = random.choice(self.loadingSongs)
        toPlay.play()
        while self.countdown > 0:
            time.sleep(1)
            self.countdown -= 1
            self.timerMain.set_value(str(self.countdown))
        games.screen.remove(self.timerMain)
        games.screen.remove(self.timerTop)
        self.client.canMove = True
        self.client.turret.canMove = True

    def close(self, exception):
        games.screen.clear()
        games.screen.quit()
        raise exception

    def update(self):
        if games.keyboard.is_pressed(games.K_ESCAPE):
            self.connection.send("Disconnect")
            games.screen.quit()
            sys.exit([0])
        p = self.client
        t = self.client.turret
        for b in self.buildings:
            if self.client in b.get_overlapping_sprites():
                p.x = p.last_x
                p.y = p.last_y
                p.angle = p.last_a
                t.x = t.last_x
                t.y = t.last_y

        #Let's thread it ##Or not, that creates race conditions
        #Thread(target=self.doUpdating).start()
        self.doUpdating()

    def doUpdating(self):
        #This occurs on every gameloop, gonna update the local client and send some data 
        #Give the server my position
        try:
            self.connection.send([self.id,
                                 [self.client.x,
                                  self.client.y,
                                  self.client.angle,
                                  self.client.turret.angle,
                                  self.client.hp],
                                 self.client.getBulletValues(),
                                 self.despawnToServer,
                                 self.toRebound,
                                 self.damageDone])

        except HostDisconnectedException as e:
            self.close(e)
        if self.connection.recieved[0] == "EndGame":
            self.endGame(self.connection.recieved[1])

        #it'll give me the positions of all connected players, including me, we don't want that
        self.recvPlayers = self.connection.recieved[0]
        self.recvBullets = self.connection.recieved[1]
        self.damageDone = []
        #Ok. Pop us.
        self.recvPlayers.pop(self.id)
        self.recvCopy = self.recvPlayers

        #Now add the new players. if the list of connected is [p1, p2, p3, p4] and the new list is [p1,p2,p3,p4,p5], the new players are old players [len(old):]
        #For each in new players, create a new server instance and add it
        while len(self.recvPlayers) > len(self.serverInstances):
            try:
                self.newAdd = self.recvPlayers[-1]
                self.serverInstancesTurret.append(Turret(self.newAdd[0],  self.newAdd[1],  self.newAdd[3],  self.newAdd[4]))
                self.serverInstances.append(Player(self.newAdd[0],  self.newAdd[1],  self.newAdd[2],  self.newAdd[4],  self.newAdd[5], self.newAdd[6], self.serverInstancesTurret[-1], self.newAdd[7], self.client.team))
                games.screen.add(self.serverInstances[-1])
                games.screen.add(self.serverInstancesTurret[-1])
                self.recvPlayers.pop(-1)

            except IndexError as ex:
                self.resyncClient()

        #Now update everyone
        self.recvPlayers = self.recvCopy
        for i in range(len(self.serverInstances)):
            try:
                self.serverInstances[i].x = self.recvPlayers[i][0]
                self.serverInstances[i].y = self.recvPlayers[i][1]
                self.serverInstances[i].angle = self.recvPlayers[i][2]
                self.serverInstances[i].hp = self.recvPlayers[i][5]
                
                self.serverInstancesTurret[i].x = self.recvPlayers[i][0]
                self.serverInstancesTurret[i].y = self.recvPlayers[i][1]
                self.serverInstancesTurret[i].angle = self.recvPlayers[i][3]
                
                self.serverInstances[i].nametag.x  = self.serverInstances[i].x
                self.serverInstances[i].nametag.y  = self.serverInstances[i].y-70
                self.serverInstances[i].userTag.x = self.serverInstances[i].x
                self.serverInstances[i].userTag.y = self.serverInstances[i].y - 90
            except Exception as ex:
                print "Exception in update: " + str(ex)
                #self.resyncClient()
        
        self.doBulletSpawnDespawn(self.recvBullets)
        self.checkBulletCollisions() 
        
        #Ok we cool

    def doBulletSpawnDespawn(self,  server):
        """Main method to make the local bullets equal the server bullets"""

        #Init the arrays we'll use to store data
        self.despawnToServer = []
        self.toRebound = []

        #Check for building collisions
        self.checkBuildings(self.bullets)

        #These are the bullets currently spawned by the server and their IDS
        currentIDs = [b.bulletID for b in self.bullets]
        serverIDs = [b[6] for b in server]

        #Add new bullets
        for bullet in server:
            if bullet[6] not in currentIDs:
                self.fire.play()
                self.bullets.append(Bullet(bullet[0],  bullet[1],  bullet[2],  bullet[3],
                                           bullet[4],  bullet[6], bullet[7]))
                games.screen.add(self.bullets[-1])
                
        for b in self.bullets:
            if b.bulletID not in serverIDs:
                games.screen.remove(b)
                self.bullets.remove(b)
            for c in self.buildings:
                if c.isCollided(b):
                    self.despawnToServer.append(b.bulletID)

                
        for i in range(0,  len(server)):
            self.bullets[i].x = server[i][0]
            self.bullets[i].y = server[i][1]
            self.bullets[i].angle = server[i][2]
            
    def dotProduct(self,  vA,  vB):
        xComp = vA[0] * vB[0]
        yComp = vA[1] * vB[1]
        return xComp + yComp

    def checkBulletCollisions(self):
        """A generic bullet collision method. Calls about a million other things"""

        #Update the client's vectors
        self.setVectors()

        #Iterate through all the bullets, checks them
        for bullet in self.bullets:
            angle = math.radians(bullet.angle)
            if bullet.ownerId != self.client.id:
                if self.is_collided(bullet):
                    #self.damageDone.append([bullet.damage, bullet.ownerId])
                    pass

    def is_collided(self, bullet):
        """Checks for collision, will test for overlap between the vectors of the tank and the bullet"""

        #Repeat for all 4 side of the tank
        for v in self.vectors:
            if self.vectorsIntersect(v, bullet.getVector()):
                noVectorIntersects = False
                angle = getAngleOfIntersection(bullet.getVector(), v)
                if self.doesPenetrate(angle, bullet):

                    #Damage tank accordingly and despawn the bullet
                    self.client.hp -= bullet.damage
                    self.despawnToServer.append(bullet.bulletID)
                else:
                    b = bullet.getVector()
                    self.toRebound.append([bullet.bulletID,angle,v.angle - 90, b.x1, b.y1, b.x2, b.y2, v.x1, v.y1, v.x2, v.y2, bullet.angle])
            noVectorIntersects = True

        #BUG: Occasionally the bullet will just fly through the vector, this WILL penetrate as it needs to be at a very low angle
        overlaps =  self.client.get_overlapping_sprites()
        if bullet in overlaps and not noVectorIntersects:
            #This means that the bullet is within the tank without colliding
            #We'll give it penetration
            #self.client.hp -= bullet.damage
            #self.despawnToServer.append(bullet.bulletID)
            #self.damageDone.append([bullet.damage, bullet.ownerId])
            pass

    def vectorsIntersect(self, vecA, vecB):
        """Checks if 2 vectors intersect, calls game_calcs"""

        if intersect(vecA, vecB):
            return True
        return False

    def setVectors(self):
        #This sets vectors around the edge of the image
        ###DO NOT EDIT, MAGIC BE HERE###
        angle = math.radians(self.client.angle + 45)
        rect = self.client._rect
        center = rect.center
        tri_hyp = math.sqrt((self.client.orig_width/2)**2 + (self.client.orig_height/2)**2)
        corner1X, corner1Y = center[0] + (math.cos(angle)*tri_hyp), center[1] + (math.sin(angle)*tri_hyp)
        corner2X, corner2Y = center[0] - (math.cos(angle)*tri_hyp), center[1] - (math.sin(angle)*tri_hyp)
        corner3X, corner3Y = center[0] + (math.sin(angle)*tri_hyp), center[1] - (math.cos(angle)*tri_hyp)
        corner4X, corner4Y = center[0] - (math.sin(angle)*tri_hyp), center[1] + (math.cos(angle)*tri_hyp)
        self.vectors = [Vector(corner1X, corner1Y, corner3X, corner3Y),
                        Vector(corner1X, corner1Y, corner4X, corner4Y),
                        Vector(corner2X, corner2Y, corner3X, corner3Y),
                        Vector(corner2X, corner2Y, corner4X, corner4Y)]

    def doesPenetrate(self, angle, bullet):
        """Returns true if the bullet has enough penetration, false otherwise"""

        #This is the critical angle at which any bullet will auto-bounce
        if angle < 50:
            return False

        #Calculate effective armour via trigonometry.
        armourValue = self.client.armour
        effectiveArmour = armourValue / math.sin(math.radians(angle))

        #Check if the bullet has enough penetration and return
        if bullet.penetration > effectiveArmour:
            self.damageDone.append([bullet.damage, bullet.ownerId])
            return True
        else:
            return False

    def resyncClient(self):
        games.screen.clear()
        games.screen.add(self.client)
        games.screen.add(self.clientTurret)
        self.doBulletSpawnDespawn(self.recvBullets)
        for p in self.serverPlayers:
            #Add a new turret instance
            self.serverInstancesTurret.append(Turret(p[0], p[1], p[3], p[4]))
            #Add a new player instance
            self.serverInstances.append(Player(p[0], p[1], p[2], p[4],  p[5], p[6], self.serverInstancesTurret[-1], p[7], self.client.team))
            #add them
            games.screen.add(self.serverInstances[-1])
            games.screen.add(self.serverInstancesTurret[-1])

    def checkBuildings(self, bul):
        for b in bul:
            for a in self.buildings:
                if a.overlaps(b):
                    self.despawnToServer.append(b.bulletID)

    def endGame(self, stats):
        self.connection.close()
        games.screen.clear()
        games.screen.quit()
        quit()
        raise EndOfGame(str(stats))

def mainGame(instance):
    """Called to run the client, requires data for the tank and the host/port"""

    #Open the screen

    try:
        #This sets the initial conditions for the client
        username = instance[0]
        stats = instance[1]
        host = instance[2]
        port = instance[3]

        #Establish background
        back = games.load_image("res/background.png")
        games.screen.background = back

        #Set up the game controller and feed it the conditions
        fat_controller = GameController(stats,  host,  port, username)
        games.screen.add(fat_controller)

        #Start the game
        games.screen.mainloop()

    #Exceptions - can communicate with the login client
    except GameInProgressException as message:
        return message

    except HostDisconnectedException as message:
        return message

    #except Exception as ex:
    #    print "ERROR: " + str(ex)
    #    fat_controller.connection.send(["Disconnect", fat_controller.id])

