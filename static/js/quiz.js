currQuestion = 0;
$(document).ready(function(){
  console.log("This was loaded correctly.");
  SetOptionClicks();
  LoadNextQuestion();

  $(".nextQuestion").click(LoadNextQuestion);
});


function LoadNextQuestion(){
  $(".questionBlock").css("display", "none");
  $(".questionBlock:eq(" +String(currQuestion) + ")").css("display", "block");

  currQuestion += 1;
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
