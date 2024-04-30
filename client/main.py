import connexion_client as cc
from utils import *
import time

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