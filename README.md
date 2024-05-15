# Projet - Néphélé

---

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Projet - Néphélé](#projet---néphélé)
  - [I - Identification du projet](#i---identification-du-projet)
  - [II - Préparation du matériel](#ii---préparation-du-matériel)
    - [II.1 - Client](#ii1---client)
      - [II.1.a - Configuration](#ii1a---configuration)
      - [II.1.b - Scripts](#ii1b---scripts)
      - [II.1.c - Dépendances](#ii1c---dépendances)
    - [II.2 - Module](#ii2---module)
      - [II.2.a - Configuration](#ii2a---configuration)
      - [II.2.b - Scripts](#ii2b---scripts)
      - [II.2.c -  Dépendances](#ii2c----dépendances)
  - [III - Utilisation](#iii---utilisation)
    - [III.1 - Paramètrage](#iii1---paramètrage)
    - [III.2 - Lancement](#iii2---lancement)
    - [III.3 - Erreurs](#iii3---erreurs)

<!-- /code_chunk_output -->


---




## I - Identification du projet

Le projet **neOCampus** de l'université Paul Sabatier a été étendu pour améliorer la station environnementale existante. Dans cette optique, un ajout crucial consiste à intégrer un appareil photo sur une carte Raspberry Pi-4, équipée d'une optique fish-eye, afin de compléter la collecte de données météorologiques.

Membres du groupe :

- **Bibyk Bogdan**  
- **Zerkani Yanis**

Nous avons intitulé ce projet **"Néphélé"**. :cloud:

## II - Préparation du matériel

Pour commencer, le matériel nécéssite une préparation au préalable du déploiement. Dans les 6 paragraphes suivant nous allons détailler les manipulations à réaliser côté client et côté module.

### II.1 - Client

L'**ordinateur d'acquisition** doit fonctionner sous un système d'exploitation **Linux**. Nous allons volontairement omettre la partie de préparation de l'OS, car elle dépend de votre configuration.

#### II.1.a - Configuration

- **Configurer** une **adresse IP statique** sur l'interface qui sera utilisée pour la communication avec le module. La démarche à suivre dépend de l'entité qui contrôle l'attribution des IP dans le système que vous utilisez pour l'ordinateur d'acquisition.
- **Créer** un répertoire de **dépot** où seront stockées les photos.

#### II.1.b - Scripts

- **Cloner** tous les **scripts** client sur l'ordinateur :
```
git init
git remote add -f origin "https://github.com/bBibyk/Nephele.git"
git config core.sparseCheckout true
echo "client/" >> .git/info/sparse-checkout
git pull origin main
```

#### II.1.c - Dépendances

- **Installer** les **bibliothèques** python nécessaires, depuis ```client/``` :
```
python -m pip install -r requirements_client.txt
```
- **Mettre en place** le script de **autostart**, depuis ```client/``` :
  ```
  chmod +x start_client.sh
  ```
- **S'assurer** que le chemin dans le fichier start_client.sh est **complet et absolu**.

### II.2 - Module

Les éléments suivants seront nécessaires pour faire fonctionner le module :

 - **Carte Raspberry Pi**. Ce projet sera réalisé avec une carte Raspberry Pi 4, mais une autre version pourra être utilisée
 - **Alimentation USB-C** compatible avec la carte Raspberry Pi
 - **Carte MicroSD** sur laquelle sera installé le système d'exploitation
 - **Adaptateur SD** pour installer le système d'exploitation (ordinateur avec lecteur SD necessaire pour la configuration)
 - **Module caméra haute qualité**
 - **Objectif fisheye**

#### II.2.a - Configuration

- **Installer** sur le module le système d'exploitation **Raspberry Pi OS Bookworm**.
  
- **Mettre à jour apt** :
  ```
  sudo apt update
  sudo apt upgrade
  ```
- **Installer** sur le module le **démon DHCPCD** :
  ```
  sudo apt-get install dhcpcd5
  ```
- **Configurer** une **adresse IP statique** sur l'interface qui sera utilisée pour la communication avec le module. Dans notre cas c'est l'interface ```eth0```.
   - Lancer la commande :
  ```
  sudo nano /etc/dhcpcd.conf
  ```
   - Ecrire :
  ```
  interface eth0
  static ip_address=10.0.0.10/24
  ```
   - Sauvegarder.
   - Redémarer le système.


Et enfin
\\TODO dependances apt?

#### II.2.b - Scripts

- **Cloner** tous les **scripts** client sur l'ordinateur :
```
git init
git remote add -f origin "https://github.com/bBibyk/Nephele.git"
git config core.sparseCheckout true
echo "module/" >> .git/info/sparse-checkout
git pull origin main
```

#### II.2.c -  Dépendances

- **Installer** les **bibliothèques** python nécessaires, depuis ```module/``` :
```
python -m pip install -r requirements_module.txt
```

\\TODO script bash pour le lancement automatique coté module

## III - Utilisation

Dans les

### III.1 - Paramètrage

### III.2 - Lancement

### III.3 - Erreurs

Le développement du module a été orienté sur une gestion maximale des exception et un systèmes de secours a été conçu pour permettre la reprise de l'algorithme distribué en cas de terminaison non attendue.
