import socket
import os
from time import sleep
import re

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
                print("Incorrect choice !")
        except ValueError:
            print("Incorrect choice !")
    return rep

def initConnexion():
    """Initialise la connexion avec le serveur"""
    ipRgx = re.compile(r"^((1?[0-9]{1,2}|2[0-4][0-9]|25[0-5]).){3}(1?[0-9]{1,2}|2[0-4][0-9]|25[0-5])$|^localhost$")
    ip = "tampon"
    while not ipRgx.match(ip):
        ip = input("Please input the server IP : ")
        if ip == "":
            ip = "localhost"
            print("Blank IP, connecting to local . . .")
        elif not ipRgx.match(ip):
            print("Incorrect IP ! Must be in the form : X.X.X.X or localhost")

    port = inputInt(0, 65535, "Please input the server port")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    return sock

def boucleJeu(connexion):
    """Boucle principale du jeu"""
    while True:
        # On attend une question du serveur. Ce message peut aussi être la fin de la partie

        print("Waiting question from the server ...")
        tailleQuestion = int(connexion.recv(1024).decode())
        question = connexion.recv(tailleQuestion).decode()
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
            print("Thanks for your participation !")
            sleep(3)
            break


if __name__ == '__main__':
    clear()
    server = None
    while server is None:
        try:
            server = initConnexion()
            print("Connection done !")
        except TimeoutError:
            print("Connection timed out ! Please try again . . .")
            server = None
        except ConnectionRefusedError:
            print("Connection refused ! Please try again . . .")
            server = None
        except OSError:
            print("Connection error ! Please try again . . .")
            server = None

    if server is not None:
        clear()
        try:
            boucleJeu(server)
        except Exception as e:
            print("An error has occurred during the game ! " + str(e))
        finally:
            server.close()
            print("Connection closed !")
            sleep(3)
        clear()
        print("Disconnection done !")
        input("Press enter to exit...")
