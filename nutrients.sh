#!/bin/bash

# Run the Python script
python3 "/Users/avi/Documents/personal code/nutrients/draw.py"

# Kill Preview if it's running
pkill Preview

# Display the images
open "/Users/avi/Documents/personal code/nutrients/spider_charts.png"
open "/Users/avi/Documents/personal code/nutrients/nutrient_charts.png"
open "/Users/avi/Documents/personal code/nutrients/nutrients.png"
