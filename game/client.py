import socket
from os import system
from time import sleep

def demanderReponse(nbreRep):
    reponseOk = False
    while not reponseOk:
        rep = input("Réponse : ")
        try:
            rep = int(rep)
            if rep > 0 and rep <= nbreRep:
                reponseOk = True
            else:
                print("Réponse incorrecte !")
        except ValueError:
            print("Réponse incorrecte !")
    return rep

def clearTerminal():
    print("\033c")


# ---------------------------- DEBUT DU PROGRAMME ----------------------------

def mainClient():
    port = 52864
    ip = "127.0.0.1"

    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((ip, port))

    print("Connecté au serveur " + ip + ":" + str(port))
    sleep(3)
    clearTerminal()

    finBoucle = False
    while not finBoucle:
        print("En attente de la question...")
        msg = socket_client.recv(1024)
        msg = msg.decode()
        if (msg == "fin question"):
            print("Fin des questions, merci pour votre participation")
            finBoucle = True
        else:
            clearTerminal()
            print(msg)

            # On demande la réponse au joueur et on l'envoie
            reponse = demanderReponse(2)
            socket_client.send(str(reponse).encode())
            sleep(3)
            clearTerminal()

    print("Closing connection")    
    socket_client.close()
