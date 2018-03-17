import psycopg2
import json
from operator import itemgetter
from pprint import pprint


database = "d7vi1mstte1dkp"
user = "kdenbwpcekclck"
host = "ec2-54-197-254-189.compute-1.amazonaws.com"
port ='5432'
password = "a7ed71fef239b7582c87af0a14c25bb89b4f86f6d66f19d577a7db9b38512094"

# database = "wrapt_gratitude_development"
# user = "srikasip"
# host = "localhost"
# port =''
# password = ''


def getGifts():
  fileName = "grabData/getGifts.sql"
  jsonString = runFileStatement(fileName, [])

  return jsonString

def getSurveyQuestions(expID):
  fileName = "grabData/grabQuizData.sql"
  replacers = [{"holdText": "||_id_||", "replaceText": str(expID)}]
  jsonString = runFileStatement(fileName, replacers)

  #quizObj = json.load(jsonString)

  return jsonString #quizObj

def runFileStatement(filename, replaceVars):
  with open(filename, "rU") as sqlHandle:
    cmdStatement = sqlHandle.read()

  for replacer in replaceVars:
    cmdStatement = cmdStatement.replace(replacer["holdText"], replacer["replaceText"])

  retData = connectToDB(cmdStatement)
  return retData

def connectToDB(command):
  conn = psycopg2.connect("dbname='"+database+"' user='"+user+"' host='"+host+"' password='"+password+"' port="+port)
  cur = conn.cursor()
  cur.execute(command)
  allData = cur.fetchall()[0][0]
  
  conn.close()
  return allData







