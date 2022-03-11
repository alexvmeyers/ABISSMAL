#!/bin/bash
##
 # Created by PyCharm
 # Author: nmoltta
 # Project: ParentalCareTracking
 # Date: 03/08/2022
##

user_name=$(whoami)
location=
python_v=

irbb_file="/Modules/IRBB.py"
irbb_command="${python_v} ${location}${irbb_file}"

temp_file="/Modules/Temp.py"
temp_command="${python_v} ${location}${temp_file}"

rfid_file="/Modules/RFID.py"
rfid_command="${python_v} ${location}${rfid_file}"

backups_file="/Modules/Backups.py"
backups_command="${python_v} ${location}${backups_file}"

monitor_file="/Modules/monitor.py"
monitor_command="${python_v} ${location}${monitor_file}"

find Modules/ -type f -exec chmod 644 {} \;
chown -R "${user_name}" .

echo "$(date): PCT Starting cron as ${user_name}"
screen -ls | grep temp | cut -d. -f1 | awk '{print $1}' | xargs kill
screen -ls | grep irbb | cut -d. -f1 | awk '{print $1}' | xargs kill
screen -ls | grep rfid | cut -d. -f1 | awk '{print $1}' | xargs kill
screen -ls | grep backup | cut -d. -f1 | awk '{print $1}' | xargs kill
screen -ls | grep monitor | cut -d. -f1 | awk '{print $1}' | xargs kill
echo "$(date): PCT Killed screens"
sleep 1s
screen -dmS temp bash -c "${temp_command}"
echo "$(date): PCT Started screen: temp"
sleep 1s
screen -dmS irbb bash -c "${irbb_command}"
echo "$(date): PCT Started screen: irbb"
sleep 1s
screen -dmS rfid bash -c "${rfid_command}"
echo "$(date): PCT Started screen: rfid"
sleep 1s
screen -dmS backup bash -c "${backups_command}"
echo "$(date): PCT Started screen: backup"
sleep 1s
screen -dmS monitor bash -c "${monitor_command}"
echo "$(date): PCT Started screen: monitor"
sleep 2s
screen -list
echo "$(date): Ran PCT cron job"