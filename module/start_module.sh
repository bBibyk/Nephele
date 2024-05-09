#!/usr/bin/bash

PROCESS_NAME="python3 ./connexion_server.py"

while true
do
    if ! pgrep -f "$PROCESS_NAME" > /dev/null
    then
    	echo "$PROCESS_NAME n'est pas en cours d'exécution. Redémarrage..."
        python3 ./connexion_server.py   
    fi
    sleep 5
done
