# Chat en Réseau avec Python et Tkinter

Ce projet est une application de chat simple utilisant les sockets en Python avec une interface graphique réalisée avec Tkinter. Il comprend un serveur et un client qui permettent aux utilisateurs de se connecter et de s'envoyer des messages en temps réel.

## Fonctionnalités

- Connexion multiple de clients au serveur.
- Interface graphique pour envoyer et recevoir des messages.
- Affichage des messages avec horodatage.
- Gestion des connexions et déconnexions des clients avec notification à tous les participants.

## Prérequis

Pour exécuter ce projet, vous aurez besoin de Python installé sur votre machine. Ce projet a été testé avec Python 3.8, mais il devrait être compatible avec d'autres versions de Python 3.

## Installation

Clonez le dépôt sur votre machine locale en utilisant le lien fourni par GitHub :

```bash
git clone https://github.com/Thomas-Adragna/pythonSocket.git
```
## Usage

Ouvrir un terminal, powershell, démarrer le serveur 

```bash
python app3server.py
```

Ensuite dans un autre terminal, ouvrir un client, pour chaque client supplémentaire, ouvrir un nouveau terminal

```bash
python app3client.py
```

## Structure de fichiers

app3client.py : Script pour l'interface client du chat.
app3server.py : Script pour le serveur gérant les connexions et la transmission des messages.
README.md : Ce fichier.




