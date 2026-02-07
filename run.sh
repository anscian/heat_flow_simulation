#!/usr/bin/bash

# Create python virtual environment
python3 -m venv .my_env

# Activate it
. ./.my_env/bin/activate

# Install the requirements
pip3 install -r ./requirements.txt

# Run the animation generation (set to save in org, can be changed to just display)
python3 ./code.py 10 15 0.1 # outputs how much time it takes to get the whole tube below 100 deg

# Speedup the generated animation to desired video length in seconds
python3 ./speedup.py ./org/r10th15dt0.1.mp4 ./res/r10th15dt0.1.mp4 10 # 10 sec video
