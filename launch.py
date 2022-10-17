from game import utils, client, server

def main():
    utils.clearTerminal()
    print("1 - Créer un serveur")
    print("2 - Se connecter à un serveur")

    rep = utils.demanderReponse(2)
    if rep == 1:
        server.mainServer()

    else:
        client.mainClient()


if __name__ == "__main__":
    main()