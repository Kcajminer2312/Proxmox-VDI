The is some scripts to connect to Proxmox VMs VIA SPICE

Also has the ablity to display a home assistant dashboard

set the home assistant IP to 0.0.0.0 if not using

run command ./select.sh as shown below

to use this the Users root and admin must be created and have the same password

admin need to be added to sudoers like shown below
keep the rest of the file just change whats shown
```bash
# User privilege specification
root    ALL=(ALL:ALL) ALL
admin   ALL=(ALL:ALL) NOPASSWD:ALL
```

for the notification service add
sudo nano /usr/share/dbus-1/services/org.freedesktop.Notifications.service
```bash
[D-BUS Service]
Name=org.freedesktop.Notifications
Exec=/usr/lib/notification-daemon/notification-daemon
```

You must have the following installed: xserver-xorg x11-xserver-utils xinit openbox virt-viewer libnotify-bin
```bash
sudo apt install -y xserver-xorg x11-xserver-utils xinit openbox virt-viewer libnotify-bin
```
the ./select.sh script uses the following arguments
```bash
./select.sh (HomeAssistant IP) (Proxmox IP) (Password)
```

or add this to /etc/xdg/openbox/autostart
```bash
#Allow exit of X server with ctrl+alt+backspace
#If you don't want to let the user terminate/restart, leave this out
#You can always `killall xinit` via SSH to return to a terminal
setxkbmap -option terminate:ctrl_alt_bksp

#Start the shell script we already wrote in our home directory
#Runloop restarts the thin client (new access token, new config file)
#if the session is terminated (i.e the VM is inaccessible or restarts)
#User will see a black screen with a cursor during this process
while true
do
notify-send "Update"
sudo apt update
notify-send "Install Git"
sudo apt install -y git
notify-send "Git clone"
git clone https://github.com/Kcajminer2312/Proxmox-VDI.git
notify-send "Cd"
cd Proxmox-VDI/
notify-send "Xterm"

chmod +x ./*.sh

xterm -fullscreen -e ./select.sh (HomeAssistant IP) (Proxmox IP) (Password)
cd ..
sudo rm -frv ./Proxmox-VDI
```
