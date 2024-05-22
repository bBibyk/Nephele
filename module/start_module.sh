#!/usr/bin/bash

PROCESS_NAME="python3 /home/nephele/Nephele/module/main.py" # Remplacer le chemin ici

sudo ip link set eth0 down
sudo ip addr add 192.168.1.101/24 dev eth0
sudo ip link set eth0 up

while true
do
    if ! pgrep -f "$PROCESS_NAME" > /dev/null
    then
    	echo "$PROCESS_NAME n'est pas en cours d'exécution. Redémarrage..."
        python3 /home/nephele/Nephele/module/main.py # Et ici aussi
    fi
    sleep 5
done
