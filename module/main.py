import connection_server as cs 
import sensor as ss
import signal
import os
import time
from utils import *



configurations = load_configurations("default.yaml")
connection = None
pc_time = None
delay = configurations['module']['delay']
time_interval = configurations['module']['clock']['time_interval']
config_interval = configurations['module']['clock']['conf_interval']

sync_time_counter = time_interval
sync_config_counter = config_interval

def sigint_handler(sig, frame):
    global connection, sensor
    
    connection.disconnect_client()
    connection.disconnect()
    sensor.close()
    logger("Main", "Exiting...")
    exit()
    
def sigalrm_handler(sig, frame):
    global sync_config_counter
    global sync_time_counter

    sensor.capture_image()
    signal.alarm(delay)

    sync_config_counter +=1
    sync_time_counter +=1
    send_photo()
    
    if sync_config_counter >= config_interval:
        sync_configuration()
        sensor.stop()
        sync_config_counter = 1
        
    if sync_time_counter >= time_interval:
        sync_time()
        sync_time_counter = 1
        

def instantiate_connection():
    global connection
    if connection is None:
        try:
            connection = cs.Connection()
        except Exception as e:
            logger("Main", "Couldn't create connection entity.", e)
            return False
    return True
    
def sync_time():

    global pc_time

    if not instantiate_connection():
        sensor.sync_time()
        return
    if connection.connect():
        connection.send_request("<TIME>")
        pc_time = connection.recv_time()
        connection.disconnect_client()
        if pc_time is not None:
            string_format_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(pc_time))
            os.system("sudo date -s \"" + string_format_time + "\" > /dev/null")
            logger("Main", "Time set to " + string_format_time)
        logger("Main", "Synchronizing time.")
        sensor.sync_time(pc_time)
    else:
        connection.disconnect_client()
        sensor.sync_time()
        logger("Main", "Couldn't synchronize time.")
    
def sync_configuration():
    global configurations, time_interval, config_interval, delay
    
    if not instantiate_connection():
        return
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
    
    if not instantiate_connection():
        return
    
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
            return
            

def capture():
    sync_configuration()
    sync_time()
    send_photo()
    signal.alarm(4)
    while True:
        signal.pause()
        

#Handle signals
signal.signal(signal.SIGALRM, sigalrm_handler)
signal.signal(signal.SIGINT, sigint_handler)

instantiate_connection()

sensor = ss.Sensor(configurations=configurations, pc_time=pc_time)

capture()

#Closing camera
# sensor.close()

# connection.disconnect()

        
#send_photo('./shots/*')
