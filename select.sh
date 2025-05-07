#!/bin/bash
python3.11 ./select-make.py $1 $2 $3
clear
# Create a temporary file to store the selected number
tempfile=$(mktemp)

# Use dialog to create a menu for selecting a number
#dialog --title "Select a Number" --menu "Choose A Machine To Connect To:" 100 70 30 \
dialog --title "Choose A System Type To Connect To: ARgs: $1 $2 $3" --menu "" 1920 1080 1080 \
100 "Server" \
101 "Client" \
102 "HomeAssiant firefox " \
103 "ProxMox firefox  " 2> "$tempfile"

# Read the selected number from the temporary file
selected_number=$(cat "$tempfile")

# Remove the temporary file
rm "$tempfile"

# Pass the selected number to another script
echo "$selected_number"
if [[ $selected_number == *"100"* ]]; then
    ./select-server.sh
elif [[ $selected_number == *"101"* ]]; then
    ./select-client.sh
elif [[ $selected_number == *"102"* ]]; then
    firefox $1:8123/dashboard-pi/0
elif [[ $selected_number == *"103"* ]]; then
    firefox $2:8006
else
    exit
fi
