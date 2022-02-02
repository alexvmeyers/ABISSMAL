# Created by PyCharm
# Author: nmoltta, gsvidaurre
# Project: ParentalCareTracking
# Date: 11/16/2021

# !/usr/bin/env python3

import time
import signal
from datetime import datetime
import sys
import csv
import RPi.GPIO as GPIO
import logging
from helper import logger_setup
from helper import csv_writer
from helper import box_id
from time import sleep
from subprocess import call
from os import walk

logger_setup('/home/pi/')

BEAM_PIN_lead = 13
BEAM_PIN_rear = 19
warn = 0
module = 'IRBB'
header = ['chamber_id', 'sensor_id', 'year', 'month', 'day', 'timestamp']
irbb_data = "/home/pi/Data_ParentalCareTracking/IRBB/"

logging.info('started irbb script')

GPIO.setmode(GPIO.BCM)
GPIO.setup(BEAM_PIN_lead, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BEAM_PIN_rear, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setwarnings(False)


def detect_beam_breaks_callback(BEAM_PIN, sensor_id):
    if not GPIO.input(BEAM_PIN):
        dt = datetime.now()
        logging.info('IRBB activity detected in sensor: ' + sensor_id)
        csv_writer(str(box_id), 'IRBB', irbb_data, f"{dt.year}_{dt.month}_{dt.day}",
                   header, [box_id, sensor_id, f"{dt.year}", f"{dt.month}", f"{dt.day}", f"{dt:%H:%M:%S.%f}"])


# Manual Ctrl + C
def signal_handler():
    GPIO.cleanup()
    sys.exit(0)
    

GPIO.add_event_detect(BEAM_PIN_lead, GPIO.FALLING,
                      callback=lambda x: detect_beam_breaks_callback(BEAM_PIN_lead, "lead"), bouncetime=100)

GPIO.add_event_detect(BEAM_PIN_rear, GPIO.FALLING,
                      callback=lambda x: detect_beam_breaks_callback(BEAM_PIN_rear, "rear"), bouncetime=100)


try:
    while True:
        pass

except KeyboardInterrupt:
    logging.info('exiting IRBB')
    GPIO.cleanup()

finally:
    GPIO.cleanup()
