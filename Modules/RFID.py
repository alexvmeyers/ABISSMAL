# Created by PyCharm
# Author: nmoltta, gsvidaurre
# Project: ParentalCareTracking
# Date: 11/13/21

# !/usr/bin/env python3

import wiringpi as wiringpi2
import numpy as np
import time
import sys
from datetime import datetime

import csv
import logging
from helper import logger_setup
from helper import csv_writer
from helper import box_id
from helper import email_alert
from time import sleep

logger_setup("/home/pi/")

warn = 0
module = 'RFID'

header = ['chamber_id', 'year', 'month', 'day', 'timestamp', 'PIT_tag_ID']
rfid_data = "/home/pi/Data_ParentalCareTracking/RFID"

logging.info('started RFID script')

GPIO_PIN = 1


def WaitForCTS():
    while wiringpi2.digitalRead(GPIO_PIN):
        time.sleep(0.001)
    return


def RFIDSetup():
    response = wiringpi2.wiringPiSetup()
    wiringpi2.pinMode(GPIO_PIN, 0)
    fd = wiringpi2.serialOpen('/dev/serial0', 9600)
    wiringpi2.serialFlush(fd)
    if response != 0 and fd <= 0:
        print("Unable to Setup communications")
        logging.error("Unable to Setup communications")
        email_alert('RFID', 'Error: Unable to setup communications')
        sys.exit()
    return fd


def SetReaderMode(fd):
    WaitForCTS()
    wiringpi2.serialPutchar(fd, 0x76)
    wiringpi2.serialPutchar(fd, 0x03)


def SetPollingDelay(fd):
    WaitForCTS()
    wiringpi2.serialPutchar(fd, 0x50)
    wiringpi2.serialPutchar(fd, 0x60)


def ReadText(fd):
    response = ""
    i = 1
    while i <= 5:
        temp = format(wiringpi2.serialGetchar(fd), 'x').upper()
        if len(temp) == 1:
            temp = '0' + temp
        if i <= 4:
            temp = temp + "-"
        response = response + temp
        i = i + 1
    return response


def ReadInt(fd):
    qtydata = wiringpi2.serialDataAvail(fd)
    response = 0
    if qtydata > 0:
        response = wiringpi2.serialGetchar(fd)
    return response


def ReadTagPageZero(fd):
    notag = True
    try:
        while notag:
            WaitForCTS()
            wiringpi2.serialPutchar(fd, 0x52)
            wiringpi2.serialPutchar(fd, 0x00)
            time.sleep(0.1)
            ans = ReadInt(fd)
            if ans == int("0xD6", 16):
                notag = False
                ans = ReadText(fd)
                dt = datetime.now()
                logging.info('RFID activity detected at:' + f"{dt:%H:%M:%S.%f}")
                print('RFID activity detected at:' + f"{dt:%H:%M:%S.%f}")
                csv_writer(str(box_id), module, rfid_data, f"{dt.year}_{dt.month}_{dt.day}", header,
                           [box_id, f"{dt.year}", f"{dt.month}", f"{dt.day}", f"{dt:%H:%M:%S.%f}", ans])
                notag = True

    except KeyboardInterrupt:
        logging.info('exiting RFID')
        print('exiting RFID')
    except Exception as E:
        logging.error('RFID error: ' + str(E))
        print('RFID error: ' + str(E))
        email_alert('RFID', 'Error: ' + str(E))


comms = RFIDSetup()
SetReaderMode(comms)
SetPollingDelay(comms)
ReadTagPageZero(comms)
