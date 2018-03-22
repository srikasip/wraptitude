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


app = Flask(__name__)

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
  # inExp = random.choice(["experiment", "control"])
  inExp = "control"
  if inExp == "experiment":
    expID = "16"
    templateURL = "templates/quizStuff/quiz.html"
  else:
    expID = "16"
    templateURL = "templates/quizStuff/quiz.html"

  quizDict = dbHand.getSurveyQuestions(expID)
  quizPage = quizB.LoadQuiz(templateURL, quizDict, questionID, occasionID)
  quizPage = quizPage.replace("||_experiment_group_||", inExp)

  #return render_template('quizStuff/quizTester.html')
  return render_template_string(quizPage)

@app.route("/profile", methods=['POST'])
def saveProfile():
  profile = request.get_json()
  response = {"profileID": 1}
  return jsonify(response)


@app.route("/recs/<int:profileID>")
def getRecommendation(profileID):
  recs = dbHand.getGifts()
  inExp = random.choice(["experiment", "control"])

  if inExp == "experiment":
    templateURL = "templates/recStuff/recTemplateSignup.html"
  else:
    templateURL = "templates/recStuff/recTemplate.html"
  
  expData = {}
  expData["Signup"] = {"Category": "Signup_SignupBeforeRec",
                       "Action": inExp
                      }
  recPage = recB.BuildRecommendations(templateURL, recs)
  recPage = recPage.replace('"||_experiment_group_||"', json.dumps(expData))
  #return render_template("recStuff/recTrial.html")
  return render_template_string(recPage)

if __name__ == '__main__':
  app.run()
