from picamera2 import Picamera2
from utils import *
from time import sleep
import os

class Sensor:
    def __init__(self, configurations, pc_time : time):
        self.update_configurations(configurations)
        self.sync_time(pc_time)
        self.picam2=Picamera2()
        self.module_time_specifier = ""
    
    def update_configurations(self, configurations):

        if configurations is not None:
            self.configurations = configurations
            logger("Sensor","Configurations loaded.")
        else:
            logger("Sensor","No configurations provided.")
    
    def sync_time(self, pc_time : time=None):
        if pc_time is None:
            self.module_time_specifier="m"
        else:
            self.module_time_specifier=""
        
            
    def start_camera(self):

        if not self.picam2.started:
            try:
                width = self.configurations['module']['sensor']['output_size']['width']
                size = (width, int(width // (4/3)))
                bit_depth = self.configurations['module']['sensor']['bit_depth']

                still_configurations = self.picam2.create_still_configuration(main={'size':size},sensor={'output_size': size, 'bit_depth': bit_depth})
                self.picam2.configure(still_configurations)
        
                self.picam2.start()
                sleep(1)
                logger("Sensor", "Picamera initialized.")
            except Exception as e:
                logger("Sensor", "Error during preview initialization.", e)
            
        else:
            logger("Sensor", "Picamera preview already started.")
        
    def __get_path(self):
        
        try:
            timestamp : str = time.strftime(self.configurations['module']['naming']['timestamp'])
            image_name_format : str = self.configurations['module']['naming']['image_name']
            image_name : str = image_name_format.format(timestamp=timestamp, module_time_specifier=self.module_time_specifier)
            image_path = get_script_directory()+self.configurations['module']['shots'] + image_name  
            return image_path, image_name
        except Exception as e:
            logger("Sensor", "Couldn't get image path.", e)
        
    def capture_image(self):
        
        image_path, image_name = self.__get_path()
        metadata = None
        self.start_camera()
        try:    
            metadata = self.picam2.capture_file(image_path)
            logger("Sensor", f"Image captured: {image_name}")
            if not self.__check_brightness(metadata):
                os.remove(image_path)
                logger("Sensor", f"Brightness does not satistfy the given threshold. Image deleted: {image_name}")
        except Exception as e:
            logger("Sensor", "Error during capture.", e)
            self.close()
        
        return metadata


    def __check_brightness(self, metadata):
        if metadata is not None:
            brightness_threshold = self.configurations['module']['brightness_threshold']
            if metadata['Lux']>brightness_threshold:
                return True
        return False
    
    def stop(self):
        self.picam2.stop()
        
    def close(self):
        self.picam2.close()

if __name__ == '__main__':
    
    import time
    
    configurations = load_configurations("default.yaml")
    test_time = time.time()
    
    sensor = Sensor(configurations=configurations, pc_time=test_time)

    print("Test classic capture")
    sensor.start_camera()
    for i in range(3):
        sensor.sync_time(time.time())
        metadata = sensor.capture_image()
        print(metadata['Lux'])
        sleep(3)
    sensor.close()
