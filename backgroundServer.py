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

app = Flask(__name__)

@app.route('/')
def index():
  #TODO: I can render different templates depending on whether we run an experiment
  quizDict = dbHand.getSurveyQuestions("16")
  homePage = homeB.LoadHome(quizDict, "templates/homeTemplate.html")
  return render_template_string(homePage)

@app.route('/quiz/<string:questionID>/<string:occasionID>')
def getQuiz(questionID, occasionID):
  #TODO: Render different templates for the quiz from the database.
  quizDict = dbHand.getSurveyQuestions("16")
  quizPage = quizB.LoadQuiz("templates/quizStuff/quiz.html", quizDict, questionID, occasionID)
  #return render_template('quizStuff/quizTester.html')
  return render_template_string(quizPage)

@app.route("/profile", methods=['POST'])
def saveProfile():
  profile = request.get_json()
  response = {"profileID": 1}
  return jsonify(response) #render_template("recStuff/recTrial.html")

@app.route("/recs/<int:profileID>")
def getRecommendation(profileID):
  recs = dbHand.getGifts()
  recPage = recB.BuildRecommendations(recs)
  return render_template_string(recPage)


if __name__ == '__main__':
  app.run()
