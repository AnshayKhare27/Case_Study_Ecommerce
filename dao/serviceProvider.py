import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple

from entity.customers import Customers
from entity.products import Products


class OrderProcessorRepository(ABC):

    @abstractmethod
    def createProduct(self, products : Products):
        pass 

    @abstractmethod
    def createCustomer(self, customers : Customers):
        pass 

    @abstractmethod
    def deleteProduct(self, product_id : int):
        pass

    @abstractmethod
    def deleteCustomer(self, customer_id : int):
        pass

    @abstractmethod
    def addToCart(self , customers : Customers, products : Products, quantity : int):
        pass

    @abstractmethod
    def removeFromCart(self, customers : Customers, products : Products):
        pass

    @abstractmethod
    def getAllFromCart(self, customers : Customers):
        pass

    @abstractmethod
    def placeOrder(self, customers : Customers, items: List[Tuple[Products, int]], shippingAddress: str):
        pass

    @abstractmethod
    def getOrdersByCustomer(self, customer_id : int):
        pass                     
        
