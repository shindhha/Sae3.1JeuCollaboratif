import socket
import os
from time import sleep

def clear():
    """
    Efface la console
    :return: None
    """
    os.system('cls')

def inputInt(min, max, msg="Please input an integer"):
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
                print("Incorrect answer !")
        except ValueError:
            print("Incorrect answer !")
    return rep

def initConnexion():
    """Initialise la connexion avec le serveur"""
    ip = input("Please input the server IP : ")
    port = inputInt(0, 65535, "Please input the server port")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    return sock

def boucleJeu(connexion):
    """Boucle principale du jeu"""
    while True:
        # On attend une question du serveur. Ce message peut aussi être la fin de la partie
        # TODO : demander la taille de la question au serveur avant de la recevoir

        print("Waiting question from the server ...")
        question = connexion.recv(1024).decode()
        clear()
        if question != "FIN":
            intervalleRep = connexion.recv(16).decode() # Réception de l'ID MAX de la liste des réponses
            print(question)
            rep = inputInt(1, int(intervalleRep), "Please input your response here")

            # Envoi de la réponse au serveur
            connexion.send(str(rep).encode())
            clear()
            print("Response sent !")
            sleep(3)
        else:
            break


if __name__ == '__main__':
    clear()
    try:
        server = initConnexion()
        print("Connection done !")
    except Exception as e:
        print("Error during the initialisation: " + str(e))
        server = None

    if server is not None:
        clear()
        boucleJeu(server)
        server.close()
        clear()
        print("Disconnection done !")
        input("Press enter to exit...")
