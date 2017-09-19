#!/usr/bin/env python3

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

username = input("Enter you telnet username: ")
password = getpass.getpass()
deviceList = open("./deviceList.txt")

for device in deviceList:
    print("Getting running config for " + (device))
    host = device.strip()
    connect = telnetlib.Telnet(host)
    print("connecting")
    connect.read_until(b"Username: ")
    connect.write((username + "\n").encode('ascii'))
    if password:
        connect.read_until(b"Password: ")
        connect.write((password + "\n").encode('ascii'))
        
    connect.write(b"terminal length 0\n")
    connect.write(b"show run\n")
    connect.write(b"exit\n")
    
    now = datetime.datetime.now()
    runningConfig = connect.read_all()
    saveFile = open(device + "_" + now.strftime("%d-%m-%Y %H:%M") +".txt", "w")
    saveFile.write(runningConfig.decode('ascii'))
    saveFile.write("\n")
    saveFile.close
    print("Config saved for " + device)