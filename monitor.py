# Created by PyCharm
# Author: nmoltta
# Project: ParentalCareTracking
# Date: 2/20/22

import subprocess
import logging
from Modules.helper import email_alert
from Modules.helper import logger_setup

logger_setup('/home/pi/')
modules = ['temp', 'video', 'rfid', 'irbb', 'backups']

logging.info('Starting Monitor script')
print('Starting Monitor script')


def monitor_screens():
    screens = str(subprocess.getoutput("screen -list"))
    for screen in screens:
        if screens.find(screen) == -1:
            email_alert(screen, 'Screen not running.')
            logging.error('Screen not running: ' + screen)
            print('Screen closed: ' + screen)


try:
    while True:
        monitor_screens()
except Exception as E:
    logging.error('Monitor error: ' + str(E))
    email_alert('Monitor', 'Error while monitoring screens: ' + str(E))
    print('Monitor error: ' + str(E))