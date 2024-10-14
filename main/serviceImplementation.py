import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dao.implementation import OrderProcessorRepositoryImpl
from entity.customers import Customers
from entity.products import Products

class EcomApp:
    def __init__(self):
        self.implementation = OrderProcessorRepositoryImpl()

    def main(self):
        while True:
            print("*********************************")
            print("*     Ecommerce Application     *")
            print("*********************************")
            print("1 . Create Product")
            print("2 . Register Customer")
            print("3 . Delete Product")
            print("4 . Delete Customer")
            print("5 . Add To Cart")
            print("6 . Remove From Cart")
            print("7 . Get All From Cart")
            print("8 . Place Order")
            print("9 . View Orders")
            print("10. EXIT")
            print("*********************************")  

            choice = int(input("Enter your choice(1-10): "))

            if choice == 1:
                self.create_product()
            elif choice == 2:
                self.create_customer()
            elif choice == 3:
                self.delete_product()
            elif choice == 4:
                self.delete_customer()
            elif choice == 5:
                self.add_to_cart()
            elif choice == 6:
                self.remove_from_cart() 
            elif choice == 7:
                self.get_all_from_cart()
            elif choice == 8:
                self.place_order()
            elif choice == 9:
                self.get_orders_by_customer()
            elif choice == 10:
                print("Thank you. Have a great day!")
                break
            else:
                print("Invalid choice. Please try again.")

    
    def create_product(self):
        product_id = int(input("Enter product ID: "))
        name = input("Enter product name: ")
        price = input("Enter product price: ")
        description = input("Provide product description: ")
        stockQuantity = input("Enter product stock quantity: ")

        products = Products(product_id,name,price,description,stockQuantity)
        result = self.implementation.createProduct(products) 


    def create_customer(self):
        customer_id = int(input("Enter customer ID: "))
        name = input("Enter customer name: ")
        email = input("Enter email: ")
        password = input("Enter password: ")

        customers = Customers(customer_id,name,email,password)
        result = self.implementation.createCustomer(customers)


    def delete_product(self):
        product_id = int(input("Enter product ID: "))

        result = self.implementation.deleteProduct(product_id)



    def delete_customer(self):
        customer_id = int(input("Enter customer ID: "))

        result = self.implementation.deleteCustomer(customer_id)


    def add_to_cart(self):

        customer_id = int(input("Enter customer ID: "))
        customers = self.implementation.get_customer_by_id(customer_id)

        product_id = int(input("Enter product ID: "))
        products = self.implementation.get_product_by_id(product_id)

        quantity = int(input("Enter quantity: "))

        result = self.implementation.addToCart(customers,products,quantity)



    def remove_from_cart(self):
        customer_id = int(input("Enter customer ID: "))
        customers = self.implementation.get_customer_by_id(customer_id)

        product_id = int(input("Enter product ID: "))
        products = self.implementation.get_product_by_id(product_id)

        result = self.implementation.removeFromCart(customers,products)


    
    def get_all_from_cart(self):
        customer_id = int(input("Enter customer ID: "))
        customers = self.implementation.get_customer_by_id(customer_id)


        items = self.implementation.getAllFromCart(customers)

        if items:
            print(f"Showing cart items for {customers.name}")
            for item in items:
                print(item)

        else:
            print("Failed to retrieve items.")



    def place_order(self):
        customer_id = int(input("Enter customer ID: "))
        shipping_address = input("Enter shipping address: ")
        items = []  # List of tuples (product, quantity)
        # Fetch the customer from the repository
        customer = self.implementation.get_customer_by_id(customer_id)

        while True:
            product_id = int(input("Enter product ID to order (0 to finish): "))
            if product_id == 0:
                break
            quantity = int(input("Enter quantity: "))
            product = self.implementation.get_product_by_id(product_id)
            if not product:
                print(f"Product with ID {product_id} not found.")
                continue
            
            if product.stockQuantity< quantity:
                print(f"Not enough stock for {product.name}. Available: {product.stockQuantity}")
                continue
            items.append((product, quantity))
        if not items:
            print("No products were selected for the order.")
            return 


    
    def get_orders_by_customer(self):
        customer_id = int(input("Enter customer ID to view orders: "))
        orders = self.implementation.getOrdersByCustomer(customer_id)
        if orders:
            print("Orders for Customer ID:", customer_id)
            for product, quantity in orders.items():
                print(f"- Product ID: {product.product_id}, Quantity: {quantity}")
        else:
            print("No orders found for this customer.")
        

def main():
    ecom_app = EcomApp()
    ecom_app.main()

if __name__ == "__main__":
    main()  
