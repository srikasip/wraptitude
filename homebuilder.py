import json


def LoadHome(sentQuiz, templateURL):
  with open(templateURL, "rU") as templateHandle:
    homeTemplate = templateHandle.read()

  #Update the occassion question
  occasionQ = sentQuiz["questions"][0]
  homePage = homeTemplate.replace("||_occasionQID_||", str(occasionQ["id"]))

  options = ""
  for occ in occasionQ["options"]:
    option = '<div class="occasion" id="'+str(occ["id"])+'" data-question="'+str(occ["survey_question_id"])+'" '
    option += 'style="background-image: url(\'static/images/occasion/'+occ['image']+'\');">'
    option += '<div>' + occ["text"] + '</div>'
    option += '</div>'
    options += option + "\n"

  homePage = homePage.replace("||_AddOccasions_||", options)

  return homePage
