currQuestion = 0;
responses = {};
$(document).ready(function(){
  console.log("This was loaded correctly.");
  SetOptionClicks();
  LoadQuestions();
});

function LoadFirstQuestion(){
  $(".questionBlock").css("display", "none");
  $(".questionBlock:eq(" +String(currQuestion) + ")").css("display", "block");

  currQuestion += 1;
}

function LoadQuestions(){
  $(".nextQuestion, .lastQuestion").click(function(){
    var is_valid = true;

    if(currQuestion>=1){
      $qBox = $(this).parent();
      qType = $qBox.attr("data-element");
      qID = $qBox.attr("id");

      //responses["response"] = [];
      if((qType == "text")||(qType == "slider")){
        response = ""
        response = $qBox.find("input").val().trim();
        if(response == ""){is_valid = false;}
      }
      else{
        response = []
        $qBox.find(".option.selected").each(function(index){
          datName = $(this).attr("data-name");
          if(datName.indexOf("other") != -1){
            otherTxt = $("#"+datName + " input").val().trim();
            datName = "__other__" + otherTxt
            if(otherTxt.length == 0){
              is_valid = false;
            }
          }
          response.push(datName);
        });
        if(response.length == 0){
          is_valid = false;
        }
      }

      responses[qID] = response;
    }
    if(($(this).hasClass("nextQuestion")) && (is_valid)){
      LoadFirstQuestion();
    }
    else if(is_valid){
      CompleteQuiz();
    }
  });
  LoadFirstQuestion();
}

function CompleteQuiz(){
  responses[question] = [occasion]
  //console.log(responses);

  $.ajax({
    url: '/profile',
    data: JSON.stringify({'profile': responses}),
    contentType: "application/json",
    type: "POST"
  })
    .done(function(data) {
      console.log( "success" );
      window.location.replace("/recs/" + String(data["profileID"]));
    })
    .fail(function(data) {
      console.log( "error" );
    })
    .always(function(data, status) {
    });
}

function SetOptionClicks(){
  $(".multiSelect .option").click(function(){
    if($(this).hasClass("selected")){
      $(this).removeClass('selected');
    }
    else{
      $(this).addClass('selected');
    }
  });
  $(".singleSelect .option").click(function(){
    if($(this).hasClass("selected")){
      $(this).removeClass('selected');
    }
    else{
      if($(this).parent().find(".otherBox").hasClass("selected")){
        var otherBox_id = "#" + $(this).parent().find(".otherBox").attr("data-name");
        $(otherBox_id).css("display", "none");
        console.log(otherBox_id);
      }
      $(".selected").removeClass("selected");
      $(this).addClass('selected');
    }
  });

  $(".otherBox").click(function(){
    var otherBox_id = "#" + $(this).attr("data-name")
    if($(otherBox_id).css("display")=="none"){
      $(otherBox_id).css("display", "block");
      $(otherBox_id).focus();
    }
    else{
      $(otherBox_id).css("display", "none");
    }

  });
}
