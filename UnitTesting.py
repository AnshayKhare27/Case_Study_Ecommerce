import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from dao.implementation import OrderProcessorRepositoryImpl
from entity.customers import Customers
from entity.products import Products
from entity.cart import Cart
from entity.orders import Orders

class TestEcommerceSystem(unittest.TestCase):

    def setUp(self):
        # Set up database connection and any required data
        self.implementation = OrderProcessorRepositoryImpl()
        

        # Sample data for testing
        self.product = Products(101, "Watch", 200.0, "Luxury watch", 15)
        self.customer = Customers(102, "John Doe", "john@example.com", "1234567890")

        # Adding sample product to the database for testing
        self.implementation.create_product(self.product)

    
    def tearDown(self):
        # Clean up any test data from the database
        self.implementation.delete_product(self.product.get_product_id())


    def test_product_creation(self):
        """Test that a product is created successfully."""
        self.assertEqual(self.product.get_name(), "Watch")
        self.assertEqual(self.product.get_price(), 200.0)
        self.assertEqual(self.product.get_stockQuantity(), 15)

    def test_add_product_to_cart(self):
        """Test that a product is added to the cart successfully."""
        self.cart.add_to_cart(self.customer.get_customer_id(), self.product.get_product_id(), 2)
        cart_items = self.cart.get_all_from_cart(self.customer)
        self.assertIn(self.product.get_product_id(), [item.get_product_id() for item in cart_items])
        
    def test_place_order(self):
        """Test that an order is placed successfully."""
        self.cart.add_to_cart(self.customer.get_customer_id(), self.product.get_product_id(), 2)
        success = self.order_manager.place_order(self.customer, [(self.product, 2)], "123 Main St")
        self.assertTrue(success)

    def test_customer_not_found_exception(self):
        """Test exception is thrown when customer ID not found."""
        with self.assertRaises(Exception) as context:
            self.implementation.get_customer_by_id(999)  # Assuming 999 does not exist
        self.assertTrue('Customer not found' in str(context.exception))

    def test_product_not_found_exception(self):
        """Test exception is thrown when product ID not found."""
        with self.assertRaises(Exception) as context:
            self.implementation.get_product_by_id(999)  # Assuming 999 does not exist
        self.assertTrue('Product not found' in str(context.exception))



if __name__ == '__main__':
    unittest.main()