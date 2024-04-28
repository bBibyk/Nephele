# Projet - Néphélé

---
- [Projet - Néphélé](#projet---néphélé)
  - [Identification du projet](#identification-du-projet)
  - [Préparation du matériel](#préparation-du-matériel)
    - [Client](#client)
      - [Dépendances](#dépendances)
      - [Configuration](#configuration)
    - [Module](#module)
      - [Dépendances](#dépendances-1)
      - [Configuration](#configuration-1)
  - [Téléchargement des scripts](#téléchargement-des-scripts)
    - [Client](#client-1)
    - [Module](#module-1)
  - [Utilisation](#utilisation)
    - [Paramètrage du module](#paramètrage-du-module)
    - [Lancement](#lancement)
---

## Identification du projet

<p style="text-align: justify;">Le projet neOCampus de l'université Paul Sabatier a été étendu pour améliorer la station environnementale existante. Dans cette optique, un ajout crucial consiste à intégrer un appareil photo sur une carte Raspberry Pi-4, équipé d'une optique fish-eye, afin de compléter la collecte de données météorologiques.</p>

Membres du groupe :
- Bibyk Bogdan
- Zerkani Yanis

Nous avons intitulé le projet "Néphélé" :cloud:

## Préparation du matériel

### Client

L'**ordinateur client** doit fonctionner sur un système d'exploitation Linux. Les bibliothèques contenues dans le fichier **client/requirements_client.txt** doivent être installées au préalable.

#### Dépendances

python -m pip install -r requirements_client.txt

#### Configuration

Il faut aussi configurer une adresse IP statique sur l'interface qui sera utilisée pour la communication avec le module. Dans notre cas c'est l'interface eth0.

Pour cela il faut modifier le fichier de configuration du démon DHCPCD du système en 3 étapes:
 - Lancer la commande ```sudo nano /etc/dhcpcd.conf```
 - Ecrire :
  interface eth0
  static ip_address=10.0.0.10/24
 - Lancer la commande ```sudo reboot```

### Module

Les éléments suivants seront nécessaires pour faire fonctionner le module:

 - **Carte Raspberry Pi**. Ce projet sera réalisé avec une carte Raspberry Pi 4, mais une autre version pourra être utilisée
 - **Alimentation USB-C** compatible avec la carte Raspberry Pi
 - **Carte MicroSD** sur laquelle sera installé le système d'exploitation
 - **Adaptateur SD** pour installer le système d'exploitation (ordinateur avec lecteur SD necessaire pour la configuration)
 - **Module caméra haute qualité**
 - **Objectif fisheye**

#### Dépendances

python -m pip install -r requirements_module.txt

#### Configuration

 1. Se rendre sur le site officiel https://www.raspberrypi.com/software/, et télécharger puis installer l'outil d'imagerie **Raspberry Pi Os**
 2. Inserer la carte SD et lancer l'outil d'imagerie. Inserer la carte microSD dans le Raspberry Pi une fois l'écriture terminée, le demarrer et suivre les instructions à l'écran pour configurer l'Os
 3. Une fois l'installation terminée, ouvrir un terminal et executer les commandes suivantes afin de mettre à jour le système:
  ```
  sudo apt update
  sudo apt upgrade
  ```

## Téléchargement des scripts

### Client

### Module

\\TODO script bash pour le lancement automatique coté module
\\TODO how to venv // pip install

## Utilisation

### Paramètrage du module

\\TODO dependances apt?

### Lancement