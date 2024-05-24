import connection_client as cc
import signal
from utils import *
import time

def sigint_handler(sig, frame):
    global connection
    connection.disconnect()
    logger("Main", "Exiting...")
    exit()

def sigalarm_handler(sig, frame):
    pass
    

signal.signal(signal.SIGINT, sigint_handler)
    
connection = cc.Connection()

refresh_configuration = 0


while True :
    if refresh_configuration >= 30:
        refresh_configuration = 0
        connection.update_configurations()
    try:
        logger("Main", "Connecting...")
        if connection.connect():
            connection.request()
            connection.disconnect()
        else:
            logger("Main", "Unable to connect. Retrying in 5 seconds...")
            time.sleep(5)
    except Exception as e:
        logger("Main", "Unexpected exception.", e)
    refresh_configuration += 1