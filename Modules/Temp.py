# Created by PyCharm
# Author: nmoltta, gsvidaurre
# Project: ParentalCareTracking
# Date: 12/13/21

import os
import glob
import time
from datetime import datetime
import csv
import logging
from pathlib import Path
from helper import logger_setup
from helper import csv_writer
from helper import box_id
from time import sleep
from helper import email_alert

logger_setup('/home/pi/')

logging.error('Testing error log')

warn = 0
module = 'Temp'
header = ['chamber_id', 'year', 'month', 'day', 'time', 'degrees_Celsius', 'degrees_Farenheit']
temp_data = '/home/pi/Data_ParentalCareTracking/Temp'
logging.info('Started Temp')
print('Started Temp')
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = (temp_c * (9.0 / 5.0)) + 32.0
        return temp_c, temp_f


try:
    while True:
        dt = datetime.now()
        temp = read_temp()
        logging.info('Temperature sensor reading at:' + f"{dt:%H:%M:%S.%f}")
        print('Temperature sensor reading at:' + f"{dt:%H:%M:%S.%f}")
        csv_writer(str(box_id), module, temp_data, f"{dt.year}_{dt.month}_{dt.day}", header,
                   [box_id, f"{dt.year}", f"{dt.month}", f"{dt.day}", f"{dt:%H:%M:%S.%f}", temp[0], temp[1]])
        time.sleep(60)
except KeyboardInterrupt:
    logging.info('Exiting Temp')
except Exception as E:
    logging.error('Temp error: ' + str(E))
    print('Temp error: ' + str(E))
    email_alert('Temp', 'Error: ' + str(E))
