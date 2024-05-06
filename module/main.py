import module.connexion_server as cs 
import module.sensor as ss
import signal
import threading
from utils import *
from time import sleep

configs = None
pc_time = None
delay = configs['module']['delay']
sync_delay = configs['module']['clock']['sync_interval']

def sigint_handler(sig, frame):
    logger("Main", "Exiting...")
    sensor.close()
    connection.disconnect()
    # TODO : sortir correctement
    
def sigalrm_handler(sig, frame):
    sensor.capture_image()
    
def sync():
    global pc_time
    while True:
        pc_time = connection.recv_time()
        sensor.sync_time(pc_time)
        sleep(sync_delay)
    
def capture():
    while True:
        signal.alarm(delay)
        signal.pause()
        
def send():
    send_photo()
    
def send_photo(filename : str):
    #TODO
    pass

# Entity creation
connection = cs.Connexion()
sensor = ss.Sensor(configurations=configs, pc_time=pc_time)
#Handle signal

#While loop TODO
connection.connect()
configs = connection.recv_configurations()
connection.disconnect_client()

#for i in range(config_update_frequency):
connection.connect()
pc_time = connection.recv_time()
connection.disconnect_client()
#TODO reste du script...

#Starting camera
sensor.start_camera()

signal.signal(signal.SIGALRM, sigalrm_handler)

synchronizing_thread = threading.Thread(target=sync)
capturing_thread = threading.Thread(target=capture)
sending_thread = threading.Thread(target=send)

synchronizing_thread.start()
capturing_thread.start()
sending_thread.start()

#Exiting

#Waiting untill all threads join
synchronizing_thread.join()
capturing_thread.join()
sending_thread.join()

#Closing camera
sensor.close()

        
#send_photo('./shots/*')
