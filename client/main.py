import yaml

configurations_file = open("config.yaml", "r")
configurations = yaml.load(configurations_file, Loader=yaml.SafeLoader)
print(configurations)
print(configurations["sensor"]["exposure"], type(configurations["sensor"]["exposure"]))