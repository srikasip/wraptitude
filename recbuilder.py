import json


def BuildRecommendations(recTemplateUrl, recDict):
  recTemplateHandle = recTemplateUrl
  recBlockHandle = "templates/recStuff/recBlock.html"
  carBlockHandle = "templates/recStuff/carouselBlock.html"
  subCarBlockHandle = "templates/recStuff/subCarouselBlock.html"

  with open(recTemplateHandle, "rU") as recHandle:
    recTemplate = recHandle.read()
  with open(recBlockHandle, "rU") as rbHandle:
    recBlock = rbHandle.read()
  with open(carBlockHandle, "rU") as cbHandle:
    carBlock = cbHandle.read()
  with open(subCarBlockHandle, "rU") as scbHandle:
    subCarBlock = scbHandle.read()


  allRecs = ""
  allCars = ""
  main_counter = 1
  for rec in recDict:
    oneRec = recBlock.replace("||_gift_id_||", str(rec["id"]))
    oneRec = oneRec.replace("||_gift_title_||", rec["title"])
    oneRec = oneRec.replace("||_gift_description_||", rec["description"])
    oneRec = oneRec.replace("||_selling_price_||", '%.2f' % rec["selling_price"])
    oneRec = oneRec.replace("||_carousel_display_||", str(rec["id"]))

    subCarHtml = ""
    toplineImg = ""
    if len(rec["images"]) > 1:
      subCarHtml = subCarBlock.replace("||_num_images_||", str(len(rec["images"])))
      subCarImages = ""
      count = 1
      for image in rec["images"]:
        subCarImages += '<img id="rec'+str(rec["id"])+'_'+str(count)+'" class="recSubImage' 
        if count == 1:
          subCarImages += ' showSubImage'
          #toplineImg = 'https://wrapt-gratitude-production.s3.amazonaws.com/uploads/' + image["image_url"]
        subCarImages += '" src="https://wrapt-gratitude-production.s3.amazonaws.com/uploads/'
        subCarImages += image["image_url"]+'" />'
        subCarImages += "\n"
        count += 1
      subCarHtml = subCarHtml.replace("||_sub_images_||",subCarImages)

    else:
      subCarHtml = '<div class="giftShowcase" style="background-image:url(\'https://wrapt-gratitude-production.s3.amazonaws.com/uploads/'
      subCarHtml += rec["images"][0]["image_url"]+'\');"></div>'
      #toplineImg = 'https://wrapt-gratitude-production.s3.amazonaws.com/uploads/' + rec["images"][0]["image_url"]

    toplineImg = 'https://wrapt-gratitude-production.s3.amazonaws.com/uploads/' + rec["carousel_img"][0]["image_url"]
    oneRec = oneRec.replace("||_showcase_block_||", subCarHtml)
    oneCar = '<img class="demo cursor" data-assoc=' + str(main_counter)
    oneCar += ' id="tn_'+ str(rec["id"])+'" src="'+toplineImg+'" />'
    oneCar = carBlock.replace("||_carousel_item_||", oneCar)
    oneCar += "\n"

    allRecs += oneRec
    allCars += oneCar

    main_counter += 1

  recPage = recTemplate.replace("||_RecommendationSlides_||", allRecs)
  recPage = recPage.replace("||_CarouselColumns_||", allCars)

  return recPage
