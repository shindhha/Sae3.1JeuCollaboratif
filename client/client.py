import socket
import os
from time import sleep

def clear():
    """
    Efface la console
    :return: None
    """
    os.system('cls')

def inputInt(min, max, msg="Veuillez entrer une valeur"):
    """
    Demande à l'utilisateur de rentrer un entier entre min et max
    :param msg: Le message a afficher
    :param min: La valeur minimum
    :param max: La valeur maximum
    :return: L'entier entré par l'utilisateur
    """
    msg = msg + " (" + str(min) + " - " + str(max) + ") : "

    reponseOk = False
    while not reponseOk:
        rep = input(msg)
        try:
            rep = int(rep)
            if rep >= min and rep <= max:
                reponseOk = True
            else:
                print("Réponse incorrecte !")
        except ValueError:
            print("Réponse incorrecte !")
    return rep

def initConnexion():
    """Initialise la connexion avec le serveur"""
    ip = input("Veuillez entrer l'IP du serveur : ")
    port = inputInt(0, 65535, "Veuillez entrer le port du serveur")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    return sock

def boucleJeu(connexion):
    """Boucle principale du jeu"""
    while True:
        # On attend une question du serveur. Ce message peut aussi être la fin de la partie
        # TODO : demander la taille de la question au serveur avant de la recevoir

        print("En attente d'une question du serveur...")
        question = connexion.recv(1024).decode()
        clear()
        if question != "FIN":
            intervalleRep = connexion.recv(16).decode() # Réception de l'ID MAX de la liste des réponses
            print(question)
            rep = inputInt(1, int(intervalleRep), "Veuillez entrer votre réponse")

            # Envoi de la réponse au serveur
            connexion.send(str(rep).encode())
            clear()
            print("Réponse envoyée !")
            sleep(3)
        else:
            break


if __name__ == '__main__':
    clear()
    try:
        server = initConnexion()
        print("Connexion établie !")
    except Exception as e:
        print("Erreur lors de la connexion avec le serveur !")
        server = None

    if server is not None:
        clear()
        boucleJeu(server)
        server.close()
        clear()
        print("Fin de la partie ! Merci pour votre participation !")
        input("Appuyez sur entrée pour quitter...")
