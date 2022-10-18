class Question:
    def __init__(self, question, answers, nextQuestions):
        self.question = question
        self.answers = answers
        self.nextQuestions = nextQuestions

    def nbReponses(self):
        """
        :return: Le nombre de réponses possibles
        """
        return len(self.answers)

    def createQuestionDisplay(self):
        """
        Crée la chaine de caractère jolie à afficher à l'utilisateur
        :return: La chaine de caractère
        """
        # la question est entourée l'étoiles (*)
        chaine = "*" * (len(self.question) + 4) + "\n" \
                    + "* " + self.question + " *\n" \
                    + "*" * (len(self.question) + 4) + "\n"

        # On ajoute les réponses
        for i in range(self.nbReponses()):
            chaine += str(i + 1) + "   - " + self.answers[i] + "\n"

        return chaine

    def __str__(self):
        return self.question