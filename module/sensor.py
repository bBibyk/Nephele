from picamera2 import Picamera2, Preview
from utils import *
from time import sleep
from os import remove

class Sensor:
    def __init__(self, configurations, pc_time : time):
        self.metadata = None
        self.update_configurations(configurations)
        self.sync_time(pc_time)
        self.picam2=Picamera2()
    
    def update_configurations(self, configurations):
        
        self.configurations = None
        if configurations is not None:
            self.configurations = configurations
            logger("Sensor","Configurations loaded.")
        else:
            logger("Sensor","No configurations provided.")
    
    def sync_time(self, pc_time : time):    
        self.module_time = time.localtime(pc_time)
        
    def start_preview(self):
        
        self.picam2.start_preview(Preview.NULL)
        self.picam2.start()
        sleep(1)

    def stop_preview(self):
        self.picam2.stop_preview()
    
    def quick_capture(self):
        image_name = "Test.jpg"
        self.picam2.start_and_capture_file(image_name)
        logger("Sensor", f"Image captured: {image_name}")
        self.stop()
        
    def __get_path(self):
        
        timestamp : str = time.strftime("%Y%m%d%H%M%S", self.module_time)
        image_name_format : str = self.configurations['module']['format']['image_name']
        image_name : str = image_name_format.format(timestamp=timestamp)
        image_path = get_script_directory()+self.configurations['module']['shots'] + image_name  
        return image_path, image_name
        
    def capture_image(self):
        
        image_path, image_name = self.__get_path()
        try:    
            self.metadata = self.picam2.capture_file(image_path)
            logger("Sensor", f"Image captured: {image_name}")
        
        except Exception as e:
            logger("Sensor", "Error during capture.", e)
            self.stop()

    def check_brightness(self):
        if self.metadata is not None:
            brightness_threshold = self.configurations['sensor']['brightness_threshold']
            if self.metadata['Lux']<brightness_threshold:
                return False
        return True
    
    def __night_mode(args):
        pass
    
    def enable_night_mode(args):
        pass
                
    
    def stop(self):
        self.picam2.close()

if __name__ == '__main__':
    
    import time
    
    configurations = load_configurations("default.yaml")
    test_time = time.time()
    
    
    # print("Test quick capture.")
    
    sensor = Sensor(configurations=configurations, pc_time=test_time)
    # sensor.quick_capture()

    print("Test classic capture")
    sensor.start_preview()
    sensor.capture_image()
    for i in range(3):
        sensor.sync_time(time.time())
        sensor.capture_image()
        sleep(3)
    sensor.stop()
    