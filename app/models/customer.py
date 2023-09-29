""" customer model """
from app.utils.database import execute_sql_one, commit_sql

class Customer() :
    """ customer model """
    def __init__(self, id_, first_name, last_name, email, phone, driving_license) :
        self.id = id_
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.driving_license = driving_license

    @staticmethod
    def get(cust_id) :
        """ get a customer by id """
        cust = execute_sql_one(
            "SELECT * FROM customers WHERE id = %s", cust_id
        )
        if not cust :
            return None # bro
        
        cust = Customer(
            id_=cust[0],
            first_name=cust[1],
            last_name=cust[2],
            email=cust[3],
            phone=cust[4],
            driving_license=cust[5]
        )
        return cust
    
    @staticmethod
    def create(first_name, last_name, email, phone, driving_license) :
        """ create a new customer """
        commit_sql(
            "INSERT INTO customers"
            "(c_first_name, c_last_name, c_email, c_phone_number, driving_license_no)"
            "VALUES (%s, %s, %s, %s, %s);",
            first_name, last_name, email, phone, driving_license
        )
        cust = execute_sql_one("SELECT * FROM customers WHERE customer_id = LAST_INSERT_ID()")
        return Customer(
            id_=cust[0],
            first_name=cust[1],
            last_name=cust[2],
            email=cust[3],
            phone=cust[4],
            driving_license=cust[5]
        )