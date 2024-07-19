import socket  # Importe le module socket pour la communication réseau
import threading  # Importe le module threading pour permettre l'exécution de tâches en parallèle
from tkinter import *  # Importe tout depuis tkinter pour créer l'interface graphique
from tkinter import scrolledtext  # Importe le composant scrolledtext pour un affichage de texte défilant
from datetime import datetime  # Importe le module datetime pour obtenir l'heure et la date actuelle

def serveur():
    s = socket.socket()  # Crée un nouvel objet socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Configure le socket pour réutiliser l'adresse
    host = socket.gethostname()  # Obtient le nom d'hôte local
    port = 12345  # Définit le numéro de port sur 12345
    s.bind((host, port))  # Lie le socket à l'adresse et au port spécifiés
    s.listen(5)  # Met le serveur en écoute, prêt à accepter jusqu'à 5 connexions
    txt.insert(END, "Le serveur écoute à l'adresse : " + host + " sur le port : " + str(port) + "\n")  # Affiche l'état du serveur dans la zone de texte

    clients = {}  # Crée un dictionnaire pour stocker les informations des clients connectés

    def handle_client(conn, addr):
        name = conn.recv(1024).decode()  # Reçoit et décode le nom du client
        welcome = f"Bienvenue {name}. Vous pouvez commencer à envoyer des messages."  # Crée un message de bienvenue
        conn.send(welcome.encode())  # Envoie le message de bienvenue encodé en bytes
        msg = f"{name} s'est connecté à partir de {addr}"  # Message informant de la connexion d'un client
        broadcast(msg, name="Serveur", skip_sender=conn)  # Diffuse ce message à tous les autres clients
        clients[conn] = name  # Enregistre le client et son nom dans le dictionnaire

        while True:
            data = conn.recv(1024)  # Reçoit les données du client
            if not data:
                msg = f"{name} a quitté la discussion."  # Message lorsque le client se déconnecte
                broadcast(msg, name="Serveur", skip_sender=conn)  # Diffuse le message de déconnexion
                conn.close()  # Ferme la connexion
                del clients[conn]  # Supprime le client du dictionnaire
                break
            broadcast(data, name=name, skip_sender=conn)  # Diffuse les messages du client aux autres

    def broadcast(msg, name="", skip_sender=None):
        time_stamp = datetime.now().strftime("%H:%M")  # Obtient l'heure actuelle
        log_message = f"{time_stamp} -> {name}: {msg.decode() if isinstance(msg, bytes) else msg}"  # Formate le message pour l'ajouter à la zone de texte
        txt.insert(END, log_message + "\n")  # Insère le message dans la zone de texte
        for conn in clients:
            if conn != skip_sender:
                if isinstance(msg, bytes):
                    conn.send(msg)  # Envoie le message tel quel aux autres clients
                else:
                    conn.send(bytes(f"{name}: {msg}", "utf8"))  # Envoie le message formaté aux autres clients

    while True:
        conn, addr = s.accept()  # Accepte les nouvelles connexions
        txt.insert(END, f"Nouvelle connexion de {addr}\n")  # Affiche les nouvelles connexions dans la zone de texte
        threading.Thread(target=handle_client, args=(conn, addr)).start()  # Démarre un nouveau thread pour gérer le client

def start_server():
    threading.Thread(target=serveur, daemon=True).start()  # Démarre un thread daemon pour le serveur

window = Tk()  # Crée la fenêtre principale de l'application
window.title("Serveur")  # Définit le titre de la fenêtre
window.geometry("500x300")  # Définit les dimensions de la fenêtre

txt = scrolledtext.ScrolledText(window, width=60, height=20)  # Crée une zone de texte défilante pour afficher les messages
txt.grid(column=0, row=0, padx=10, pady=10)  # Positionne la zone de texte dans la fenêtre

btn = Button(window, text="Démarrer le Serveur", command=start_server)  # Crée un bouton pour démarrer le serveur
btn.grid(column=0, row=1, pady=10, sticky=E+W)  # Positionne le bouton dans la fenêtre

def on_closing():
    window.destroy()  # Définit la fonction à appeler lorsque la fenêtre est fermée

window.protocol("WM_DELETE_WINDOW", on_closing)  # Lie la fonction on_closing à l'événement de fermeture de la fenêtre

window.mainloop()  # Démarre la boucle principale de l'interface graphique pour attendre les événements utilisateur
