import time
import yaml

def get_script_directory() -> str:
    return "/".join(__file__.split("/")[0:-1])

def logger(talker : str, message : str, exception : Exception = None):
    current_time = time.strftime("%d/%m/%Y-%H:%M:%S", time.localtime())
    if exception is None:
        print(f"\t[{current_time}] {talker} : {message}")
    else:
        print(f"\t[{current_time}] {talker} : {message}", exception)

def load_configurations(filename : str) -> str:
    configurations = None
    try:
        cwd = get_script_directory()
        filepath = cwd + "/" + filename
        configurations = yaml.load(open(filepath, "r"), Loader=yaml.SafeLoader)
        logger("Utils", "Configurations loaded.")
        return configurations
    except Exception as e:
        logger("Utils", "Unable to load configurations.", e)
        return configurations