class Products:
    def __init__(self,product_id,name,price,description,stockQuantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.stockQuantity = stockQuantity

    #Getters
    def get_product_id(self):
        return self.product_id
    def get_name(self):
        return self.name
    def get_price(self):
        return self.price
    def get_description(self):
        return self.description
    def get_stockQuantity(self):
        return self.stockQuantity

    #Setters
    def set_product_id(self,product_id):
        self.product_id = product_id     
    def set_name(self,name):
        self.name = name
    def set_price(self,price):
        self.price = price
    def set_description(self,description):
        self.description = description
    def set_stockQuantity(self,stockQuantity):
        self.stockQuantity = stockQuantity
        