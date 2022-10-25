import socket
import json
import time
from random import randrange

# Permet l'import du module question sans erreur
import sys
sys.path.insert(0, ".")

from Question import Question
import os
from time import sleep


def clear():
    """
    Efface la console
    :return: None
    """
    os.system('cls')


def initSocket(port, ip=''):
    """
    Initialise le socket avec l'IP et le port donné
    :param port: Le port sur lequel le socket doit écouter
    :param ip: (OPT) IP du serveur
    :return: l'objet socket initialisé
    """

    socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_ecoute.bind((ip, port))
    print("Information for the applicant : \n   - IP : "
          + socket.gethostbyname(socket.gethostname()) + "\n   - Port : " + str(port))
    return socket_ecoute


def ouvrirFichierQuestions():
    """
    Ouvre le fichier des questions (json) et les stocke dans un dictionnaire avec id -> question
    :return: Le dict des questions ainsi qu'une liste contenants les id des questions que le serveur doit choisir au départ
    """
    path = "res/test.json"
    with open(path, "r") as file:
        jsonFile = json.load(file)
        questDict = {}
        for question in jsonFile["questions"]:
            questDict[question["id"]] = Question(question["intitule"], question["reponse"], question["next"])
        return questDict, jsonFile["startIDs"]


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


def boucleJeu(connection):
    """
    Lancement de la boucle principale du jeu.
    :param connection: L'objet de connexion tcp
    :param adress: L'adresse du destinataire retourné lors de accept() de la connexion
    :return: None
    """

    questionId = 0  # L'id de la question qui est jouée
    questionReponseDict = {}  # Dictionnaire contenant les réponses que formule le client

    try:
        questDict, aChoisir = ouvrirFichierQuestions()
    except Exception:
        print("Erreur lors de l'ouverture du fichier des questions !")
        return

    while True:
        clear()
        if -1 in aChoisir:
            # C'est fini, il n'y a plus rien a poser
            break
        else:
            # On demande à l'utilisateur de chosir une question a poser
            print("Choose a question to ask : ")
            for i in range(len(aChoisir)):
                print("   - " + str(i + 1) + " : " + str(questDict[aChoisir[i]]))

            # Enregistrement du choix de la question
            questionId = inputInt(1, len(aChoisir)) - 1
            questionId = aChoisir[questionId]
            print("\nYou have chosen : " + str(questDict[questionId]))
            sleep(3)
            clear()

            # On envoie la question au client et on affiche la question envoyée
            questionDisplay = questDict[questionId].createQuestionDisplay()
            connection.send(str(len(questionDisplay)).encode()) # Envoi de la taille de la question
            connection.send(questionDisplay.encode())  # Envoi de la question
            connection.send(str(questDict[questionId].nbReponses()).encode())  # Envoi du nombre de réponses

            # Affichage de la question mise en forme a l'utilisateur du serveur
            print(questionDisplay)
            print("\nWaiting for the applicant...")

            # On attend la réponse du client
            tailleReponse = len(str(questDict[questionId].nbReponses())) # Calcul de la taille max de la réponse que peut envoyer le client
            reponse = connection.recv(tailleReponse).decode()
            reponse = int(reponse)

            # On vérifie la réponse
            if reponse in range(1, len(
                    questDict[questionId].answers) + 1):  # +1 car range est exclusif sur la borne supérieure
                # La réponse est bonne, on récupère la réponse correspondante à l'ID envoyée
                reponseStr = questDict[questionId].answers[reponse - 1]

                questionReponseDict[questionId] = reponseStr
                print("The applicant has chosen the answer : " + reponseStr)
                # On récupère les prochains choix de questions
                aChoisir = questDict[questionId].nextQuestions
                sleep(3)
            else:
                # La réponse est mauvaise, en théorie on ne devrait jamais arriver ici (sauf si le client a été modifié)
                print("ERROR! The applicant response is incorrect !")
                print("This response will not be saved !")
                sleep(3)

    # Fin du jeu
    # On envoie le message de fin au client
    connection.send(str(len("FIN")).encode()) # Taille de la chaine de fin
    time.sleep(0.1) # On attent pour éviter que TCP envoie les 2 messages en même temps
    connection.send("FIN".encode())

    # On affiche les réponses du client
    clear()
    print("End of the game ! Applicant response : ")
    for questionId in questionReponseDict:
        print("   - " + str(questDict[questionId]) + " -> " + questionReponseDict[questionId])
    input("Press enter to exit...")


if __name__ == "__main__":
    clear()
    # Initialisation du socket

    tcp = None
    while tcp is None:
        port = randrange(49152, 65535)
        try:
            tcp = initSocket(port)
        except OSError: # Le port sélectionné est déja occupé
            tcp = None

    if tcp is not None:
        # Attente de la connexion du client
        print("\nWaiting for a connection...")
        tcp.listen()
        client, adress = tcp.accept()

        print("\nApplicant connected ! Address of the applicant : ", adress)
        sleep(3)
        clear()

        # Lancement du jeu
        boucleJeu(client)

        # Fermeture du socket
        tcp.close()
