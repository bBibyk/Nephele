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
  - [Téléchargement des scrptis](#téléchargement-des-scrptis)
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

### Module

Les éléments suivants seront nécessaires pour faire fonctionner le module:

 - **Carte Raspberry Pi**. Ce projet sera réalisé avec une carte Raspberry Pi 4, mais une autre version pourra être utilisée
 - **Alimentation USB-C** compatible avec la carte Raspberry Pi
 - **Carte MicroSD** sur laquelle sera installé le système d'exploitation
 - **Module caméra haute qualité**
 - **Objectif fisheye**

#### Dépendances

python -m pip install -r requirements_module.txt

#### Configuration

Matériel requis :

 - Un ordinateur avec un lecteur de carte SD
 - Une carte microSD d'au moins 8 GB
 - Un adaptateur de carte microSD
 - Une connexion Internet stable

Étapes:
 1. Se rendre sur le site officiel https://www.raspberrypi.com/software/, et télécharger puis installer l'outil d'imagerie **Raspberry Pi Os**
 2. Insérer dans le lecteur de carte de l'ordinateur la carte microSD à l'aide de l'adaptateur
 3. Lancer l'outil d'imagerie et sélectionner la version de l'Os souhaitée, puis entammer le processus d'écriture de l'image sur la carte microSD. À noter que l'outil formatera automatiquement la carte microSD et écrira l'image dessus
 4. Une fois l'écriture terminée, retirer la carte microSD et l'insérer dans la Raspberry Pi. Connecter le Raspberry Pi à un écran, à un clavier, à une souris et à l'alimentation
 5. Démarrer le Raspberry Pi. Le processus d'installation de Raspberry Pi OS devrait commencer automatiquement. Suivre les instructions à l'écran pour configurer l'Os
 6. Une fois l'installation terminée, ouvrir un terminal et executer les commandes suivantes afin de mettre à jour le système:
  ```
  sudo apt update
  sudo apt upgrade
  ```

## Téléchargement des scrptis

### Client

### Module

\\TODO script bash pour le lancement automatique coté module

## Utilisation

### Paramètrage du module

### Lancement