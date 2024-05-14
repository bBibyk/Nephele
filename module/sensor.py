from picamera2 import Picamera2, Preview
from utils import *
from time import sleep
import os

class Sensor:
    def __init__(self, configurations, pc_time : time):
        self.update_configurations(configurations)
        self.sync_time(pc_time)
        self.picam2=Picamera2()
        self.metadata = None
        self.module_time_specifier = ""
    
    def update_configurations(self, configurations):
        
        self.configurations = None
        if configurations is not None:
            self.configurations = configurations
            logger("Sensor","Configurations loaded.")
        else:
            logger("Sensor","No configurations provided.")
    
    def sync_time(self, pc_time : time=None):    
        if pc_time is None:
            self.module_time = time.time()
            self.module_time_specifier="m"
        else:
            self.module_time = time.localtime(pc_time)
            self.module_time_specifier=""
            
    def start_camera(self):
        if not self.picam2.started:  
            try:
                self.picam2.start_preview(Preview.NULL)
                self.picam2.start()
                sleep(1)
                logger("Sensor", "Picamera initialized.")
            except Exception as e:
                logger("Sensor", "Error during preview initialization.", e)
            
        else:
            logger("Sensor", "Picamera preview already started.")

    def quick_capture(self):
        image_name = "Test.jpg"
        image_path = get_script_directory()+self.configurations['module']['shots'] + image_name
        try:    
            if self.picam2.started:
                self.picam2.stop()
            self.picam2.start_and_capture_file(image_path)
            logger("Sensor", f"Test image captured: {image_name}")
            self.close()
        
        except Exception as e:
            logger("Sensor", "Error during test image capture.", e)
            self.close()
        
    def __get_path(self):
        
        try:
            timestamp : str = time.strftime(self.configurations['module']['naming']['timestamp'], self.module_time)
            image_name_format : str = self.configurations['module']['naming']['image_name']
            image_name : str = self.module_time_specifier + image_name_format.format(timestamp=timestamp)
            image_path = get_script_directory()+self.configurations['module']['shots'] + image_name  
            return image_path, image_name
        except Exception as e:
            logger("Sensor", "Couldn't get image path.", e)
        
    def capture_image(self):
        
        image_path, image_name = self.__get_path()
        # if not self.picam2.started:
        #     logger("Sensor", "Camera preview is not active.")
        #     return
            
        try:    
            self.metadata = self.picam2.capture_file(image_path)
            logger("Sensor", f"Image captured: {image_name}")
            if not self.check_brightness():
                os.remove(image_path)
                logger("Sensor", f"Brightness does not satistfy the given threshold. Image deleted: {image_name}")
        except Exception as e:
            logger("Sensor", "Error during capture.", e)
            self.close()

    def check_brightness(self):
        if self.metadata is not None:
            brightness_threshold = self.configurations['module']['brightness_threshold']
            if self.metadata['Lux']>brightness_threshold:
                return True
        return False
    
    def __night_mode(args):
        pass
    
    def enable_night_mode(args):
        pass
                
    
    def close(self):
        self.picam2.close()

if __name__ == '__main__':
    
    import time
    
    configurations = load_configurations("default.yaml")
    test_time = time.time()
    
    sensor = Sensor(configurations=configurations, pc_time=test_time)
    # sensor.quick_capture()

    print("Test classic capture")
    sensor.start_camera()
    for i in range(3):
        sensor.sync_time(time.time())
        sensor.capture_image()
        print(sensor.metadata['Lux'])
        sleep(3)
    sensor.close()
