#! /usr/bin/python

"""Copyright 2011 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__="Adam Stelmack"
__version__="2.1.8"
__date__ ="14-Jan-2011 2:29:14 PM"

#Basic imports
from socket import *

from graph import graph

import sys
from time import sleep
import time
import datetime

from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.Bridge import Bridge, BridgeGain

class FileController:
    def __init__(self):
        self.file_data = None
        self.file_data_3 = None
        self.file_log = None
        self.file_prefix = None
    
    def print_data_3(self,msg):
        if self.file_data_3 is None:
            print(msg)
        else:
            self.file_data_3.write(msg+"\n")
    
    def print_data(self,msg):
        if self.file_data is None:
            print(msg)
        else:
            self.file_data.write(msg+"\n")
        
    def print_log(self,msg):
        if self.file_log is None:
            print(msg)
        else:
            self.file_log.write(msg+"\n")

        
    def open_file(self, fn):
        if(len(fn)>0):
            try:
                self.file_log = open("/root/sensor/"+fn+'_log.txt','w+',0)
            except:
                self.file_log = None

            try:                
                self.file_data = open("/root/sensor/"+fn+'_data.txt','w+',0)
                self.file_data_3 = open("/root/sensor/"+fn+'_3_data.txt','w+',0)                
            except:
                self.file_data = None
                self.file_data_3 = None
                self.print_log("data file create wrong: %s" % fn)
            print("Starting store to file: %s" % fn)
                
    def close_file(self):
        if self.file_data is not None:
            try:
                self.file_data.close()
                self.file_data_3.close()
            except:
                self.print_log("data file close wrong")
            finally:
                self.file_data = None
                self.file_data_3 = None
                
        if self.file_log is not None:
            try:
                self.file_log.close()
            except:
                print("log file close wrong")
            finally:
                self.file_log = None
                
        print("close_file: finished")

f = FileController()

try:
    bridge = Bridge()
except RuntimeError as e:
    f.print_log("Runtime Exception: %s" % e.details)
    f.print_log("Exiting.... ")
    #exit(1)

def displayDeviceInfo():

    f.print_log('Start: '+datetime.datetime.utcnow().ctime())
    f.print_log("|------------|----------------------------------|--------------|------------|")
    f.print_log("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    f.print_log("|------------|----------------------------------|--------------|------------|")
    f.print_log("|- %8s -|- %30s -|- %10d -|- %8d -|" % (bridge.isAttached(), bridge.getDeviceName(), bridge.getSerialNum(), bridge.getDeviceVersion()))
    f.print_log("|------------|----------------------------------|--------------|------------|")
    f.print_log("Number of bridge inputs: %i" % (bridge.getInputCount()))
    f.print_log("Data Rate Max: %d" % (bridge.getDataRateMax()))
    f.print_log("Data Rate Min: %d" % (bridge.getDataRateMin()))
    f.print_log("Input Value Max: %d" % (bridge.getBridgeMax(0)))
    f.print_log("Input Value Min: %d" % (bridge.getBridgeMin(0)))

def BridgeAttached(e):
    attached = e.device
    f.print_log(datetime.datetime.utcnow().ctime() + "    Bridge %i Attached!" % (attached.getSerialNum()))

def BridgeDetached(e):
    detached = e.device
    f.print_log(datetime.datetime.utcnow().ctime() + "    Bridge %i Detached!" % (detached.getSerialNum()))

def BridgeError(e):
    try:
        source = e.device
        f.print_log(datetime.datetime.utcnow().ctime() + "    Bridge %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        f.print_log(datetime.datetime.utcnow().ctime() + "    Phidget Exception %i: %s" % (e.code, e.details))


def BridgeData(e):

    source = e.device
    if (e.index == 0):
        f.print_data("%i;%i;%s;%f" % (source.getSerialNum(), e.index, time.time() , e.value))
    else:
        f.print_data_3("%i;%i;%s;%f" % (source.getSerialNum(), e.index, time.time() , e.value))

def printOk():
    f.print_log("**********************")
    f.print_log("*         OK         *")
    f.print_log("**********************")
    
def printErr():
    f.print_log("**********************")
    f.print_log("*       ERROR        *")
    f.print_log("**********************")

def close():
    f.print_log(datetime.datetime.utcnow().ctime() + "    Closing...")

    try:
        f.print_log(datetime.datetime.utcnow().ctime() + "    Disable the Bridge input for reading data...")
        bridge.setEnabled(0, False)
        bridge.setEnabled(3, False)        
        sleep(2)
    except PhidgetException as e:
        f.print_log(datetime.datetime.utcnow().ctime() + "    Phidget Exception %i: %s" % (e.code, e.details))
        try:
            bridge.closePhidget()
        except PhidgetException as e:
            f.print_log(datetime.datetime.utcnow().ctime() + "    Phidget Exception %i: %s" % (e.code, e.details))
            f.print_log(datetime.datetime.utcnow().ctime() + "    Exiting....")
            printErr()
    else:
        try:
            bridge.closePhidget()
        except PhidgetException as e:
            f.print_log(datetime.datetime.utcnow().ctime() + "    Phidget Exception %i: %s" % (e.code, e.details))
            f.print_log(datetime.datetime.utcnow().ctime() + "    Exiting....")
            printErr()
        else:
            printOk()
    
def start():
    try:
        bridge.setOnAttachHandler(BridgeAttached)
        bridge.setOnDetachHandler(BridgeDetached)
        bridge.setOnErrorhandler(BridgeError)
        bridge.setOnBridgeDataHandler(BridgeData)
    except PhidgetException as e:
        f.print_log(datetime.datetime.utcnow().ctime() + "    Phidget Exception %i: %s" % (e.code, e.details))
        f.print_log(datetime.datetime.utcnow().ctime() + "    Exiting....")
        #exit(1)

    f.print_log("Opening phidget object....")

    try:
        bridge.openPhidget()
    except PhidgetException as e:
        f.print_log(datetime.datetime.utcnow().ctime() + "    Phidget Exception %i: %s" % (e.code, e.details))
        f.print_log(datetime.datetime.utcnow().ctime() + "    Exiting....")
        #exit(1)

    f.print_log(datetime.datetime.utcnow().ctime() + "    Waiting for attach....")

    try:
        bridge.waitForAttach(10000)
    except PhidgetException as e:
        f.print_log(datetime.datetime.utcnow().ctime() + "    Phidget Exception %i: %s" % (e.code, e.details))
        try:
            bridge.closePhidget()
        except PhidgetException as e:
            f.print_log(datetime.datetime.utcnow().ctime() + "    Phidget Exception %i: %s" % (e.code, e.details))
            f.print_log(datetime.datetime.utcnow().ctime() + "    Exiting....")
            #exit(1)
        f.print_log(datetime.datetime.utcnow().ctime() + "    Exiting....")
        #exit(1)
    else:
        displayDeviceInfo()

    try:
        f.print_log(datetime.datetime.utcnow().ctime() + "    Set data rate to 8ms ...")
        bridge.setDataRate(16)
        sleep(2)

        f.print_log(datetime.datetime.utcnow().ctime() + "    Set Gain to 8...")
        bridge.setGain(0, BridgeGain.PHIDGET_BRIDGE_GAIN_8)
        bridge.setGain(3, BridgeGain.PHIDGET_BRIDGE_GAIN_8)        
        sleep(2)

        f.print_log(datetime.datetime.utcnow().ctime() + "    Enable the Bridge input for reading data...")
        bridge.setEnabled(0, True)
        bridge.setEnabled(3, True)
        sleep(2)

    except PhidgetException as e:
        f.print_log(datetime.datetime.utcnow().ctime() + "    Phidget Exception %i: %s" % (e.code, e.details))
        try:
            bridge.closePhidget()
        except PhidgetException as e:
            f.print_log(datetime.datetime.utcnow().ctime() + "    Phidget Exception %i: %s" % (e.code, e.details))
            f.print_log(datetime.datetime.utcnow().ctime() + "    Exiting....")
            #exit(1)
        f.print_log(datetime.datetime.utcnow().ctime() + "    Exiting....")
    print('storing...\n')

def server():
        s = socket(AF_INET, SOCK_STREAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind(('',9000))
        s.listen(5)
        f.print_log('listening...')
        
        while True:
            client, address = s.accept()
            f.print_log("sensor server: got connection from %s port %d\n" % (address[0], address[1]))
            client.send("Connected\n")
            data = client.recv(1024)

            while(len(data) >0):
               if "stop" in data:
                   print("stop incoming")               
                   close()
                   f.close_file()
                   
                   client.close()
                   data=''
                   g = graph('/root/sensor/data/','/root/sensor/stylesheets/', f.file_prefix)
                   g.saveTData()
                   break
               else:
                   if(len(data)>0):
                       f.file_prefix = data
                       f.open_file("data/"+data)
                       start()

               data = client.recv(1024)
               
server()
