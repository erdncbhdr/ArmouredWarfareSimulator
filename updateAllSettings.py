#!/usr/bin/env python
import os
import shutil

f = open("login.conf", "w+")

f.write("#This is the configuration for Armoured Warfare Simulator 2014")
f.write("\n#The data for the login server is stored here")
ip = raw_input("Please enter the IP address of the server machine: ")
f.write("\nip_address="+str(ip))
f.write("\n#The port the server is running on")
port = raw_input("Which port do you wish to run on? ")
f.write("\nport="+str(port))
lol = raw_input("\nDo you want to boot the login server on game launch? (True/False) ")
f.write("\nloginOnLaunch="+str(lol))
f.close()
print "\n\nServer configured. Copying to client and server directories."

shutil.copy("login.conf", "Server/")
shutil.copy("login.conf", "Client/")
