import json
from pprint import pprint


def LoadQuiz(sentQuizDict):
  name = sentQuizDict["title"]
  qId = sentQuizDict["id"]

  counter = 1
  allQuestions = ""
  for question in sentQuizDict["questions"]:
    questionObj = getQuestion(question, counter, len(sentQuizDict["questions"]))
    allQuestions += questionObj + "\n"

    counter += 1

  with open("templates/quizStuff/quiz.html", "r") as quizTemp:
    quizContent = quizTemp.read()

  quizContent = quizContent.replace(u"||_REPLACE ME WITH QUIZ_||", allQuestions)
  #quizContent = quizContent.decode('utf-8').replace(u"||_REPLACE ME WITH QUIZ_||", allQuestions.decode('utf-8'))
  return quizContent

def getQuestion(qDict, qNum, totalNum):
  inputTemp = "templates/quizStuff/inputTemplate.html"
  with open(inputTemp, "r") as inputHandle:
    questionTemplate = inputHandle.read()

  questionIns = questionTemplate.replace("||_count_||", str(qNum) + " of " + str(totalNum))
  questionIns = questionIns.replace("||_prog_||", str(qNum)+" * 100% / " + str(totalNum))
  questionIns = questionIns.replace("||_prompt_||", qDict["prompt"])

  return questionIns