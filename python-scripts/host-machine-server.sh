#!/usr/bin/env bash

'''
General Idea for this script is the following

# Direct to folder containing web files
cd ~/Documents/coding/projects/personal-portfolio-website/

# Use Python to create a local server on host machine
python3 -m http.server 8000

# Open run the server in host machine browser
http://localhost:8000
'''

# Configure port and location of server persistence
PORT=8000
DIR="$HOME/Documents/coding/projects/personal-portfolio-website"

# Start server in background
python3 -m http.server "$PORT" & SERVER_PID=$!

echo "Server started on http://localhost:#PORT (PID: $SERVER_PID)"

# Open in host machine browser
xdg-open "http://localhost:$PORT" >/dev/null 2>&1

# Keep script running
wait "$SERVER_PID"
