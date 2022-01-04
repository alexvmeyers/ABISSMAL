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
from Video import convert
from Video import record_video
from time import sleep
from subprocess import call
from os import walk

logger_setup('/home/pi/')

<<<<<<< HEAD
=======
# GPIO pin IDs through which IR receivers transmit data
# BEAM_PIN = 16
>>>>>>> 952fc981b1f7dac97792713eee6f53ab3a58dbfa
BEAM_PIN_lead = 16
BEAM_PIN_rear = 19
#REC_LED = 12  # change accordingly
VIDEO_PIN = 13
warn = 0
module = 'IRBB'
<<<<<<< HEAD
header = ['chamber_id', 'sensor_id', 'year', 'month', 'day', 'timestamp']
irbb_data = "/home/pi/Data_ParentalCareTracking/IRBB/"
video_duration = 90
video_data = "/home/pi/Data_ParentalCareTracking/Video/"
camera_state = 0 # global variable, camera turned off
             
=======

header = ['chamber_id', 'sensor_id', 'year', 'month', 'day', 'timestamp']

irbb_data = "/home/pi/Data_ParentalCareTracking/IRBB"
>>>>>>> 952fc981b1f7dac97792713eee6f53ab3a58dbfa

logging.info('started irbb + video script')


<<<<<<< HEAD
# Need to update recording function to record only if the previous video
# was recorded 90 seconds or some threshold ago
=======
>>>>>>> 952fc981b1f7dac97792713eee6f53ab3a58dbfa
def detect_beam_breaks_callback(BEAM_PIN, sensor_id):
    
    if not GPIO.input(BEAM_PIN):
        dt = datetime.now()
        logging.info('IRBB activity detected in sensor: ' + sensor_id)
        csv_writer(str(box_id), 'IRBB', irbb_data, f"{dt.year}_{dt.month}_{dt.day}",
                   header, [box_id, sensor_id, f"{dt.year}", f"{dt.month}", f"{dt.day}", f"{dt:%H:%M:%S.%f}"])
        if sensor_id == "rear":
            #GPIO.output(REC_LED, GPIO.HIGH)
            # sleep(1)
            GPIO.output(VIDEO_PIN, GPIO.HIGH)
            sleep(1)
            GPIO.output(VIDEO_PIN, GPIO.LOW)
            
    else:
        #GPIO.output(REC_LED, GPIO.LOW)
        GPIO.output(VIDEO_PIN, GPIO.LOW)
        
# Another callback function to monitor the LED and record video
#def detect_trigger_callback(BEAM_PIN):
#    if GPIO.input(BEAM_PIN):
#        record_video(video_data, box_id, video_duration)


# Handler function for manual Ctrl + C cancellation
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


GPIO.setmode(GPIO.BCM)
GPIO.setup(BEAM_PIN_lead, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BEAM_PIN_rear, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False)
#GPIO.setup(REC_LED, GPIO.OUT)

# pull_up_down parameter not valid for outputs
# Pins used for GPIO.add_event_detect need to be set up as inputs, but cannot change the
# value of a pin using GPIO.input, only GPIO.output (which requires pin to be set up as an output)
# GPIO.setup(VIDEO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(VIDEO_PIN, GPIO.OUT)
GPIO.output(VIDEO_PIN, GPIO.LOW)

GPIO.add_event_detect(BEAM_PIN_lead, GPIO.FALLING,
                      callback=lambda x: detect_beam_breaks_callback(BEAM_PIN_lead, "lead"), bouncetime=100)

<<<<<<< HEAD
GPIO.add_event_detect(BEAM_PIN_rear, GPIO.FALLING,
                      callback=lambda x: detect_beam_breaks_callback(BEAM_PIN_rear, "rear"), bouncetime=100)

# Does not work since pin needs to be an input (see above)
#GPIO.add_event_detect(VIDEO_PIN, GPIO.FALLING,
#                      callback=lambda x:detect_trigger_callback(VIDEO_PIN), bouncetime=100)

# Cannot have multple edge detection functions running for the same pin
# RuntimeError: Conflicting edge detection already enabled for this GPIO channel
#GPIO.add_event_detect(BEAM_PIN_rear, GPIO.FALLING,
#                      callback=lambda x:detect_trigger_callback(BEAM_PIN_rear), bouncetime=100)
=======
GPIO.add_event_detect(BEAM_PIN_lead, GPIO.FALLING,
                      callback=lambda x: detect_beam_breaks_callback(BEAM_PIN_lead, "lead"), bouncetime=100)
GPIO.add_event_detect(BEAM_PIN_rear, GPIO.FALLING,
                      callback=lambda x: detect_beam_breaks_callback(BEAM_PIN_rear, "rear"), bouncetime=100)
>>>>>>> 952fc981b1f7dac97792713eee6f53ab3a58dbfa

try:
    while True:
        pass
<<<<<<< HEAD
        if GPIO.input(VIDEO_PIN):
            record_video(video_data, box_id, video_duration)
=======
>>>>>>> 952fc981b1f7dac97792713eee6f53ab3a58dbfa

except KeyboardInterrupt:
    logging.info('exiting IRBB')
    GPIO.cleanup()

finally:
    GPIO.cleanup()
