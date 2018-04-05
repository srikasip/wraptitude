WITH allRecs AS (
  SELECT g.id, g.title, g.wrapt_sku, gCat.name as Category, gSubCat.name as SubCategory, ting.taggable_id, count(ting.tag_id) as score,
  ROW_NUMBER() OVER(PARTITION BY gCat.name, gSubCat.name ORDER BY count(ting.tag_id) desc) as rk
  FROM taggings as ting 
    JOIN tags 
      ON ting.tag_id = tags.id
    JOIN gifts as g 
      ON g.id = ting.taggable_id 
    JOIN product_categories as gCat
      ON g.product_category_id = gCat.id
    JOIN product_categories as gSubCat
      ON g.product_subcategory_id = gSubCat.id

  WHERE tags.name in (||_BOOST_TAGS_||)
    AND ting.taggable_id not in (SELECT eting.taggable_id
                                  FROM taggings as eting JOIN tags as etags
                                  ON eting.tag_id = etags.id
                                  WHERE etags.name in (||_EXCLUDE_TAGS_||)
                                  )
    AND g.selling_price >= ||_MIN_PRICE_||
    AND g.selling_price <= ||_MAX_PRICE_||
  GROUP BY ting.taggable_id, g.wrapt_sku, g.title, g.id, gCat.name, gSubCat.name
  ORDER BY score desc
)

SELECT rec.* 
  FROM allRecs as rec
WHERE rec.rk = 1
ORDER BY rec.score desc
LIMIT(6);