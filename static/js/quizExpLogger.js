$(document).ready(function(){
  expGroup = experimentGroup;
  expName = "Quiz_RmvName_MatrixEnd"

  //Log when the page loads and which group the user is in
  LoadQuestionAnal(2,expName,expGroup);
  AnswerQuestionAnal(1,expName,expGroup);
  $(".nextQuestion, .lastQuestion").click(function(){
    qID = $(this).parent().attr("data-order");
    AnswerQuestionAnal(qID,expName, expGroup);
    LoadQuestionAnal(parseInt(qID)+1,expName, expGroup);
  });
});

function LoadQuestionAnal(qNum, expName, expGroup){
  expLabel = expGroup + ":" + String(qNum);
  expAction = "Impression";
  PassEvent(expName, expAction, expLabel);
}
function AnswerQuestionAnal(qNum, expName, expGroup){
  expLabel = expGroup + ":" + String(qNum);
  expAction = "Engaged";
  PassEvent(expName, expAction, expLabel);
}

function PassEvent(exp_category, exp_action, exp_label){
  gtag('event', exp_action, {'event_category' : exp_category,'event_label' : exp_label});
}