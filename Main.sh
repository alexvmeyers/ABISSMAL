#!/bin/bash
##
 # Created by PyCharm
 # Author: nmoltta
 # Project: Abissmal
 # Date: 12/08/2021
##

RED='\033[0;31m'
NC='\033[0m'
BIGreen='\033[1;92m'
Green='\033[0;92m'
Yellow='\033[0;93m'
Blue='\033[0;94m'
Purple='\033[0;95m'
Cyan='\033[0;96m'

user_name=$(whoami)
location=$(pwd)
python_v=$(which python)
cron_path="${location}/cron.sh"

irbb_file="/Modules/IRBB.py"
irbb_command="${python_v} ${location}${irbb_file}"

video_file="/Modules/Video.py"
video_command="${python_v} ${location}${video_file}"

validation_file="/Modules/alt_video.py"
validation_command="${python_v} ${location}${validation_file}"

temp_file="/Modules/Temp.py"
temp_command="${python_v} ${location}${temp_file}"

rfid_file="/Modules/RFID.py"
rfid_command="${python_v} ${location}${rfid_file}"

backups_file="/Modules/Backups.py"
backups_command="${python_v} ${location}${backups_file}"

monitor_file="/Modules/monitor.py"
monitor_command="${python_v} ${location}${monitor_file}"

helper_file="Modules/helper.py"

v='"Video"'
a='"Validation"'
r='"RFID"'
i='"IRBB"'
t='"Temp"'
comma=', '
modules_string=''
selected=false

echo -e "${Green}
           ____ _____  _____ _____ __  __          _
     /\   |  _ \_   _|/ ____/ ____|  \/  |   /\   | |
    /  \  | |_) || | | (___| (___ | \  / |  /  \  | |
   / /\ \ |  _ < | |  \___  \___ \| |\/| | / /\ \ | |
  / ____ \| |_) || |_ ____) |___) | |  | |/ ____ \| |____
 /_/    \_\____/_____|_____/_____/|_|  |_/_/    \_\______|

${NC}"
echo -e "${Green}Automated behavioral tracking by integrating sensors that survey movements around a target location${NC}"
echo -e "${Blue}Repository:${NC}  ${Blue}https://github.com/lastralab/abissmal"${NC}
echo -e "${Blue}Date:${NC}        ${Blue}November 2021 - 2023${NC}"
echo -e "${Blue}Authors:${NC}     ${Cyan}Molina, T.${NC} & ${Cyan}Smith-Vidaurre, G.${NC}"
echo ""

echo -e "${Yellow}Setting permissions for user:${NC} ${user_name}"
echo ""
find Modules/ -type f -exec chmod 644 {} \;
chown -R "${user_name}" .
mkdir -p /home/pi/log/
filename="/home/pi/log/abissmal_cron.log"
[[ -f ${filename} ]] || touch ${filename}
echo -e "${Yellow}/home/pi/log/abissmal_cron.log ready to log cron jobs as${NC} ${user_name}"
echo ""

echo -e "${Cyan}Enter first letter of the modules to track:${NC}"
echo -e "${Cyan}Example: virt ${NC}${Purple}(V/v)ideo/(R/r)fid/(I/i)rbb/(T/t)emp${NC}"
echo -e "${RED}To run Validation Video only, enter (A/a)${NC}"
read -r modules

sed -i "s#^modules=.*#modules=\"$modules\"#" "${cron_path}"

if [[ $modules == *"A"* || $modules == *"a"* ]];
then
    modules_string="${modules_string}${a}${comma}"
    selected=true

    echo -e "${Cyan}Enter hour number to start validation videos (in 24hrs format)${NC}"
    echo -e "${Cyan}Example: 7:00am = 7 / 11:00pm = 23. Minutes not allowed.${NC}"
    read -r start_video
    echo -e "${Cyan}Enter hour to stop validation videos${NC}"
    read -r end_video
    sed -i "s#^video_time_range =.*#video_time_range = [$start_video, $end_video]#" "${location}${validation_file}"
    echo -e "${Green}Recording time set from $start_video:00 to $end_video:00hrs${NC}"

    echo -e "${Cyan}Enter duration of each video in seconds${NC}"
    echo -e "${Cyan}Example: 5 seconds = 5 / 2 minutes = 120${NC}"
    read -r duration
    sed -i "s#^record_duration =.*#record_duration = $duration" "${location}${validation_file}"
    echo -e "${Green}Set video duration to $duration seconds${NC}"

    echo -e "${Cyan}Enter hour to start the LED recording indicator (in 24hrs format)${NC}"
    echo -e "${Cyan}Example: 7:00am = 7 / 11:00pm = 23. Minutes not allowed.${NC}"
    read -r start_led
    echo -e "${Cyan}Enter hour to stop LED indicator${NC}"
    read -r end_led
    echo -e "${Green}LED recording indicator set from $start_led:00 to $end_led:00hrs${NC}"
    sed -i "s#^LED_time_range =.*#LED_time_range = [$start_led, $end_led]#" "${location}${validation_file}"

    echo -e "${Purple}Enabled Validation Videos${NC}"
    echo -e "Starting screen name: ${Cyan}validation${NC}..."
    sleep 1s
    screen -dmS validation bash -c "${validation_command}"
    echo ""
else
  if [[ $modules == *"V"* || $modules == *"v"* ]];
  then
      modules_string="${modules_string}${v}${comma}"
      selected=true
      echo -e "${Purple}Enabled Video${NC}"
      echo -e "Starting screen name: ${Cyan}video${NC}..."
      sleep 1s
      screen -dmS video bash -c "${video_command}"
      echo ""
  fi

  if [[ $modules == *"I"* || $modules == *"i"* ]];
  then
      modules_string="${modules_string}${i}${comma}"
      selected=true
      echo -e "${Purple}Enabled IRBB${NC}"
      echo -e "Starting screen name: ${Cyan}irbb${NC}..."
      sleep 1s
      screen -dmS irbb bash -c "${irbb_command}"
      echo ""
  fi

  if [[ $modules == *"R"* || $modules == *"r"* ]];
  then
      modules_string="${modules_string}${r}${comma}"
      selected=true
      echo -e "${Purple}Enabled RFID${NC}"
      echo -e "Starting screen name: ${Cyan}rfid${NC}..."
      sleep 1s
      screen -dmS rfid bash -c "${rfid_command}"
      echo ""
  fi

  if [[ $modules == *"T"* || $modules == *"t"* ]];
  then
      modules_string="${modules_string}${t}${comma}"
      selected=true
      echo -e "${Purple}Enabled Temp${NC}"
      echo -e "Starting screen name: ${Cyan}temp${NC}..."
      sleep 1s
      screen -dmS temp bash -c "${temp_command}"
      echo ""
  fi
fi

if [[ $selected == true ]];
then
  	sed -i "s/^modules.*/modules = [${modules_string}]/" "${helper_file}"
    echo -e "Starting screen name: ${Cyan}backup${NC}..."
    sleep 1s
    screen -dmS backup bash -c "${backups_command}"
    echo -e "Starting screen name: ${Cyan}monitor${NC}..."
    sleep 1s
    screen -dmS monitor bash -c "${monitor_command}"
    echo ""
    sleep 3s
    screen -list
    echo ""
    echo -e "To kill all detached screens, run:"
    echo -e "${BIGreen}screen -ls | grep Detached | cut -d. -f1 | awk '{print \$1}' | xargs kill${NC}"
    echo -e "To access a screen run:${Green} screen -r ${NC}${Purple}{name}${NC}"
    echo -e "To detach a screen press${Blue} Ctrl + A${NC} then type ${RED}:${NC} to enter command mode and use command ${RED}detach${NC}"
    echo ""
else
    echo ""
    echo -e "${RED}No modules were activated, please enter valid letters.${NC}"
    echo ""
fi
