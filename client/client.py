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
    erreur = 0
    while not reponseOk:
        rep = input(msg)
        try:
            if rep.isdigit() and not rep.isspace() and len(rep) != 0:
                rep = int(rep)
                if rep >= min and rep <= max:
                    reponseOk = True
                else:
                    erreur += 1
                    print("Incorrect choice !")
            else:
                erreur += 1
                print("Incorrect choice !")
        except ValueError:
            erreur += 1
            print("Incorrect choice !")

        if erreur >= 5:
            rep = erreur
            reponseOk = True

    return rep

def initConnexion():
    """
    Initialise la connexion avec le serveur
    :return : soit la socket de connexion
              soit 1 pour indiquer trop d'erreur de saisie
    """
    ipRgx = re.compile(r"^((1?[0-9]{1,2}|2[0-4][0-9]|25[0-5]).){3}(1?[0-9]{1,2}|2[0-4][0-9]|25[0-5])$|^localhost$")
    ip = "tampon"
    compErreur = 0
    while not ipRgx.match(ip):
        ip = input("Please input the recruiter IP : ")
        if ip == "":
            ip = "localhost"
            print("Blank IP, connecting to local . . .")
        elif not ipRgx.match(ip):
            print("Incorrect IP ! Must be in the form : X.X.X.X or localhost")
            compErreur += 1

        # si nombres erreurs d'entrée égale a 5 alors on coupe sinon programme infinie en cas d'echec consécutif
        if compErreur >= 5:
            break

    if compErreur < 5:
        port = inputInt(0, 65535, "Please input the recruiter port")
        if port == 5:
            return 1
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        return sock
    else:
        # correspond a une erreur si trop d 'erreur d'entrée dans l'adresse IP
        return 1



def boucleJeu(connexion):
    """Boucle principale du jeu"""
    # affichage des regles
    print("-------------- Rules of the game --------------\n")
    print("You are applicant, in this game, \n"
          "you have to answer 3 questions in the most sincere way by choosing among the answers given. \n"
          "These questions are given by the recruiter. \n"
          "When the game ends, you will be able to  close the window\n")

    # permet de laisser le temps de lire
    sleep(5)

    while True:
        # On attend une question du serveur. Ce message peut aussi être la fin de la partie
        print("Waiting question from the recruiter ...")
        tailleQuestion = int(connexion.recv(1024).decode())
        question = connexion.recv(tailleQuestion).decode()
        clear()

        if question != "FIN":
            clear()
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
    compErreur = 0
    while server is None:
        try:
            server = initConnexion()
            # Si trop d'erreur de saisie alors on mets le nombre d'erreur au max
            if server == 1:
                compErreur = 5
            else:
                print("Connection done !")
        except TimeoutError:
            print("Connection timed out ! Please try again . . .")
            server = None
        except ConnectionRefusedError:
            print("Connection refused ! Please try again . . .")
            compErreur += 1
            server = None
        except OSError:
            print("Connection error ! Please try again . . .")
            server = None

        # Si nombre d'erreurs égale a 5 alors on demande de relancer et arrete le prog
        if compErreur >= 5:
            print("Too many wrong attempts, restart the game")
            server = None
            break

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
        print("Disconnection done !")
        input("Press enter to exit...")
