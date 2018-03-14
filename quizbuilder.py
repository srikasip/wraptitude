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
  isType = ""
  if qDict['type']=="SurveyQuestions::MultipleChoice":
    inputTemp = "templates/quizStuff/multiselectTemplate.html"
    isType = "multiselect"
  elif qDict['type']=="SurveyQuestions::Range":
    inputTemp = "templates/quizStuff/sliderTemplate.html"
    isType = "slider"
  else:
    inputTemp = "templates/quizStuff/inputTemplate.html"
    isType = "text"
  
  with open(inputTemp, "r") as inputHandle:
    questionTemplate = inputHandle.read()

  questionIns = questionTemplate.replace("||_count_||", str(qNum) + " of " + str(totalNum))
  questionIns = questionIns.replace("||_prog_||", str(qNum)+" * 100% / " + str(totalNum))
  questionIns = questionIns.replace("||_prompt_||", qDict["prompt"])

  if isType == "slider":
    questionIns = questionIns.replace("||_rangeMin_||", qDict["min_label"])
    questionIns = questionIns.replace("||_rangeMax_||", qDict["max_label"])
  
  elif isType == "multiselect":
    if qDict["multiple_option_responses"]:
      questionIns = questionIns.replace("||_selectorType_||", "multiSelect")
    else:
      questionIns = questionIns.replace("||_selectorType_||", "singleSelect")

    options = ""
    surveyQuestID = ""
    for option in qDict["options"]:
      surveyQuestID = str(option["survey_question_id"])
      if (option["text"] == "Other") or (option["type"]=='SurveyQuestionOtherOption'):
        options += '<div class="option otherBox" data-name="other'+surveyQuestID+'">Other</div>'
      else:
        options += '<div class="option">'+option["text"]+'</div>'

    options += '<div class="otherResponse" id="other'+surveyQuestID+'">'
    options += '<input type="text" class="inputResp" />'
    options += "</div>"

    questionIns = questionIns.replace("||_options_||", options)


  return questionIns