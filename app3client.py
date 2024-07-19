import socket  
from tkinter import *  
from tkinter import simpledialog, scrolledtext 
import threading 

def client():
    s = socket.socket()  # Crée un nouvel objet socket
    host = socket.gethostname()  # Obtient le nom d'hôte local
    port = 12345  # Définit le numéro de port sur 12345
    s.connect((host, port))  # Connecte le socket à l'adresse et au port spécifiés
    
    # Demande le nom d'utilisateur au client à travers une boîte de dialogue
    name = simpledialog.askstring("Nom", "Entrez votre nom d'utilisateur:")
    if name:
        s.send(name.encode())  # Si un nom est fourni, il est envoyé au serveur encodé en bytes
    else:
        name = 'Anonyme'  # Nom par défaut si l'utilisateur ne saisit rien
        s.send(name.encode())  # Envoie le nom par défaut encodé en bytes

    def send_message(event=None):
        message = entry_message.get()  # Récupère le message saisi dans le champ de saisie
        if message:
            s.send(message.encode())  # Envoie le message au serveur encodé en bytes
            txt.insert(END, f"Vous : {message}\n")  # Affiche le message dans la zone de texte du client
            entry_message.delete(0, END)  # Efface le champ de saisie après l'envoi du message

    def receive_messages():
        while True:
            try:
                response = s.recv(1024).decode()  # Réceptionne les messages du serveur, avec un buffer de 1024 bytes
                if ": " in response:  # Vérifie si le message reçu contient un séparateur "nom: message"
                    response_name, response_message = response.split(": ", 1)
                    if response_name != name:  # Vérifie si le message provient d'un autre client
                        txt.insert(END, f"{response_name} : {response_message}\n")  # Affiche le message avec le nom de l'expéditeur
                else:
                    txt.insert(END, response + "\n")  # Affiche le message tel quel s'il n'est pas au format attendu
            except OSError:
                break  # Sort de la boucle si une erreur de socket survient

    threading.Thread(target=receive_messages, daemon=True).start()  # Démarre un thread daemon pour recevoir les messages

    entry_message = Entry(window, width=40)  # Crée un champ de saisie pour les messages
    entry_message.grid(column=0, row=1, padx=10, pady=10, sticky=W+E)  # Positionne le champ de saisie dans la fenêtre
    entry_message.bind("<Return>", send_message)  # Lie la touche Entrée à la fonction send_message

    btn_send = Button(window, text="Envoyer", command=send_message)  # Crée un bouton pour envoyer les messages
    btn_send.grid(column=1, row=1, padx=10, pady=10, sticky=W+E)  # Positionne le bouton dans la fenêtre

window = Tk()  # Crée la fenêtre principale de l'application
window.title("Client")  # Définit le titre de la fenêtre
window.geometry("500x300")  # Définit les dimensions de la fenêtre

txt = scrolledtext.ScrolledText(window, width=60, height=20)  # Crée une zone de texte défilante pour afficher les messages
txt.grid(column=0, row=0, columnspan=2, padx=10, pady=10)  # Positionne la zone de texte dans la fenêtre

client()  # Appelle la fonction client pour démarrer le client de chat

window.mainloop()  # Démarre la boucle principale de l'interface graphique pour attendre les événements utilisateur
