#! /usr/bin/PYTHON3

# Script to connect to list of devices, pull and save running configs with time date stamp
# Device list is pulled from text file containing list of IP addresses
# Currently prompts for username and password - TODO: add funcitonaility to allow as arguments from clu_c

# import required modules
import getpass
import datetime
import telnetlib

# Set global parmeters
# username    username used to connect to device
# password    users password for connecting to device
# deviceList    file containing list of IP addressing

username = raw_input("Enter you telnet username:")
password = getpass.getpass()
deviceList = open("./deviceList.txt")

for device in deviceList:
    print("Getting running config for" + (device))
    host = device.strip()
    connect = telnetlib.Telnet(host)
    connect.read_until("Username: ")
    connect.write(username + "\n")
    if password:
        connect.read_until("Password: ")
        connect.write(password + "\n")
        
    connect.write("terminal length 0\n")
    connect.write("show run\n")
    connect.write("exit\n")
    
    now = datetime.datetime.now()
    runningConfig = connect.read_all()
    saveFile = open(device + "_" + now, "w")
    saveFile.write(runningConfig)
    saveFile.write("\n")
    saveFile.close
    print("Config saved for " + device)