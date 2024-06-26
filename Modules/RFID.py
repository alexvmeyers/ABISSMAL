# Created by PyCharm
# Author: tanismo, gsvidaurre
# Project: Abissmal
# Date: 11/13/21

# !/usr/bin/env python3

import wiringpi as wiringpi2
import time
import sys
from datetime import datetime
import csv
from helper import dir_setup
from helper import csv_writer
from helper import box_id
from helper import sms_alert
from time import sleep
from helper import get_logger

dir_setup("/home/pi/")

warn = 0
module = 'RFID'
header = ['chamber_id', 'sensor_id', 'year', 'month', 'day', 'timestamp', 'PIT_tag_ID']
rfid_data = "/home/pi/Data_Abissmal/RFID"
logging = get_logger(datetime.today())
logging.info('Started RFID script')
GPIO_PIN = 1


def WaitForCTS():
    while wiringpi2.digitalRead(GPIO_PIN):
        time.sleep(0.01)
    return


def RFIDSetup():
    response = wiringpi2.wiringPiSetup()
    wiringpi2.pinMode(GPIO_PIN, 0)
    fd = wiringpi2.serialOpen('/dev/serial0', 9600)
    wiringpi2.serialFlush(fd)
    if response != 0 and fd <= 0:
        print("Unable to Setup communications")
        logging.error("RFID Error: Unable to Setup communications")
        sms_alert('RFID', 'Error: Unable to setup communications')
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
    try:
        while True:
            WaitForCTS()
            wiringpi2.serialPutchar(fd, 0x52)
            wiringpi2.serialPutchar(fd, 0x00)
            ans = ReadInt(fd)
            time.sleep(0.1)
            if ans == int("0xD6", 16):
                ans = ReadText(fd)
                dt = datetime.now()
                logging.info('RFID read proximity: ' + ans)
                print('RFID activity detected')
                csv_writer(
                    str(box_id),
                    module,
                    rfid_data,
                    str(dt.strftime("%Y_%m_%d")),
                    header,
                    [
                        box_id,
                        'RFID',
                        dt.strftime("%Y"),
                        dt.strftime("%m"),
                        dt.strftime("%d"),
                        f"{dt:%H:%M:%S.%f}",
                        ans
                    ]
                )
                time.sleep(1)
    except KeyboardInterrupt:
        logging.info('Exiting RFID')
        print('Exiting RFID')
    except Exception as E:
        logging.error('RFID error: ' + str(E))
        print('RFID error: ' + str(E))
        sms_alert('RFID', 'Error: ' + str(E))


comms = RFIDSetup()
SetReaderMode(comms)
SetPollingDelay(comms)
ReadTagPageZero(comms)
