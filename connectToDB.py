import psycopg2
import json
from operator import itemgetter
from pprint import pprint


database = "d9hm1onbau0jau"
user = "qyobxzafmewrue"
host = "ec2-54-204-44-140.compute-1.amazonaws.com"
port ='5432'
password = "7c7a685d1ab55da990cc12198a9cc64783d9586bcdbc9941a19fabe3311d3438"

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

  return jsonString

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