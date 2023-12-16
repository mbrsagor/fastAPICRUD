SELECT * FROM products WHERE id =2 or id=10 or id=3;
INSERT INTO products (name, price, inventory) VALUES ('car', 3939, 8);
SELECT * FROM posts LEFT JOIN users ON posts.owner_id = users.id
SELECT * FROM posts RIGHT JOIN users ON posts.owner_id = users.id
