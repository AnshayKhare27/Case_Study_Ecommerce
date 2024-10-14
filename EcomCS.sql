create database EcomCS;

use EcomCS;

create table customers(
customer_id INT PRIMARY KEY,
name VARCHAR(20) NOT NULL,
email VARCHAR(30) NOT NULL,
password VARCHAR(15) NOT NULL);

create table products(
product_id INT PRIMARY KEY,
name VARCHAR(20) NOT NULL,
price decimal,
description VARCHAR(30),
stockQuantity int);

create table cart(
cart_id INT PRIMARY KEY,
customer_id INT FOREIGN KEY REFERENCES customers(customer_id),
product_id INT FOREIGN KEY REFERENCES products(product_id),
quantity int);

create table orders(
order_id INT PRIMARY KEY,
customer_id INT FOREIGN KEY REFERENCES customers(customer_id),
order_date Varchar(15),
total_price decimal,
shipping_address Varchar(30));

create table order_items(
order_item_id INT PRIMARY KEY,
order_id INT FOREIGN KEY REFERENCES orders(order_id),
product_id INT FOREIGN KEY REFERENCES products(product_id),
quantity INT);