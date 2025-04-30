import subprocess
import sys
ha = str(sys.argv[1])
proxmox = str(sys.argv[2])
password = str(sys.argv[3])

print("homeassitant: "+homeassitant)
print("proxmox: "+proxmox)
print("password: "+password)

runningproxmox=subprocess.getoutput("cat /etc/apt/sources.list")
if "download.proxmox.com" in runningproxmox:
    print("Running local")
    servercommand=["#!/bin/bash","clear","tempfile=$(mktemp)","""dialog --title "Local: Choose A Machine To Connect To: IP:"""+proxmox+""" " --menu "" 1920 1080 1080 \ """]
    clientcommand=["#!/bin/bash","clear","tempfile=$(mktemp)","""dialog --title "Local: Choose A Machine To Connect To: IP:"""+proxmox+"""" --menu "" 1920 1080 1080 \ """]
    
    print(servercommand)
    
    print(str("sshpass -p "+password+" ssh root@"+proxmox+" dir /etc/pve/local/qemu-server/"))
    output=(subprocess.getoutput("dir /etc/pve/local/qemu-server/"))
    output=output.replace(" ","")
    output=output.split(".conf")
    machines=[]
    for item in output:
        item=item.replace(" ","")
        try:
            #print(item)
            item=int(item)
            #print(item)
        except:
            item=0
        machines.append(item)
    
    machines.sort()
    machines = machines[1:]
    #print(str(machines))
    for item in machines:
        if item >= 100 and item <= 199:
            print("\nSERVER: "+str(item))
            name=subprocess.getoutput("cat /etc/pve/local/qemu-server/"+str(item)+".conf")
            name=name.split("name: ")
            name=name[1]
            name=name.split("\n")
            name=name[0]
            #import sys
            #sys.exit()
            servercommand.append(str(item)+""" " """ +name+ """ " """ + " \ ")
        else:
            print("\nClient: "+str(item))
            name=subprocess.getoutput("cat /etc/pve/local/qemu-server/"+str(item)+".conf")
            name=name.split("name: ")
            name=name[1]
            name=name.split("\n")
            name=name[0]
            clientcommand.append(str(item)+""" " """ +name+ """ " """ + " \ ")
    
    servercommand.append("""999 "N\A" 2> "$tempfile" """)
    clientcommand.append("""999 "N\A" 2> "$tempfile" """)
    
    servercommand.append("""selected_number=$(cat "$tempfile") """)
    clientcommand.append("""selected_number=$(cat "$tempfile") """)
    
    
    servercommand.append("""rm "$tempfile" """)
    clientcommand.append("""rm "$tempfile" """)
    
    servercommand.append("""./thinclient.sh "$selected_number" '"""+proxmox +"' '"+password+"'")
    clientcommand.append("""./thinclient.sh "$selected_number" '"""+proxmox +"' '"+password+"'")
    
    newservercommand=[]
    for item in servercommand:
        item=item.replace("\ ","\#")
        item=item.replace("#","")
        newservercommand.append(item)
    
    newclientcommand=[]
    for item in clientcommand:
        item=item.replace("\ ","\#")
        item=item.replace("#","")
        newclientcommand.append(item)
    print(newservercommand)
    with open('select-server.sh', 'w') as file:
        file.writelines(f"{item}\n" for item in newservercommand)
    with open('select-client.sh', 'w') as file:
        file.writelines(f"{item}\n" for item in newclientcommand)
    subprocess.getoutput("chmod +x ./select-server.sh")
    subprocess.getoutput("chmod +x ./select-client.sh")
else:
    print("Running Remote")

    servercommand=["#!/bin/bash","clear","tempfile=$(mktemp)","""dialog --title "Remote: Choose A Machine To Connect To: IP:"""+proxmox+""" " --menu "" 1920 1080 1080 \ """]
    clientcommand=["#!/bin/bash","clear","tempfile=$(mktemp)","""dialog --title "Remote: Choose A Machine To Connect To: IP:"""+proxmox+"""" --menu "" 1920 1080 1080 \ """]
    
    print(servercommand)
    
    print(str("sshpass -p "+password+" ssh root@"+proxmox+" dir /etc/pve/local/qemu-server/"))
    output=(subprocess.getoutput("sshpass -p "+password+" ssh admin@"+proxmox+" dir /etc/pve/local/qemu-server/"))
    output=output.replace(" ","")
    output=output.split(".conf")
    machines=[]
    for item in output:
        item=item.replace(" ","")
        try:
            #print(item)
            item=int(item)
            #print(item)
        except:
            item=0
        machines.append(item)
    
    machines.sort()
    machines = machines[1:]
    #print(str(machines))
    for item in machines:
        if item >= 100 and item <= 199:
            print("\nSERVER: "+str(item))
            name=subprocess.getoutput("sshpass -p "+password+" ssh root@"+proxmox+" cat /etc/pve/local/qemu-server/"+str(item)+".conf")
            name=name.split("name: ")
            name=name[1]
            name=name.split("\n")
            name=name[0]
            #import sys
            #sys.exit()
            servercommand.append(str(item)+""" " """ +name+ """ " """ + " \ ")
        else:
            print("\nClient: "+str(item))
            name=subprocess.getoutput("sshpass -p "+password+" ssh root@"+proxmox+" cat /etc/pve/local/qemu-server/"+str(item)+".conf")
            name=name.split("name: ")
            name=name[1]
            name=name.split("\n")
            name=name[0]
            clientcommand.append(str(item)+""" " """ +name+ """ " """ + " \ ")
    
    servercommand.append("""999 "N\A" 2> "$tempfile" """)
    clientcommand.append("""999 "N\A" 2> "$tempfile" """)
    
    servercommand.append("""selected_number=$(cat "$tempfile") """)
    clientcommand.append("""selected_number=$(cat "$tempfile") """)
    
    
    servercommand.append("""rm "$tempfile" """)
    clientcommand.append("""rm "$tempfile" """)
    
    servercommand.append("""./thinclient.sh "$selected_number" '"""+proxmox +"' '"+password+"'")
    clientcommand.append("""./thinclient.sh "$selected_number" '"""+proxmox +"' '"+password+"'")
    
    newservercommand=[]
    for item in servercommand:
        item=item.replace("\ ","\#")
        item=item.replace("#","")
        newservercommand.append(item)
    
    newclientcommand=[]
    for item in clientcommand:
        item=item.replace("\ ","\#")
        item=item.replace("#","")
        newclientcommand.append(item)
    print(newservercommand)
    with open('select-server.sh', 'w') as file:
        file.writelines(f"{item}\n" for item in newservercommand)
    with open('select-client.sh', 'w') as file:
        file.writelines(f"{item}\n" for item in newclientcommand)
    subprocess.getoutput("chmod +x ./select-server.sh")
    subprocess.getoutput("chmod +x ./select-client.sh")
