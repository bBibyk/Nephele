import module.connexion_server as cs 
import module.sensor as ss
from utils import *

def sigint_handler(sig, frame):
    logger("Main", "Exiting...")
    connection.disconnect()
    # TODO : sortir correctement
    
def send_photo(filename : str):
    #TODO
    pass

def get_configurations():
    #TODO
    pass

def get_time():
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

sensor.start_capture()
#send_photo('./shots/*')
