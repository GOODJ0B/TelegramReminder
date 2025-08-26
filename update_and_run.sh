#!/bin/bash

# Navigate to your project directory
cd /home/pi/TelegramReminder

# Perform a git pull to update the repository
git pull origin main

#uncomment to install requirement:
#pip install -r requirements.txt

# Run the Python script
/usr/bin/python3 script.py