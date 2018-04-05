Select opt.text, opt.configuration_string
FROM co_survey_responses as resp 
  JOIN survey_question_options as opt
  on resp.response_id = opt.id 
WHERE resp.co_profile_id = ||_profile_id_||
  AND (opt.configuration_string = '') is FALSE;