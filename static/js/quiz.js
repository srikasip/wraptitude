currQuestion = 0;
$(document).ready(function(){
  console.log("This was loaded correctly.");
  LoadNextQuestion();

  $(".nextQuestion").click(LoadNextQuestion);
});


function LoadNextQuestion(){
  $(".questionBlock").css("display", "none");
  $(".questionBlock:eq(" +String(currQuestion) + ")").css("display", "block");

  currQuestion += 1;
}
