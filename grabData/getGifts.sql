SELECT array_to_json(array_agg(row_to_json(t)))
FROM
  (
    SELECT g.id, g.title, g.description, g.selling_price, 
    cat.name as Category, subCat.name as SubCategory, 
      (Select array_to_json(array_agg(row_to_json(imgs))) FROM (
        SELECT gimg.gift_id, gimg.sort_order, 
          CASE WHEN gimg.product_image_id >= 1
            THEN pimg.image ELSE gimg.image END as image_url, 
          CASE WHEN gimg.product_image_id >= 1  
            THEN pimg.height ELSE gimg.height END as height, 
          CASE WHEN gimg.product_image_id >= 1
            THEN pimg.width ELSE gimg.width END as width
        FROM gift_images as gimg
        LEFT JOIN product_images as pimg
         ON gimg.product_image_id = pimg.id 
        WHERE gimg.gift_id = g.id
        Order by gimg.gift_id, gimg.sort_order
      ) imgs ) as images,
      (
        SELECT array_to_json(array_agg(row_to_json(ts))) FROM(
          SELECT tag.name, tag.taggings_count
          FROM taggings as t 
          JOIN tags as tag
          ON t.tag_id = tag.id
          Where taggable_id = g.id
        ) ts) as tags,
      (SELECT array_to_json(array_agg(row_to_json(img_car))) FROM(
        SELECT gimg.sort_order, 
          CASE WHEN gimg.product_image_id >= 1
            THEN pimg.image ELSE gimg.image END as image_url, 
          CASE WHEN gimg.product_image_id >= 1  
            THEN pimg.height ELSE gimg.height END as height, 
          CASE WHEN gimg.product_image_id >= 1
            THEN pimg.width ELSE gimg.width END as width
        FROM gift_images as gimg
        LEFT JOIN product_images as pimg
         ON gimg.product_image_id = pimg.id 
        WHERE gimg.gift_id = g.id 
          and ((gimg.product_image_id>=1 and pimg.width>pimg.height) or (gimg.width>gimg.height) or (gimg.product_image_id>=1 and pimg.width<=pimg.height) or (gimg.width<=gimg.height))
        Order by gimg.gift_id, gimg.sort_order
        LIMIT(1)) img_car) as carousel_img
      FROM 
        gifts as g
        Join product_categories as cat 
          On g.product_category_id = cat.id
        Join product_categories as subCat 
          On g.product_subcategory_id = subCat.id
      WHERE
        g.wrapt_sku in ||//FixedSetOfGifts//||
  ) t;

