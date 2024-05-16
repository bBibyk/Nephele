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
    signal.alarm(delay)

    
    
def sync_time(sync_type):
    """
    sync_type=0 -> auto-synchronization with module time
    
    sync_type=1 -> synchronization with pc time
    """
    global pc_time
    
    if sync_type:
        if connection.connect():
            connection.send_request("<TIME>")
            pc_time = connection.recv_time()
            connection.disconnect_client()
            sensor.sync_time(pc_time)
            logger("Main", "Synchronizing time.")
        else:
            connection.disconnect_client()
            sensor.sync_time()
            logger("Main", "Couldn't synchronize time.")
    else:
        sensor.sync_time()
    
    
def sync_configuration():
    global configurations, time_interval, config_interval, delay
    
    if connection.connect():
        connection.send_request("<PARA>")
        tmp_configuration = connection.recv_configurations()
        if tmp_configuration is not None:
            logger("Main", "Updating configurations.")
            configurations = tmp_configuration
            sensor.update_configurations(configurations)
            delay = configurations['module']['delay']
            time_interval = configurations['module']['clock']['time_interval']
            config_interval = configurations['module']['clock']['conf_interval']
        connection.disconnect_client()
    else:
        connection.disconnect_client()
        logger("Main", "Couldn't upload new configurations.")
        
    
def send_photo():
    path = get_script_directory() + configurations['module']['shots']
    dirs = os.listdir(path)
    for file in dirs:
        if connection.connect():
            connection.send_request("<PHOT>")
            if connection.send_photo(file):
                logger("Main", f"Sending photo {file}.")
                os.remove(path + file)
                logger("Main", f"Photo {file} removed from module storage.")
            connection.disconnect_client()

        else:
            logger("Main", "Couldn't send photos. Photo saved in module/shots/")
            connection.disconnect_client()
            

def capture():
    sync_time_counter = time_interval
    sync_config_counter = config_interval
    sigalrm_handler(None, None)
    while True:
        sync_config_counter +=1
        sync_time_counter +=1
        
        if sync_config_counter >= config_interval:
            sync_configuration()
            sensor.stop()
            sync_config_counter = 0
            
        if sync_time_counter >= time_interval:
            sync_time(1)
            sync_time_counter = 0
        else:
            sync_time(0)
        
        send_photo()
        signal.pause()
        

#Handle signals
signal.signal(signal.SIGALRM, sigalrm_handler)
signal.signal(signal.SIGINT, sigint_handler)

# Entity creation
connection = cs.Connection()
sensor = ss.Sensor(configurations=configurations, pc_time=pc_time)

capture()

#Closing camera
sensor.close()

connection.disconnect()

        
#send_photo('./shots/*')
