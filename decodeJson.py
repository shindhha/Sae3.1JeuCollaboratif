import json


class Question:
    def __init__(self, id, question, answers, nextQuestions):
        self.id = id
        self.question = question
        self.answer = answers
        self.nextQuestions = nextQuestions

    def __str__(self):
        return "(" + str(self.id) + ") Question: " + self.question + " | Answers: " + str(
            self.answer) + " | Next questions: " + str(self.nextQuestions)


if __name__ == "__main__":
    listQuestion = []

    with open('game/questions.json', 'r') as f:
        data = json.load(f)

    for question in data:
        listQuestion.append(Question(question['id'], question['intitule'], question['reponse'], question['next']))

    for q in listQuestion:
        print(q)
