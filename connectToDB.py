import psycopg2
import json
from operator import itemgetter
from pprint import pprint


# database = "d47tunqullfegl"
# user = "hsjcwbnmmxtndd"
# host = "ec2-54-225-255-132.compute-1.amazonaws.com"
# port ='5432'
# password = "d0b8ebd8460008cb897a7afc2cee5faeb3134dc5d1a37ed4edac1f1e2fc4ef31"

database = "wrapt_gratitude_development"
user = "srikasip"
host = "localhost"
port =''
password = ''

# database = "SurgFakeNameDB"
# user = "srikasip"
# host = "localhost"
# port =''
# password = ''

def getSurveyQuestions(expID):
  fileName = "grabData/grabQuizData.sql"
  replacers = [{"holdText": "||id||", "replaceText": str(expID)}]
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
