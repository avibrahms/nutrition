#!/bin/bash

# Install packages if they're not installed
# export PATH=$PATH:/Users/avi/Library/Python/3.9/bin
# curl https://bootstrap.pypa.io/get-pip.py | python3
# pip install pyperclip

# python3 "/Users/avi/Documents/personal code/nutrients/install.py"
# pip install -r "/Users/avi/Documents/personal code/nutrients/requirements.txt"
# Run the Python script
python3 "/Users/avi/Documents/personal code/nutrients/draw.py"

# Kill Preview if it's running
pkill Preview

# Display the images
# open "/Users/avi/Documents/personal code/nutrients/nutrient_charts.png"
# open "/Users/avi/Documents/personal code/nutrients/spider_charts.png"
open "/Users/avi/Documents/personal code/nutrients/nutrients.png"
