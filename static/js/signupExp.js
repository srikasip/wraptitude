$(document).ready(function(){
  expGroup = experimentGroup;
  expName = "Signup_PreRec"

  //Log when the page loads and which group the user is in
  PageLoadsAnalytics(expName, expGroup);
  $("#signup").click(function(){SignupClicked(expName, expGroup);});

  $(".addCart").click(function(){AddedToCart(expName, expGroup);});
  $(".next, .prev, .mover, .demo").click(function(){RecsEngaged(expName, expGroup);});
  $(".checkoutBtn").click(function(){CheckedOut(expName, expGroup);});
});

function PageLoadsAnalytics(exp_name, exp_group) {
  exp_event = "Impression";
  PassEvent(exp_name, exp_event, exp_group);
}

function SignupClicked(exp_name, exp_group){
  exp_event = "Signup";
  PassEvent(exp_name, exp_event, exp_group);
}
function RecsEngagedOnce(exp_name, exp_group){
  exp_event = "RecsEngagedOnce";
  PassEvent(exp_name, exp_event, exp_group);
}
function RecsEngagedOnce(exp_name, exp_group){
  exp_event = "AddedToCartOnce";
  PassEvent(exp_name, exp_event, exp_group);
}

function RecsEngaged(exp_name, exp_group){
  exp_event = "RecsEngaged";
  PassEvent(exp_name, exp_event, exp_group);
}
function AddedToCart(exp_name, exp_group){
  exp_event = "AddedToCart";
  PassEvent(exp_name, exp_event, exp_group);
}
function CheckedOut(exp_name, exp_group){
  exp_event = "CheckedOut";
  PassEvent(exp_name, exp_event, exp_group);
}

function PassEvent(exp_category, exp_action, exp_label){
  gtag('event', exp_action, {'event_category' : exp_category,'event_label' : exp_label});
}