from flask import Flask
from flask import render_template
from flask import render_template_string
from flask import request
from flask import jsonify
import json
from datetime import datetime
import connectToDB as dbHand
import quizbuilder as quizB


app = Flask(__name__)

@app.route('/')
def index():
  #TODO: I can render different templates depending on whether we run an experiment
  return render_template("home.html")

@app.route('/quiz')
def getQuiz():
  #TODO: Render different templates for the quiz from the database.
  quizDict = dbHand.getSurveyQuestions("16")
  quizPage = quizB.LoadQuiz(quizDict)

  return render_template_string(quizPage)

if __name__ == '__main__':
  app.run()