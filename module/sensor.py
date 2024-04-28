from picamera2 import Picamera2
from utils import *
from os.path import join

class Sensor:
    def __init__(self, configurations, pc_time : time):
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
    
    def sync_time(self, pc_time):
        self.module_time : time = pc_time
        
    def start_preview(self):
        self.picam2.start_preview()
    
    def stop_preview(self):
        self.picam2.stop_preview()
    
    def quick_capture(self):
        self.picam2.start_and_capture_file("Test.jpg")
        
    def __name_image(self):
        
        timestamp : str = self.module_time.strftime("%Y%m%d%H%M%S")
        image_name_format : str = self.configurations['module']['image_name_format']
        image_name : str = image_name_format.format(timestamp=timestamp)  
        return image_name
         
    def capture_file(self):
            try:
                with self.picam2.start_preview():
                    
                    image_name = self.__name_image()
                    image_path = join(self.configurations['module']['shots'], image_name)
                    with self.picam2.capture_file(image_path):
                        logger("Sensor", f"Image captured: {image_name}")
                    
            except Exception as e:
                logger("Sensor", "Error during capture.", e)

    def check_brightness(self):
        pass

if __name__ == '__main__':
    from picamera2 import Preview
    print("Test quick capture.")
    sensor = Sensor()
    sensor.quick_capture()

    