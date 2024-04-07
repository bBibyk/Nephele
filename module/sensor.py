import yaml

with open('../client/config.yaml', 'r') as fichier:
    dictionnaire = yaml.load(fichier, Loader=yaml.SafeLoader)

parametres_sensor = dictionnaire["sensor"]

print(parametres_sensor)