import socket
import json
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
    print("Information de connexion pour le joueur 2 : \n   - IP : "
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
            print("Choisissez une question a poser : ")
            for i in range(len(aChoisir)):
                print("   - " + str(i + 1) + " : " + str(questDict[aChoisir[i]]))

            # Enregistrement du choix de la question
            questionId = inputInt(1, len(aChoisir)) - 1
            questionId = aChoisir[questionId]
            print("\nVous avez choisi la question : " + str(questDict[questionId]))
            sleep(3)

            # On envoie la question au client et on affiche la question envoyée
            # TODO : Envoyer la taille de la caine de caractère représentant la question
            connection.send(questDict[questionId].createQuestionDisplay().encode())  # Envoi de la question
            connection.send(str(questDict[questionId].nbReponses()).encode())  # Envoi du nombre de réponses

            # Affichage de la question mise en forme a l'utilisateur du serveur
            print(questDict[questionId].createQuestionDisplay())
            print("\nEn attente de la réponse du client...")

            # On attend la réponse du client
            # TODO : Calculer la taille de la réponse pour attendre juste le nombre de caractères attendus
            reponse = connection.recv(16).decode()
            reponse = int(reponse)

            # On vérifie la réponse
            if reponse in range(1, len(
                    questDict[questionId].answers) + 1):  # +1 car range est exclusif sur la borne supérieure
                # La réponse est bonne, on récupère la réponse correspondante à l'ID envoyée
                reponseStr = questDict[questionId].answers[reponse - 1]

                questionReponseDict[questionId] = reponseStr
                print("Le client a choisi la réponse : " + reponseStr)
                # On récupère les prochains choix de questions
                aChoisir = questDict[questionId].nextQuestions
                sleep(3)
            else:
                # La réponse est mauvaise
                print("ERREUR! Le client a inséré une réponse qui n'est pas dans la liste des réponses possibles !")
                print("Cette queestion n'est pas enregistrée !")
                sleep(3)

    # Fin du jeu
    # On envoie le message de fin au client
    # TODO envoyer la taille de la chaine de caractère
    connection.send("FIN".encode())

    # On affiche les réponses du client
    clear()
    print("Fin du jeu ! Voici les réponses du client : ")
    for questionId in questionReponseDict:
        print("   - " + str(questDict[questionId]) + " -> " + questionReponseDict[questionId])
    input("Appuyez sur entrée pour quitter...")


if __name__ == "__main__":
    clear()
    # Initialisation du socket
    try:
        tcp = initSocket(52864)
    except OSError:
        print("Le port est déjà utilisé")
        print("Fin du programme")
        tcp = None

    if tcp is not None:
        # Attente de la connexion du client
        print("\nEn attente de la connexion du joueur 2...")
        tcp.listen()
        client, adress = tcp.accept()

        print("\nLe joueur 2 est connecté ! Adresse du joueur 2 : ", adress)
        sleep(3)
        clear()

        # Lancement du jeu
        boucleJeu(client)

        # Fermeture du socket
        tcp.close()
