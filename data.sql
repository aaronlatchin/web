CREATE TABLE drinks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_of_drink VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) ,
    quantity INT,
    expiry_date DATE,
    batch_no VARCHAR(100),
    drink_subtype VARCHAR(100)
);
