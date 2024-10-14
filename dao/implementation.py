import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Tuple
from dao.serviceProvider import OrderProcessorRepository
from util.DBUtil import DBConnection
from util.propertyUtil import PropertyUtil
from entity.customers import Customers  
from entity.products import Products
from exception.CustomerNotFound import CustomerNotFound
from exception.ProductNotFound import ProductNotFound
from exception.OrderNotFound import OrderNotFound

class OrderProcessorRepositoryImpl(OrderProcessorRepository):

    def __init__(self):
        self.DBUtil = DBConnection()

    def createProduct(self, products : Products):
        try:
            conn = self.DBUtil.getConnection()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO [products] (product_id,name,price,description,stockQuantity) VALUES (?,?,?,?,?)", products.product_id, products.name, products.price, products.description, products.stockQuantity)
            conn.commit()
            print("Product Created Successfully!")
            conn.close()
            return True

        except Exception as e :
            print("Error:", e)
            return False

            
    def createCustomer(self, customers : Customers):
        try:
            conn = self.DBUtil.getConnection()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO [customers] (customer_id,name,email,password) VALUES(?,?,?,?)", customers.customer_id, customers.name, customers.email,customers.password)
            conn.commit()
            print("Customer Created Successfully!")
            conn.close()
            return True

        except Exception as e :
            print("Error:", e)
            return False

    
    def deleteProduct(self, product_id : int):
        try:
            conn = self.DBUtil.getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM [products] WHERE product_id = ?", product_id)
            product_count = cursor.fetchone()[0]
            if(product_count==0):
                raise ProductNotFound(f"Product with ID {product_id} not found.")

            cursor.execute("DELETE FROM [products] WHERE product_id = ?", product_id)
            conn.commit()
            print("Product Deleted Successfully!")
            conn.close() 
            return True
        
        except ProductNotFound as e:
            print("Error :", e)
            return False

        except Exception as e:
            print("Error :", e)
            return False
                


    def deleteCustomer(self, customer_id : int):
        try:
            conn = self.DBUtil.getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM [customers] WHERE customer_id = ?", customer_id)
            customer_count = cursor.fetchone()[0]
            if(customer_count==0):
                raise CustomerNotFound(f"Customer with ID {customer_id} not found.")

            cursor.execute("DELETE FROM [customers] WHERE customer_id = ?", customer_id)
            conn.commit()
            print("Customer Deleted Successfully!")
            conn.close() 
            return True
        
        except CustomerNotFound as e:
            print("Error :", e)
            return False

        except Exception as e:
            print("Error :", e)
            return False



    def addToCart(self , customers : Customers, products : Products, quantity : int):
        try:
            conn = self.DBUtil.getConnection()
            cursor = conn.cursor()

            cursor.execute("SELECT MAX(cart_id) FROM cart")
            max_cart_id = cursor.fetchone()[0]
            if max_cart_id is None:
                new_cart_id = 1  # Start from 1 if no entries exist
            else:
                new_cart_id = max_cart_id + 1

            cursor.execute("SELECT COUNT(*) FROM [customers] WHERE customer_id = ?", customers.customer_id)
            customer_count = cursor.fetchone()[0]
            if(customer_count==0):
                raise CustomerNotFound(f"Customer with ID {customers.customer_id} not found.")
            
            cursor.execute("SELECT COUNT(*) FROM [products] WHERE product_id = ?", products.product_id)
            product_count = cursor.fetchone()[0]
            if(product_count==0):
                raise ProductNotFound(f"Product with ID {products.product_id} not found.")

            
            cursor.execute("INSERT INTO [cart] (cart_id,customer_id,product_id,quantity) VALUES(?,?,?,?)",new_cart_id,customers.customer_id,products.product_id,quantity)
            conn.commit()
            print("Item Added to Cart!!")
            conn.close()
            return True

        except CustomerNotFound as e:
            print("Error :", e)
            return False

        except ProductNotFound as e:
            print("Error :", e)
            return False

        except Exception as e:
            print("Error :", e)
            return False



    def removeFromCart(self, customers : Customers, products : Products):
        try:
            conn = self.DBUtil.getConnection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM [cart] WHERE customer_id = ?", customers.customer_id)
            customer_count = cursor.fetchone()[0]
            if(customer_count==0):
                raise CustomerNotFound(f"Customer with ID {customers.customer_id} not found.")
            
            cursor.execute("SELECT COUNT(*) FROM [cart] WHERE product_id = ?", products.product_id)
            product_count = cursor.fetchone()[0]
            if(product_count==0):
                raise ProductNotFound(f"Product with ID {products.product_id} not found.")

            cursor.execute("DELETE FROM [cart] WHERE customer_id = ? and product_id = ?", customers.customer_id, products.product_id)
            conn.commit()
            print("Cart Updated Successfully!")
            conn.close() 
            return True


        except CustomerNotFound as e:
            print("Error :", e)
            return False

        except ProductNotFound as e:
            print("Error :", e)
            return False

        except Exception as e:
            print("Error :", e)
            return False



    def getAllFromCart(self, customers : Customers):
        try:
            conn = self.DBUtil.getConnection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM [cart] WHERE customer_id = ?", customers.customer_id)
            customer_count = cursor.fetchone()[0]
            if(customer_count==0):
                raise CustomerNotFound(f"Customer with ID {customers.customer_id} not found.")

            cursor.execute("SELECT * FROM [cart] WHERE customer_id = ?", customers.customer_id)

            items = cursor.fetchall()
            conn.close()
            return items

        except CustomerNotFound as e:
            print("Error :", e)
            return None

        except Exception as e:
            print("Error :", e)
            return None


    def placeOrder(self, customers : Customers, items: List[Tuple[Products, int]], shippingAddress: str):
        try:
            conn = self.DBUtil.getConnection()
            cursor = conn.cursor()

            #Customer existence check
            cursor.execute("SELECT COUNT(*) FROM [customers] WHERE customer_id = ?", customers.customer_id)
            customer_count = cursor.fetchone()[0]
            if(customer_count==0):
                raise CustomerNotFound(f"Customer with ID {customers.customer_id} not found.")

            #Updating Orders Table
            cursor.execute("SELECT MAX(order_id) FROM [orders]")
            max_order_id=cursor.fetchone()[0]
            if max_order_id is None:
                new_order_id = 1
            else:
                new_order_id = max_order_id + 1
            total_price = self.calculate_total_price(items)
            cursor.execute("INSERT INTO [orders] (order_id, customer_id, order_date, total_price, shipping_address) VALUES (?, ?, GETDATE(), ?, ?)", new_order_id, customers.customer_id, total_price, shippingAddress)

            #Updating Order Items Table
            cursor.execute("SELECT MAX(order_item_id) FROM order_items")
            max_order_item_id=cursor.fetchone()[0]
            if max_order_item_id is None:
                new_order_item_id = 1
            else:
                new_order_item_id = max_order_item_id + 1

            for product, quantity in items:
                cursor.execute("INSERT INTO order_items (order_item_id, order_id, product_id, quantity) VALUES (?, ?, ?, ?)",(new_order_item_id, new_order_id, product.product_id, quantity))
                new_order_item_id += 1      # Increment for each order item

                cursor.execute("UPDATE products SET stockQuantity = stockQuantity - ? WHERE product_id = ?", (quantity, product.product_id))

            conn.commit()
            print("Order Placed Successfully!") 
            return True

        except CustomerNotFound as e:
            print("Error :", e)
            return False
        except Exception as e:
            print(f"Error placing order: {e}")
            return False
        finally:
            cursor.close()


    def calculate_total_price(self, product_quantity_map: List[Tuple[Products, int]]) -> float:
        total_price = 0.0
        for product, quantity in product_quantity_map:
            total_price += float(product.get_price() * quantity)
        return total_price


    
    def getOrdersByCustomer(self, customer_id : int):
        try:
            conn = self.DBUtil.getConnection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT oi.product_id, oi.quantity, p.price, p.description, p.stockQuantity "
                "FROM orders o "
                "JOIN order_items oi ON o.order_id = oi.order_id "
                "JOIN products p ON oi.product_id = p.product_id "
                "WHERE o.customer_id = ?", 
                (customer_id)
                )
            rows = cursor.fetchall()
            print("Fetched rows:", rows)
            orders={}
            for row in rows:
                product_id = row[0]          # product_id from order_items
                quantity = row[1]            # quantity from order_items
                price = row[2]               # price from products
                description = row[3]         # description from products
                stock_quantity = row[4]      # stockQuantity from products

                product = Products(
                    product_id=product_id, 
                    name=None,
                    price=price,
                    description=description, 
                    stockQuantity=stock_quantity
                ) 
                orders[product] = quantity  # quantity
            return orders
        except Exception as e:
            print(f"Error retrieving orders: {e}")
            return {}


    def get_customer_by_id(self, customer_id: int) -> Customers:
        try:
            conn = self.DBUtil.getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id))
            row = cursor.fetchone()
            if row:
                return Customers(row[0], row[1], row[2], row[3])  # Adjust index based on your schema
            else:
                return None  # No customer found
        except Exception as e:
            print(f"Error retrieving customer: {e}")
            return None


    def get_product_by_id(self, product_id: int) -> Products :
        try:
            conn = self.DBUtil.getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id))
            row = cursor.fetchone()  # Return the entire row as a tuple
            if row:
                return Products(row[0], row[1], row[2], row[3], row[4])  # Adjust index based on your schema
            else:
                return None
        except Exception as e:
            print(f"Error retrieving product: {e}")
            return None