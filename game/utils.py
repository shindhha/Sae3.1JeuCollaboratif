import os

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
    os.system("cls")