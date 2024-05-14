import connection_client as cc
import signal
from utils import *
import time

def sigint_handler(sig, frame):
    global connection
    connection.disconnect()
    logger("Main", "Exiting...")
    exit()

signal.signal(signal.SIGINT, sigint_handler)
    
connection = cc.Connection()
connected = False


while True :
    try:
        connected = connection.connect()
        if connected:
            connection.request()
            connection.disconnect()
        else:
            time.sleep(5)
    except Exception as e:
        logger("Main", "Unexpected exception.", e)