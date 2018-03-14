SELECT row_to_json(t)
FROM
  (
    SELECT s.id, s.title, (select array_to_json(array_agg(row_to_json(qs))) FROM (
      SELECT q.id, q.type, q.sort_order, q.prompt, 
        q.min_label, q.max_label, q.multiple_option_responses,(select array_to_json(array_agg(row_to_json(os))) FROM (
          SELECT o.id, o.survey_question_id, o.text, o.image, o.sort_order, o.type, o.explanation, o.configuration_string
          FROM survey_question_options as o
          WHERE o.survey_question_id = q.id
          ORDER BY o.sort_order
          ) os ) as options
      FROM survey_questions as q
      WHERE q.survey_id = s.id
      ORDER BY q.sort_order
      ) qs ) as questions
    FROM surveys as s
    WHERE s.id = ||id||
  ) t;
