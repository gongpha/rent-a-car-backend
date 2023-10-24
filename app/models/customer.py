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
    def get_by_email(email) :
        cust = execute_sql_one(
            "SELECT * FROM customers WHERE c_email = %s"
            , email
        )
        if not cust :
            return None
        
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
    
    @staticmethod
    def update(cust_id, first_name, last_name, email, phone, driving_license) :
        """ update a customer """
        commit_sql(
            "UPDATE customers SET c_first_name = %s, c_last_name = %s, c_email = %s, c_phone_number = %s, driving_license_no = %s WHERE id = %s",
            (first_name, last_name, email, phone, driving_license, cust_id)
        )

    @staticmethod
    def delete(cust_id) :
        """ delete a customer """
        commit_sql(
            "DELETE FROM customers WHERE id = %s",
            cust_id
        )

    @staticmethod
    def get_all() :
        """ get all customers """
        custs = execute_sql_one("SELECT * FROM customers")
        if not custs :
            return None # bro
        
        custs = [Customer(
            id_=cust[0],
            first_name=cust[1],
            last_name=cust[2],
            email=cust[3],
            phone=cust[4],
            driving_license=cust[5]
        ) for cust in custs]
        return custs
    
    @staticmethod
    def get_all_by_name(name) :
        """ get all customers by name """
        custs = execute_sql_one("SELECT * FROM customers WHERE c_first_name = %s", name)
        if not custs :
            return None # bro
        
        custs = [Customer(
            id_=cust[0],
            first_name=cust[1],
            last_name=cust[2],
            email=cust[3],
            phone=cust[4],
            driving_license=cust[5]
        ) for cust in custs]
        return custs
    
    @staticmethod
    def get_all_by_email(email) :
        """ get all customers by email """
        custs = execute_sql_one("SELECT * FROM customers WHERE c_email = %s", email)
        if not custs :
            return None # bro
        
        custs = [Customer(
            id_=cust[0],
            first_name=cust[1],
            last_name=cust[2],
            email=cust[3],
            phone=cust[4],
            driving_license=cust[5]
        ) for cust in custs]
        return custs
    
    @staticmethod
    def get_all_by_phone(phone) :
        """ get all customers by phone """
        custs = execute_sql_one("SELECT * FROM customers WHERE c_phone_number = %s", phone)
        if not custs :
            return None # bro
        
        custs = [Customer(
            id_=cust[0],
            first_name=cust[1],
            last_name=cust[2],
            email=cust[3],
            phone=cust[4],
            driving_license=cust[5]
        ) for cust in custs]
        return custs
    
    @staticmethod
    def get_all_by_driving_license(driving_license) :
        """ get all customers by driving license """
        custs = execute_sql_one("SELECT * FROM customers WHERE driving_license_no = %s", driving_license)
        if not custs :
            return None # bro
        
        custs = [Customer(
            id_=cust[0],
            first_name=cust[1],
            last_name=cust[2],
            email=cust[3],
            phone=cust[4],
            driving_license=cust[5]
        ) for cust in custs]
        return custs
    
    @staticmethod
    def get_all_by_name_and_email(name, email) :
        """ get all customers by name and email """
        custs = execute_sql_one("SELECT * FROM customers WHERE c_first_name = %s AND c_email = %s", (name, email))
        if not custs :
            return None # bro
        
        custs = [Customer(
            id_=cust[0],
            first_name=cust[1],
            last_name=cust[2],
            email=cust[3],
            phone=cust[4],
            driving_license=cust[5]
        ) for cust in custs]
        return custs
    
    @staticmethod
    def get_all_by_name_and_phone(name, phone) :
        """ get all customers by name and phone """
        custs = execute_sql_one("SELECT * FROM customers WHERE c_first_name = %s AND c_phone_number = %s", (name, phone))
        if not custs :
            return None # bro
        
        custs = [Customer(
            id_=cust[0],
            first_name=cust[1],
            last_name=cust[2],
            email=cust[3],
            phone=cust[4],
            driving_license=cust[5]
        ) for cust in custs]
        return custs
    
    @staticmethod
    def get_all_by_name_and_driving_license(name, driving_license) :
        """ get all customers by name and driving license """
        custs = execute_sql_one("SELECT * FROM customers WHERE c_first_name = %s AND driving_license_no = %s", (name, driving_license))
        if not custs :
            return None # bro
        
        custs = [Customer(
            id_=cust[0],
            first_name=cust[1],
            last_name=cust[2],
            email=cust[3],
            phone=cust[4],
            driving_license=cust[5]
        ) for cust in custs]
        return custs
    
    @staticmethod
    def get_all_by_email_and_phone(email, phone) :
        """ get all customers by email and phone """
        custs = execute_sql_one("SELECT * FROM customers WHERE c_email = %s AND c_phone_number = %s", (email, phone))
        if not custs :
            return None # bro
        
        custs = [Customer(
            id_=cust[0],
            first_name=cust[1],
            last_name=cust[2],
            email=cust[3],
            phone=cust[4],
            driving_license=cust[5]
        ) for cust in custs]
        return custs
    
    @staticmethod
    def get_all_by_email_and_driving_license(email, driving_license) :
        """ get all customers by email and driving license """
        custs = execute_sql_one("SELECT * FROM customers WHERE c_email = %s AND driving_license_no = %s", (email, driving_license))
        if not custs :
            return None # bro
        
        custs = [Customer(
            id_=cust[0],
            first_name=cust[1],
            last_name=cust[2],
            email=cust[3],
            phone=cust[4],
            driving_license=cust[5]
        ) for cust in custs]
        return custs
    
    @staticmethod
    def get_all_by_phone_and_driving_license(phone, driving_license) :
        """ get all customers by phone and driving license """
        custs = execute_sql_one("SELECT * FROM customers WHERE c_phone_number = %s AND driving_license_no = %s", (phone, driving_license))
        if not custs :
            return None # bro
        
        custs = [Customer(
            id_=cust[0],
            first_name=cust[1],
            last_name=cust[2],
            email=cust[3],
            phone=cust[4],
            driving_license=cust[5]
        ) for cust in custs]

        return custs