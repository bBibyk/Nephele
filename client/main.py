import connexion_client as cc
import signal
from utils import *
import time

def sigint_handler(sig, frame):
    global connexion
    logger("Main", "Exiting...")
    connexion.disconnect()
    exit()

signal.signal(signal.SIGINT, sigint_handler)
    
connexion = cc.Connexion()
connected = False


while True :
    try:
        connected = connexion.connect()
        if connected:
            connexion.request()
            connexion.disconnect()
        else:
            time.sleep(5)
    except Exception as e:
        logger("Main", "Unexpected exception", e)