#!/usr/bin/env python
import SocketServer
import pickle
import sqlite3


class LogServer(SocketServer.BaseRequestHandler):
    conn = sqlite3.Connection("LoginDatabase", check_same_thread=False)
    cur = conn.cursor()
    def handle(self):
        recv = self.request.recv(1024)
        #print "Recieved: "+str(recv)
        self.data = pickle.loads(recv)
        #print "REQUEST: "+str(self.data[0])
        if self.data[0] == "LOGIN":
            self.login(self.data[1])
        elif self.data[0] == "CREATE":
            self.create(self.data[1])
        elif self.data[0] == "Update":
            self.update(self.data[1:])
        elif self.data[0] == "GET":
            self.get(self.data[1], self.data[2])
        elif self.data[0] == "XP":
            self.xp(self.data[1], self.data[2])
        elif self.data[0] == "OWNED":
            self.owned(self.data[1])
        elif self.data[0] == "COSTS":
            self.costs()
        elif self.data[0] == "ALLXP":
            self.allXP(self.data[1])
        elif self.data[0] == "BUY":
            self.buy(self.data[1], self.data[2], self.data[3])
        else:
            #print str(self.data)
            self.request.sendall(pickle.dumps("UnknownRequestError"))

    def buy(self, name, user, previousTank):
        id = LogServer.cur.execute("SELECT UserId FROM UserInfo WHERE Username = ?", [user]).fetchone()
        #print "ID: "+str(id)
        LogServer.cur.execute("UPDATE UserOwned SET "+name+" = 1 WHERE UserId = ?", [id[0]])
        cost = LogServer.cur.execute("SELECT Cost FROM TankPrices WHERE TankName = ?", [name]).fetchone()
        #print "COST: "+str(cost)
        currentXp = LogServer.cur.execute("SELECT "+previousTank+" FROM UserProgress WHERE UserId = ?", [id[0]]).fetchone()
        #print "XP: "+str(currentXp)
        newXp = int(currentXp[0]) - int(cost[0])
        LogServer.cur.execute("UPDATE UserProgress SET "+previousTank+ " = ? WHERE UserId = ?", [newXp, id[0]])
        LogServer.conn.commit()
        self.openCloseConn()
        self.request.sendall(pickle.dumps("DONE"))

    def allXP(self, username):
        xp = LogServer.cur.execute("SELECT * FROM UserProgress INNER JOIN UserInfo ON UserInfo.UserId = UserProgress.UserId WHERE"
                                   " UserInfo.Username = ?", [username]).fetchone()[1:]
        self.request.sendall(pickle.dumps(xp))

    def costs(self):
        cost = LogServer.cur.execute("SELECT Cost FROM TankPrices").fetchall()
        #print "cost: "+str(cost)
        cost = [x[0] for x in cost]
        self.request.sendall(pickle.dumps(cost))

    def login(self, dat):
        #Check if these credentials are in the database
        if len(LogServer.cur.execute("""SELECT  UserInfo.UserName FROM UserInfo
                                        INNER JOIN UserPass ON UserInfo.UserId=UserPass.UserId
                                        WHERE UserInfo.Username=?
                                        AND UserPass.HashPass=?""", dat).fetchall()) > 0:
            userId = LogServer.cur.execute("SELECT UserId FROM UserInfo WHERE Username = ?;", [dat[0]]).fetchone()[0]
            print "ID LOGGING IN: "+str(userId)
            a=(LogServer.cur.execute("""SELECT UserInfo.Username, UserProgress.*, UserOwned.* From UserInfo
                                        INNER JOIN UserProgress, UserOwned ON UserInfo.UserId = UserProgress.UserId
                                        AND UserInfo.UserId = UserOwned.UserId WHERE UserInfo.Username = ?;""", [dat[0]]).fetchone())
            self.request.sendall(pickle.dumps(a))
        else:
            print "Login failed"
            self.request.sendall(pickle.dumps("LoginFailure"))
        
    def create(self, dat):
        print "DATA RECIEVED"
        nextId = len(LogServer.cur.execute("SELECT Username FROM UserInfo").fetchall())+1
        if len(LogServer.cur.execute("SELECT * FROM UserInfo WHERE Username = ?", [dat[0]]).fetchall()) > 0:
            self.request.sendall(pickle.dumps("UsernameException"))
        else:
            print "Next ID: "+str(nextId)
            dat.append(nextId)
            self.createNewAccount(dat)

    def get(self, username, tankname):
        values = [username]
        #print "VALS: "+str(values)
        a = LogServer.cur.execute("""SELECT """+tankname+""" FROM UserUpgrades INNER JOIN UserInfo ON UserUpgrades.UserId = UserInfo.UserId
                                  WHERE UserInfo.Username=?""", values).fetchall()
        print str(a[0][0][:-1])
        self.request.sendall(pickle.dumps(a[0][0][:-1]))

    def convertToString(self, lst):
        #print "LIST: "+str(lst)
        a = ""
        for b in lst:
            a += str(b) + ":"
        return a
    def createNewAccount(self, data):
        #Here be dragons
        self.openCloseConn()
        LogServer.cur.execute("INSERT INTO UserInfo VALUES (?, ?);", [data[2], data[0]])
        LogServer.cur.execute("INSERT INTO UserPass VALUES (?, ?);", [data[2], data[1]])
        LogServer.cur.execute("INSERT INTO UserOwned VALUES (?, 1, 0, 1, 0, 1, 0, 1);", [data[2]])
        LogServer.cur.execute("INSERT INTO UserProgress VALUES (?, 0, 0, 0, 0, 0, 0, 0);", [data[2]])
        LogServer.cur.execute("INSERT INTO UserUpgrades VALUES (?, 0, 0, 0, 0, 0, 0, 0);", [data[2]])
        tanknames = LogServer.cur.execute("SELECT Name FROM TankStats").fetchall()
        self.makeListSane(tanknames)
        #print "NAMES: "+str(tanknames)
        for i in range(7):
            Stats = LogServer.cur.execute("SELECT * FROM TankStats WHERE Name = ?;", [tanknames[i]]).fetchall()
            values = [self.convertToString(Stats[0]), data[2]]
            LogServer.cur.execute("UPDATE UserUpgrades SET "+tanknames[i]+" = ? WHERE UserId = ?;", values)
        #print "VALUES COMMITING"
        LogServer.conn.commit()
        #print "ACCOUNT CREATED"
        self.openCloseConn()
        self.request.sendall(pickle.dumps("COMPLETE"))

    def xp(self, user, tank):
        a = LogServer.cur.execute("""SELECT """+tank+ """ FROM UserProgress INNER JOIN UserInfo ON UserProgress.UserId =
                                    UserInfo.UserId WHERE UserInfo.Username=?""", [user]).fetchone()[0]
        #print str(a)
        self.request.sendall(pickle.dumps(a))

    def makeListSane(self, lst):
        for i in range(len(lst)):
            lst[i] = str(lst[i][0])

    def openCloseConn(self):
        LogServer.conn.close()
        LogServer.conn = sqlite3.Connection("LoginDatabase")
        LogServer.cur = LogServer.conn.cursor()

    def update(self, data):
        user = data[0]
        stats = data[1]
        newXp = data[2]
        letsgetthename = stats.split(":")[0]
        #print str(letsgetthename)
        #print "USER: "+str(user)
        userId = int(LogServer.cur.execute("SELECT UserId FROM UserInfo WHERE Username = ?;", [user]).fetchone()[0])
        #print "USERID: "+str(userId)
        LogServer.cur.execute("UPDATE UserUpgrades SET "+letsgetthename+ " = ? WHERE UserId = ?", [stats, userId])
        LogServer.cur.execute("UPDATE UserProgress SET "+letsgetthename+" = ? WHERE UserId = ?", [newXp, userId])
        LogServer.conn.commit()
        self.openCloseConn()

    def owned(self, username):
        owned = LogServer.cur.execute("SELECT * FROM UserOwned INNER JOIN UserInfo ON UserOwned.UserId = UserInfo.UserId WHERE "
                                      "UserInfo.Username = ?", [username]).fetchone()
        #print "OWNED: "+str(owned)
        self.request.sendall(pickle.dumps(owned))


def getConfiguration(conf, keyword):
    for a in conf:
        if keyword in a and "#" not in a:
            toRet = a.split("=")
            #print toRet
            return toRet[1]

def start():
    try:
        r = open("login.conf", "r")
        config = r.read().split("\n")
        ipAddr  = getConfiguration(config, "ip_address")
        port = getConfiguration(config, "port")
        r.close()
        server = SocketServer.TCPServer((ipAddr, int(port)), LogServer)
        print ("Login server running on "+str(ipAddr)+":"+str(port))
        server.serve_forever()
    except Exception as ex:
        print ("Port is not free")
        print ("Technical information: "+str(ex))


def main():
    import threading
    a = threading.Thread(target=start)
    a.start()

