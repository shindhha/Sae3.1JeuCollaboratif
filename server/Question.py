class Question:
    def __init__(self, question, answers):
        self.__question = question
        self.__answers = answers

    def nbReponses(self):
        """
        :return: Le nombre de réponses possibles
        """
        return len(self.__answers)

    def createQuestionDisplay(self):
        """
        Crée la chaine de caractère jolie à afficher à l'utilisateur
        :return: La chaine de caractère
        """
        # la question est entourée l'étoiles (*)
        chaine = "*" * (len(self.__question) + 4) + "\n" \
                 + "* " + self.__question + " *\n" \
                 + "*" * (len(self.__question) + 4) + "\n"

        # On ajoute les réponses
        for i in range(self.nbReponses()):
            chaine += str(i + 1) + "   - " + str(self.__answers[i]) + "\n"

        return chaine

    def getAnswers(self):
        return self.__answers

    def __str__(self):
        return self.__question


class Reponse:
    def __init__(self, reponse, nextQuestions):
        self.__reponse = reponse
        self.__nextQuestions = nextQuestions

    def __str__(self):
        return self.__reponse

    def getNextQuestions(self):
        return self.__nextQuestions
