import socket
from time import sleep


# [QUESTION, [Reponse1, Reponse2], [IndexProchaineQuestion]]
questReps = [
    ["----------", [], [1]], # Permet de demander la question de départ
    ["Question 1", ["Q1R1", "Q1R2"],[2,3]],
    ["Question 2", ["Q2R1", "Q2R2"],[5,3]],
    ["Question 3", ["Q3R1", "Q3R2"],[6,4]],
    ["Question 4", ["Q4R1", "Q4R2"],[12,13]],
    ["Question 5", ["Q5R1", "Q5R2"],[6,8]],
    ["Question 6", ["Q6R1", "Q6R2"],[8,16]],
    ["Question 7", ["Q6R1", "Q6R2"],[14,15]],
    ["Question 8", ["Q6R1", "Q6R2"],[11,12]],
    ["Question 9", ["Q6R1", "Q6R2"],[14,16]],
    ["Question 10", ["Q6R1", "Q6R2"],[-1]],
    ["Question 11", ["Q6R1", "Q6R2"],[13,9]],
    ["Question 12", ["Q6R1", "Q6R2"],[7,9]],
    ["Question 13", ["Q6R1", "Q6R2"],[16,10]],
    ["Question 14", ["Q6R1", "Q6R2"],[16,10]],
    ["Question 15", ["Q6R1", "Q6R2"],[16,10]],
    ["Question 16", ["Q6R1", "Q6R2"],[10]],
]

def clearTerminal():
    print("\033c")


def envoyerAfficherQuestion(socket_client, question):
    # Mise en forme de la question
    msg = ""
    msg = "*" * (len(question[0]) + 4) + "\n" + "* " + question[0] + " *\n" + "*" * (len(question[0]) + 4) + "\n"
    for i in range(len(question[1])):
        msg += str(i + 1) + " - " + question[1][i] + "\n"

    # Envoi du texte a afficher
    socket_client.send(msg.encode())

    # Affichage pour l'utilisateur du serveur
    print(msg)

def obtenirReponse(idRep, idQuestion):
    return questReps[idQuestion][1][idRep - 1]

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


# ---------------------------- DEBUT DU PROGRAMME ----------------------------

def mainServer():
    port = 52864

    socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_ecoute.bind(('', port))
    print("IP de connexion : " + socket.gethostbyname(socket.gethostname()))
    # Gestion de la connexion

    print("En attente de la connexion du joueur 2...")
    socket_ecoute.listen()
    client, adress = socket_ecoute.accept()
    print("Le joueur 2 est connecté ! Adresse du joueur 2 : ", adress)
    sleep(3)
    clearTerminal()

    # Envoi des questions
    finQuestion = False
    indexQuestion = 0
    while not finQuestion:

        # On demande la question a poser
        clearTerminal()
        print("Quelle question voulez vous poser ?")
        for i in range(len(questReps[indexQuestion][2])):
            print(str(i + 1) + " - " + questReps[questReps[indexQuestion][2][i]][0])
        
        indexQuestion = demanderReponse(len(questReps[indexQuestion][2]))
        clearTerminal()

        # On envoie et on affiche la question
        envoyerAfficherQuestion(client, questReps[indexQuestion])
        
        # On attend la réponse du joueur 2
        print("En attente de la réponse du joueur 2...")
        rep = client.recv(1024)
        rep = int(rep.decode())
        print("Réponse du joueur 2 : ", obtenirReponse(rep, indexQuestion))
        sleep(3)
        clearTerminal()
        
        indexQuestion = questReps[indexQuestion][2][rep - 1]
        if indexQuestion == -1:
            finQuestion = True
            print("fin question")
            client.send("fin question".encode())


    print(rep)
    print("Closing connection")
    client.close()
    socket_ecoute.close()