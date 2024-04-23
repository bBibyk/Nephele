import yaml
from picamera2 import Picamera2
import time
import os

class Sensor:
    def __init__(self):
        self.load_default_configurations()
        self.picam2=Picamera2()
    
    def load_default_configurations(self):
        
        self.configurations = None
        
        if os.path.exists("config.yaml"):
            config = "config.yaml"
            self.__logger("config.yaml file reached.")
        else:
            config = "default.yaml"
            self.__logger("Couldn't reach config.yaml. Using default.yaml")
        
        try:
            self.configurations = yaml.load(open(config, "r"), Loader=yaml.SafeLoader)
            self.__logger("Default configurations loaded.")
        except Exception as e:
            self.__logger("Unable to load default configurations.", e)
            
    def start_preview(self):
        self.picam2.start_preview()
    
    def stop_preview(self):
        self.picam2.stop_preview()
    
    def start_capture(self):
        while True:
            try:
                
                timestamp = time.strftime("%Y%m%d%H%M%S")
                image_name_format = self.configurations['module']['image_name_format']
                image_name = image_name_format.format(timestamp=timestamp)
                image_path = os.path.join(self.configurations['module']['shots'], image_name)
                
                self.picam2.capture_file(image_path)
                self.__logger(f"Image captured: {image_name}")
                
                time.sleep(self.configurations['module']['delay'])
            except Exception as e:
                self.__logger("Error during capture.", e)


    def check_brightness(self):
        pass

    def stop_capture(self):
        pass

    def __logger(self, message : str, exception : Exception = None):
        current_time = time.strftime("%d/%m/%Y-%H:%M:%S", time.localtime())
        if exception is None:
            print(f"\t[{current_time}] {message}")
        else:
            print(f"\t[{current_time}] {message}", exception)


if __name__ == '__main__':
    from picamera2 import Preview
    sensor = Sensor()
    
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    time.sleep(2)
    picam2.capture_file("test.jpg")

    