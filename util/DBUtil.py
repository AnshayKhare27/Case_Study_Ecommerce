import pyodbc

class DBConnection:
    
    @staticmethod
    def getConnection():
        try:
            conn = pyodbc.connect('Driver={SQL Server};'
                                  'Server=MSI\SQLEXPRESS;'
                                  'Database=EcomCS;'
                                  'Trusted_Connection=yes;')
            return conn

        except:
            print("Connection failed")