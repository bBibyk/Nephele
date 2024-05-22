# Projet - Néphélé

---

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Projet - Néphélé](#projet---néphélé)
  - [I - Identification du projet](#i---identification-du-projet)
  - [II - Préparation du matériel](#ii---préparation-du-matériel)
    - [II.1 - Client](#ii1---client)
      - [II.1.a - Scripts](#ii1a---scripts)
      - [II.1.b - Configuration](#ii1b---configuration)
      - [II.1.c - Dépendances](#ii1c---dépendances)
    - [II.2 - Module](#ii2---module)
      - [II.2.a - Scripts](#ii2a---scripts)
      - [II.2.b - Configuration](#ii2b---configuration)
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

Nous avons intitulé ce projet **Néphélé**. :cloud:

## II - Préparation du matériel

Pour commencer, le matériel nécessite une préparation au préalable du déploiement. Dans les 6 paragraphes suivant nous allons détailler les manipulations à réaliser côté client et côté module.

### II.1 - Client

L'**ordinateur d'acquisition** doit fonctionner sous un système d'exploitation **Linux**. Nous allons volontairement omettre la partie de préparation de l'OS, car elle dépend de votre configuration.

#### II.1.a - Scripts

- **Cloner** tous les **scripts** client sur l'ordinateur :
  ```
  git init
  git remote add -f origin "https://github.com/bBibyk/Nephele.git"
  git config core.sparseCheckout true
  echo "client/" >> .git/info/sparse-checkout
  git pull origin main
  ```

#### II.1.b - Configuration

- **Configurer** une **adresse IP statique** sur l'interface qui sera utilisée pour la communication avec le module. La démarche à suivre dépend de l'entité qui contrôle l'attribution des IP dans le système que vous utilisez pour l'ordinateur d'acquisition. Mais dans tous les cas veillez à choisir une adresse dans le même sous-réseau que le module.

- **Créer** un répertoire de **dépot** où seront stockées les photos.

- Si besoin, **mettre en autostart** le script **main.py** du client.
  
#### II.1.c - Dépendances

- **Installer** les **bibliothèques** python nécessaires, depuis ```client/``` :
  ```
  python -m pip install -r requirements_client.txt
  ```

### II.2 - Module

Les éléments suivants seront nécessaires pour faire fonctionner le module :

 - **Carte Raspberry Pi**. Ce projet sera réalisé avec une carte Raspberry Pi 4, mais une autre version pourra être utilisée
 - **Alimentation USB-C** compatible avec la carte Raspberry Pi
 - **Carte MicroSD** sur laquelle sera installé le système d'exploitation
 - **Adaptateur SD** pour installer le système d'exploitation (ordinateur avec lecteur SD necessaire pour la configuration)
 - **Module caméra haute qualité**
 - **Objectif fisheye**


#### II.2.a - Scripts

- **Cloner** tous les **scripts** module sur l'ordinateur :
  ```
  git init
  git remote add -f origin "https://github.com/bBibyk/Nephele.git"
  git config core.sparseCheckout true
  echo "module/" >> .git/info/sparse-checkout
  git pull origin main
  ```

#### II.2.b - Configuration

- **Installer** sur le module le système d'exploitation **Raspberry Pi OS Bookworm**.
  
- **Mettre à jour apt** :
  ```
  sudo apt update
  sudo apt upgrade
  ```
- **Vérifier** que l'**adresse IP** dans le fichier ```start_module.sh``` correspond bien à celle du fichier ```default.yaml```
- **Mettre** le script de ```start_module.sh``` en **autostart** :
    - Depuis ```module/``` lancer :
    ```
    chmod +x start_module.sh
    ```
    - Lancer la commande :
    ```
    sudo nano /etc/rc.local
    ```
    - Ecrire avant la ligne ```# Print the IP address```:
    ```
    [chemin_absolu]/start_module.sh
    ```

#### II.2.c -  Dépendances

- **Installer** les **bibliothèques** python nécessaires, depuis ```module/``` :
  ```
  python -m pip install -r requirements_module.txt
  ```

- **S'assurer** que le chemin dans le fichier start_client.sh est **absolu et correct**.

\\TODO dependances apt?

## III - Utilisation

Ci-dessous vous trouverez une explication générale du fonctionnement du module, au cas où il y aura besoin d'intervenir pour le modifier.

Le système repose sur une architecture client-serveur où la classe Client agit comme le centre de traitement qui se connecte au serveur pour écouter des demandes et recevoir des réponses. La classe Server quant à elle écoute les connexions entrantes et agit comme un demandeur de services. Le nommage peut paraître malvenu, mais il repose simplement sur les rôles, c'est-à-dire qui entame la connexion (Client) et qui propose la connexion (Server).

  Initialisation et Configuration :
      Le module Server initialise un objet de connexion avec les configurations par défaut et prépare le socket pour écouter les connexions entrantes.
      Le module Client initialise également un objet de connexion et met à jour les configurations à partir d'un fichier YAML.

  Connexion :
      Le module Server écoute les connexions entrantes et accepte la connexion d'un client lorsque celle-ci est établie.
      Le module Client tente de se connecter au serveur en utilisant les configurations spécifiées.

  Échange de Données :
      Le module Server envoie des demandes au client sous forme de tags prédéfinis (comme <PARA>, <TIME>, <PHOT>) via le socket.
      Le module Client reçoit ces demandes, les traite et envoie les réponses appropriées en fonction des tags reçus.

  Traitement des Demandes :
      Le module Client traite les demandes reçues du client en fonction des tags. Par exemple, il peut envoyer les configurations actuelles, l'heure actuelle ou des photos stockées.
      Le module Server attend les réponses du serveur après avoir envoyé une demande et les traite en conséquence.

  Gestion de la Connexion :
      Les deux modules sont capables de détecter si la connexion est close et de gérer proprement la fermeture des sockets lorsqu'ils ont terminé leur tâche.

Cette architecture permet une communication efficace entre un client et un serveur, chacun exécutant des tâches spécifiques selon son rôle dans le système, sachant que la logique de fonctionnement est centralisée côté Raspberry Pi donc c'est lui qui "mène le jeu".

//TODO révision par Yanis!

A propos du Sensor, c'est un "wrapper" qui offre une abstraction pour la gestion de la caméra sur Raspberry Pi. Voici comment il fonctionne :

  Initialisation:
      Lors de l'initialisation de la classe Sensor, l'utilisateur fournit des configurations et l'heure actuelle du PC. Ces informations sont utilisées pour configurer le capteur et synchroniser l'horloge interne du module.
      La classe crée une instance de Picamera2 pour gérer la caméra.

  Méthodes publiques:
      update_configurations(configurations): Cette méthode permet de mettre à jour les configurations du capteur. Si aucune configuration n'est fournie, un message de journalisation est enregistré.
      sync_time(pc_time): Elle synchronise l'horloge interne du module avec l'heure fournie en paramètre ou avec l'heure actuelle du PC si aucun paramètre n'est fourni.
      start_camera(): Cette méthode démarre la caméra s'il n'est pas déjà en cours d'utilisation. Elle configure également les paramètres de capture de l'image.
      capture_image(): Capture une image à partir de la caméra. Elle utilise les configurations actuelles pour déterminer le chemin de sauvegarde de l'image. Si la luminosité de l'image capturée ne satisfait pas un seuil prédéfini, l'image est supprimée.

  Méthodes privées:
      __check_brightness(metadata): Vérifie si la luminosité de l'image capturée dépasse un seuil défini dans les configurations.
      __update_still_configurations(): Cette méthode met à jour les configurations de capture d'image fixes en fonction des configurations actuelles.
      __get_path(): Elle génère le chemin de sauvegarde de l'image en fonction de l'heure et du format de nommage spécifiés dans les configurations.

  Utilisation:
      Lorsque le module est exécuté directement, il charge les configurations par défaut à partir d'un fichier YAML, crée une instance de Sensor, démarre la caméra et capture trois images à intervalles de 3 secondes. Enfin, il ferme la caméra.

Il offre une abstraction pratique pour la capture d'images avec la caméra Raspberry Pi en encapsulant les détails de la configuration et de la gestion de la caméra ainsi il facilite l'emploi de ces fonctionnalités dans le main, sans pour autant surcharger la présentation.

On peut passer maintenant à l'exploitation.

### III.1 - Paramètrage

Le paramètrage du module s'effectue dans le fichier config.yaml côté Client. Le module tentera de récupérer la nouvelle configuration régulièrement. Donc on peut changer les paramètres du module pendant son fonctionnement. Toutes les règles relatives au formatage du fichier config.yaml sont décrites dans l'en-tête. Chaque paramètre est expliqué dans les commentaires.

### III.2 - Lancement

Pour lancer le programme il suffit de lancer avec python le main.py de chaque côté, l'ordre n'est pas important. L'ordre n'importe peu, le script Client tente de se conneter régulièrement, et le script Server tente la connection régulièrement et continue sa routine si le Client ne se connecte pas.

### III.3 - Erreurs

Le développement du module a été orienté sur une gestion maximale des exception et un système de secour a été conçu pour permettre la reprise de l'algorithme distribué en cas de terminaison inattendue. 