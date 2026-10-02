SELECT c.category_id, c.category, c.description, nc.notecard_id 
  FROM category c LEFT JOIN notecard_category nc ON c.category_id = nc.category_id AND 0<=nc.notecard_id
  order by 2;