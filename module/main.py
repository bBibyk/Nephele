import connection_server as cs 
import sensor as ss
import signal
import os
from utils import *
from time import sleep



configurations = load_configurations("default.yaml")
pc_time = time.time()
delay = configurations['module']['delay']
time_interval = configurations['module']['clock']['time_interval']
config_interval = configurations['module']['clock']['conf_interval']

def sigint_handler(sig, frame):
    global connection, sensor
    
    connection.disconnect_client()
    connection.disconnect()
    sensor.close()
    logger("Main", "Exiting...")
    exit()
    
def sigalrm_handler(sig, frame):
    sensor.capture_image()

    
def sync_time():
    global pc_time
    if connection.connect():
        connection.send_request("<TIME>")
        pc_time = connection.recv_time()
        connection.disconnect_client()
        sensor.sync_time(pc_time)
        logger("Main", "Connection established. Synchronizing time.")
    else:
        connection.disconnect_client()
        pc_time = time.time()
        sensor.sync_time(pc_time)
        logger("Main", "Connection failed. Couldn't synchronize time.")
    
    
def sync_config():
    global configurations
    
    #TODO loop until config parameter
    if connection.connect():
        connection.send_request("<PARA>")
        configurations = connection.recv_configurations()
        connection.disconnect_client()
        sensor.update_configurations(configurations)
        logger("Main", "Connection established. Updating configurations.")
    else:
        connection.disconnect_client()
        logger("Main", "Connection failed. Couldn't upload new configurations.")
        
    
def send_photo(filename : str):
    path = get_script_directory()+configurations['module']['shots']
    dirs = os.listdir(path)
    for file in dirs:
        if connection.connect:
            connection.send_request("<PHOT>")
            connection.send_photo(file)
            connection.disconnect_client()
            logger("Main", f"Connection established. Sending photo {file}.")
            os.remove(file)
            logger("Main", f"Photo {file} removed from module storage.")
        else:
            logger("Main", "Connection failed. Couldn't send photos.")
            connection.disconnect_client()
            

def capture():
    
    sync_time_counter = time_interval
    sync_config_counter = config_interval
    while True:
        signal.alarm(delay)
        sync_config_counter +=1
        sync_time_counter +=1
        
        if sync_config_counter >= config_interval:
            sync_config()
            sync_config_counter = 0
            
        if sync_time_counter >= time_interval:
            sync_time()
            sync_time_counter = 0
        send_photo()
        signal.pause()
        

#Handle signal
signal.signal(signal.SIGALRM, sigalrm_handler)
signal.signal(signal.SIGINT, sigint_handler)

# Entity creation
connection = cs.Connection()
sensor = ss.Sensor(configurations=configurations, pc_time=pc_time)

#Starting camera
sensor.start_camera()

capture()

#Closing camera
sensor.close()

connection.disconnect()

        
#send_photo('./shots/*')
