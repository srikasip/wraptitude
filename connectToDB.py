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


def getRecSet(profID):
  #Gather the tags associated with the question responses for a given profile id
  fileName = 'grabData/getProfileTags.sql'
  replacers = [{"holdText": "||_profile_id_||", "replaceText": str(profID)}]
  profTags = runFileStatementGetSet(fileName, replacers)
  print(profTags)
  #Get a list of scored gift-candidates (ordered by score)
  mergedTags = extractTags(profTags)
  fileName = 'grabData/BuildRecSet.sql'
  replacers = []
  replacers.append({"holdText":"||_BOOST_TAGS_||", "replaceText": "'" + "','".join(mergedTags["boost_tags"]) + "'"})
  replacers.append({"holdText":"||_EXCLUDE_TAGS_||", "replaceText":"'" + "','".join(mergedTags["exclude_tags"]) + "'"})
  replacers.append({"holdText":"||_MIN_PRICE_||", "replaceText":str(mergedTags["price_range"]["min_price"])})
  replacers.append({"holdText":"||_MAX_PRICE_||", "replaceText":str(mergedTags["price_range"]["max_price"])})

  giftsSet = runFileStatementGetSet(fileName, replacers)
  skus = []
  for gift in giftsSet:
    skus.append("'" + gift[2] + "'")

  return skus
  

def extractTags(profTags):
  tagMerge = {
              "exclude_tags":[],
              "boost_tags":[],
              "price_range":{"min_price":10000, "max_price":0}
            }
  for resp in profTags:
    print(resp)
    tagBlock = resp[1]
    tagBlock = "{" + tagBlock + "}"
    tagObj = json.loads(tagBlock)
    if "exclude_tags" in tagObj.keys():
      tagMerge["exclude_tags"] = tagMerge["exclude_tags"] + tagObj["exclude_tags"]
    if "boost_tags" in tagObj.keys():
      tagMerge["boost_tags"] = tagMerge["boost_tags"] + tagObj["boost_tags"]
    if "price_range" in tagObj.keys():
      if ("min_price" in tagObj["price_range"]) and (tagObj["price_range"]["min_price"] < tagMerge["price_range"]["min_price"]):
        tagMerge["price_range"]["min_price"] = tagObj["price_range"]["min_price"]
      if ("max_price" in tagObj["price_range"]) and (tagObj["price_range"]["max_price"] > tagMerge["price_range"]["max_price"]):
        tagMerge["price_range"]["max_price"] = tagObj["price_range"]["max_price"]

  if tagMerge["price_range"]["min_price"] == 10000:
    tagMerge["price_range"]["min_price"] = 0
  if tagMerge["price_range"]["max_price"] == 0:
    tagMerge["price_range"]["max_price"] = 100000

  return tagMerge

def loadQuizProfile():
  statement = "SELECT loadProfile();"
  profID = connectToDB(statement)

  return profID

def loadQuiz(allQuestionsDict, profileID):
  fileName = "grabData/SaveQuiz.sql"
  with open(fileName, "r") as quizPart:
    quizText = quizPart.read()

  valStatements = ""
  for questionID in allQuestionsDict.keys():
    qID = questionID
    if isinstance(allQuestionsDict[qID], list):
      for item in allQuestionsDict[qID]:
        if RepresentsInt(item):
          qVal = item
          valStatements += "\n("+str(profileID)+", "+qID+", "+qVal+"),"
  
  quizText += valStatements[:-1] + ";"

  insertToDB(quizText)


def RepresentsInt(s):
  try: 
      int(s)
      return True
  except ValueError:
      return False

def getGifts(listOfGifts):
  fileName = "grabData/getGifts.sql"
  replacers = [{"holdText": "||//FixedSetOfGifts//||", "replaceText": listOfGifts}]
  jsonString = runFileStatement(fileName, replacers)

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

def runFileStatementGetSet(filename, replaceVars):
  with open(filename, "rU") as sqlHandle:
    cmdStatement = sqlHandle.read()

  for replacer in replaceVars:
    cmdStatement = cmdStatement.replace(replacer["holdText"], replacer["replaceText"])

  retData = getDBTable(cmdStatement)
  return retData

def getDBTable(command):
  conn = psycopg2.connect("dbname='"+database+"' user='"+user+"' host='"+host+"' password='"+password+"' port="+port)
  cur = conn.cursor()
  cur.execute(command)
  allData = cur.fetchall()

  conn.commit()
  cur.close()
  conn.close()
  return allData

def connectToDB(command):
  conn = psycopg2.connect("dbname='"+database+"' user='"+user+"' host='"+host+"' password='"+password+"' port="+port)
  cur = conn.cursor()
  cur.execute(command)
  allData = cur.fetchall()[0][0]

  conn.commit()
  cur.close()
  conn.close()
  return allData

def insertToDB(command):
  conn = psycopg2.connect("dbname='"+database+"' user='"+user+"' host='"+host+"' password='"+password+"' port="+port)
  cur = conn.cursor()
  cur.execute(command)
  conn.commit()
  cur.close()
  conn.close()