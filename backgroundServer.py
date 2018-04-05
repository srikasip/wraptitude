from flask import Flask
from flask import render_template
from flask import render_template_string
from flask import request
from flask import jsonify
import json
from datetime import datetime
import connectToDB as dbHand
import quizbuilder as quizB
from flask import request
from pprint import pprint
import homebuilder as homeB
import recbuilder as recB
import random
from pprint import pprint


app = Flask(__name__)

# @app.route('/backend')
# def blah():
#   dbHand.getRecSet(28)
#   return "Hello World"

@app.route('/')
def index():
  #TODO: I can render different templates depending on whether we run an experiment
  # inExp = random.choice(["experiment", "control"])
  inExp = "control"
  if inExp == "experiment":
    expID = "16"
    templateURL = "templates/homeTemplate.html"
  else:
    expID = "16"
    templateURL = "templates/homeTemplate.html"

  expData = {}
  quizDict = dbHand.getSurveyQuestions(expID)
  homePage = homeB.LoadHome(quizDict, templateURL)
  
  return render_template_string(homePage)

@app.route('/quiz/<string:questionID>/<string:occasionID>')
def getQuiz(questionID, occasionID):
  #TODO: Render different templates for the quiz from the database.
  #inExp = random.choice(["experiment", "control"])
  inExp = random.choice(["experiment", "control"])
  inExp = 'control'
  if inExp == "experiment":
    expID = "30"
    templateURL = "templates/quizStuff/quiz.html"
  else:
    expID = "16"
    templateURL = "templates/quizStuff/quiz.html"

  quizDict = dbHand.getSurveyQuestions(expID)
  quizPage = quizB.LoadQuiz(templateURL, quizDict, questionID, occasionID)
  quizPage = quizPage.replace("||_experiment_group_||", inExp)
  
  return render_template_string(quizPage)

@app.route("/profile", methods=['POST'])
def saveProfile():
  profile = request.get_json()
  profID = dbHand.loadQuizProfile()
  print("\n\n\nPROFILE ID: " + str(profID))
  dbHand.loadQuiz(profile["profile"], profID)
  response = {"profileID": profID}
  return jsonify(response)

@app.route("/checkout")
def getCheckout():
  return render_template("checkout/checkout.html")

@app.route("/recs/<int:profileID>")
def getRecommendation(profileID):

  # gSet1 = "('G-DB-JWL-EAR-006','G-DB-JWL-NEC-001','G-IH-ACS-SCF-001','G-ML-ACS-BAG-003','G-ET-CNS-GAS-003','G-AL-BNB-BTH-003')"
  # gSet2 = "('G-GH-GDN-GAC-001','G-IH-ACS-SCF-002','G-GH-TBT-SVW-006','G-KF-JWL-EAR-007','G-LS-TBT-SVW-004','G-DB-JWL-NEC-007')"

  giftSet = dbHand.getRecSet(profileID)
  giftSetString = "(" + ",".join(giftSet) + ")"
  recs = dbHand.getGifts(giftSetString)
  pprint(recs)
  inExp = random.choice(["experiment", "control"])
  if inExp == "experiment":
    templateURL = "templates/recStuff/recTemplate.html"
  else:
    templateURL = "templates/recStuff/recTemplateSignup.html"

  recPage = recB.BuildRecommendations(templateURL, recs)
  recPage = recPage.replace('||_experiment_group_||', inExp)
  #return render_template("recStuff/recTrial.html")
  return render_template_string(recPage)

if __name__ == '__main__':
  app.run()

