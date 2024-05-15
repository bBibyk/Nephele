#!/usr/bin/bash

PROCESS_NAME="python3 ./connexion_client.py" # Remplacer le chemin ici

while true
do
    if ! pgrep -f "$PROCESS_NAME" > /dev/null
    then
    	echo "$PROCESS_NAME n'est pas en cours d'exécution. Redémarrage..."
        python3 ./connexion_client.py # Et ici aussi
    fi
    sleep 5
done
