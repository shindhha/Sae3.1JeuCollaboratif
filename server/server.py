import socket
import json
import time
from random import randrange

# Permet l'import du module question sans erreur
import sys

sys.path.insert(0, ".")

from Question import Question, Reponse
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
    path = "res/questions.json"
    with open(path, "r") as file:
        jsonFile = json.load(file)
        questDict = {}
        for question in jsonFile["questions"]:
            lteReponses = []
            for rep in question["reponses"]:
                lteReponses.append(Reponse(rep["rep"], rep["nextQuestions"]))

            questDict[question["id"]] = Question(question["intitule"], lteReponses)
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
                print("Incorrect choice !")
        except ValueError:
            print("Incorrect choice !")
    return rep


def envoieQuestion(idQuestion, connection):
    """
    Envoie de la question au client avec le format voulu
    :param idQuestion: id de la question a envoyée
    :param connection: L'objet de connexion tcp
    """
    questionDisplay = idQuestion.createQuestionDisplayClient()
    connection.send(str(len(questionDisplay)).encode())  # Envoi de la taille de la question
    connection.send(questionDisplay.encode())  # Envoi de la question
    connection.send(str(idQuestion.nbReponses()).encode())  # Envoi du nombre de réponses


def choixQuestion(questDict, aChoisir):
    """
    Choix de la prochaine question a envoyée au client
    :param questDict: dictionnaire des questions
    :param aChoisir: liste des questions a choisir par le serveur
    :return : renvoie l'id de la question choisie
    """
    # On demande à l'utilisateur de chosir une question a poser si ce n'est pas la premiere question
    if len(aChoisir) == 2:
        print("Choose a question to ask : ")
        for i in range(len(aChoisir)):
            print("   - " + str(i + 1) + " : " + str(questDict[aChoisir[i]]))
        questionId = inputInt(1, len(aChoisir)) - 1
        questionId = aChoisir[questionId]
        print("\nYou have chosen : " + str(questDict[questionId]))
        sleep(3)
        clear()
    else:
        questionId = 0
        questionId = aChoisir[questionId]
        print("The first question is always the same")
    return questionId


def receptionReponse(idQuestion, connection):
    """
    Réception de la réponse client
    :param idQuestion: Id de la question en cours
    :param connection: L'objet de connexion tcp
    :return : renvoie la réponse du client
    """
    # On attend la réponse du client
    tailleReponse = len(
        str(idQuestion.nbReponses()))  # Calcul de la taille max de la réponse que peut envoyer le client
    reponse = connection.recv(tailleReponse).decode()
    reponse = int(reponse)
    return reponse


def verificationReponse(reponse, idQuestion):
    """
    Vérification de la validité de la réponse
    :param reponse: réponse du client
    :param idQuestion: id de la question actuelle
    :return : renvoie l'objet réponse correspondant
    """
    # On vérifie la réponse
    if reponse in range(1, len(
            idQuestion.getAnswers()) + 1):  # +1 car range est exclusif sur la borne supérieure
        # La réponse est bonne, on récupère la réponse correspondante à l'ID envoyée
        reponseObj = idQuestion.getAnswers()[reponse - 1]
        print("The applicant has chosen the answer : " + str(reponseObj))
        return reponseObj
    else:
        # La réponse est mauvaise, en théorie on ne devrait jamais arriver ici (sauf si le client a été modifié)
        print("ERROR! The applicant response is incorrect !")
        print("This response will not be saved !")
        return None


def finDuJeu(connection, questionReponseDict, questDict):
    """
    Fin du jeu avec affichage du résumé des réponses
    :param connection: L'objet de connexion tcp
    :param questionReponseDict: dictionnaire des réponses par questions
    :param questDict: dictionnaire des questions
    """

    # On envoie le message de fin au client
    connection.send(str(len("FIN")).encode())  # Taille de la chaine de fin
    time.sleep(0.1)  # On attent pour éviter que TCP envoie les 2 messages en même temps
    connection.send("FIN".encode())

    # On affiche les réponses du client
    clear()
    print("End of the game ! Applicant response : ")
    for questionId in questionReponseDict:
        print("   - " + str(questDict[questionId]) + "\n       -> " + questionReponseDict[questionId])
    input("Press enter to exit...")


def boucleJeu(connection):
    """
    Lancement de la boucle principale du jeu.
    :param connection: L'objet de connexion tcp
    :return: None
    """

    questionId = 0  # L'id de la question qui est jouée
    questionReponseDict = {}  # Dictionnaire contenant les réponses que formule le client

    print("-------------- Rules of the game --------------\n")
    print("You are the recruiter,\n"
          "the first question is imposed.\n"
          "For the next question, you have to choose between 2 questions that are given.\n"
          "these questions are linked to the applicant's answers.\n"
          "When the game ends, you will be able to see a summary of the questions and answers.\n")

    # permet de laisser le temps de lire
    sleep(5)
    try:
        questDict, aChoisir = ouvrirFichierQuestions()
    except Exception as e:
        print("Error while opening question file : " + str(e))
        sleep(3)
        return

    while True:
        clear()
        if -1 in aChoisir:
            # C'est fini, il n'y a plus rien a poser
            break
        else:
            # choix de la question
            questionId = choixQuestion(questDict, aChoisir)

            # envoie de la question au client
            envoieQuestion(questDict[questionId], connection)

            # Affichage de la question mise en forme a l'utilisateur du serveur
            questionDisplay = questDict[questionId].createQuestionDisplayServer()
            print(questionDisplay)
            print("\nWaiting for the applicant...")

            # Réception de la reponse
            reponse = receptionReponse(questDict[questionId], connection)

            # vérifiaction de la réponse
            repObj = verificationReponse(reponse, questDict[questionId])
            if repObj is None:
                aChoisir = -1
            else :
                # ajout de l'objet réponse dans le dictionnaire
                questionReponseDict[questionId] = str(repObj)
                # On récupère les prochains choix de questions
                aChoisir = repObj.getNextQuestions()
                sleep(3)

    # Fin du jeu
    finDuJeu(connection, questionReponseDict, questDict)


if __name__ == "__main__":
    clear()
    ouvrirFichierQuestions()
    # Initialisation du socket

    tcp = None
    while tcp is None:
        port = randrange(49152, 65535)
        try:
            tcp = initSocket(port)
        except OSError:  # Le port sélectionné est déja occupé
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
        try:
            boucleJeu(client)
        except Exception as e:
            print("An error has occurred during the game ! " + str(e))
            print("The applicant will be disconnected !")

        # Fermeture de la connexion
        client.close()
        # Fermeture du socket
        tcp.close()
