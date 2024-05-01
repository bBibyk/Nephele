from picamera2 import Picamera2, Preview
from utils import *
from time import sleep
from os.path import join

class Sensor:
    def __init__(self, configurations, pc_time : time):
        self.update_configurations(configurations)
        self.__sync_time(pc_time)
        self.picam2=Picamera2()
    
    def update_configurations(self, configurations):
        
        self.configurations = None
        if configurations is not None:
            self.configurations = configurations
            logger("Sensor","Configurations loaded.")
        else:
            logger("Sensor","No configurations provided.")
    
    def __sync_time(self, pc_time : time):
        self.module_time = time.localtime(pc_time)
        
    def start_preview(self):
            
        self.config = self.picam2.create_preview_configuration()
        self.picam2.configure(self.config)
        self.picam2.start_preview(Preview.QTGL)
        self.picam2.start()
        sleep(1)

    def stop_preview(self):
        self.picam2.stop_preview()
    
    def quick_capture(self):
        image_name = "Test.jpg"
        self.picam2.start_and_capture_file(image_name)
        logger("Sensor", f"Image captured: {image_name}")
        
    def __name_image(self):
        
        timestamp : str = self.module_time.strftime("%Y%m%d%H%M%S")
        image_name_format : str = self.configurations['module']['format']['image_name']
        image_name : str = image_name_format.format(timestamp=timestamp)  
        return image_name
        
    def capture_image(self):
            try:
                self.start_preview()
                    
                image_name = self.__name_image()
                image_path = get_script_directory()+self.configurations['module']['shots'] + image_name
                image_path = join(self.configurations['module']['shots'], image_name)
                with self.picam2.capture_file(image_path):
                    logger("Sensor", f"Image captured: {image_name}")
                self.picam2.close()
            
            except Exception as e:
                logger("Sensor", "Error during capture.", e)
                self.picam2.close()

    def check_brightness(self):
        pass

if __name__ == '__main__':
    
    import time
    
    configurations = load_configurations("default.yaml")
    test_time = time.time()
    
    
    # print("Test quick capture.")
    
    sensor = Sensor(configurations=configurations, pc_time=test_time)
    # sensor.quick_capture()

    print("Test classic capture")
    sensor.capture_image()
    