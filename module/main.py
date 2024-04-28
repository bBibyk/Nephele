import module.connexion_server as cs 
import module.sensor as ss

connection = cs.Connexion()
configs = connection.recv_configurations()
pc_time = connection.recv_time()
sensor = ss.Sensor(configurations=configs, pc_time=pc_time)

sensor.start_capture()
#send_photo('./shots/*')

