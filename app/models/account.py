""" account model """
from .customer import Customer
from app.utils.database import execute_sql_one, commit_sql

class Account() :
    """ customer model """
    def __init__(self, id_, customer, display_name, pfp_url=None, dob=None) :
        self.id = id_
        self.customer = customer
        self.dob = dob
        self.display_name = display_name
        self.pfp_url = pfp_url

    @staticmethod
    def get(acc_id) :
        acc = execute_sql_one(
            "SELECT * FROM customers JOIN web_accounts USING (customer_id) WHERE account_id = %s", acc_id
        )
        if not acc :
            return None # bro
        
        return Account(
            id_=acc[6],
            dob=acc[7],
            display_name=acc[8],
            pfp_url=acc[9],
            customer=Customer(
                id_=acc[0],
                first_name=acc[1],
                last_name=acc[2],
                email=acc[3],
                phone=acc[4],
                driving_license=acc[5]
            )
        )
    
    @staticmethod
    def get_by_email(email) :
        acc = execute_sql_one(
            "SELECT * FROM customers JOIN web_accounts USING (customer_id) WHERE c_email = %s"
            , email
        )
        if not acc :
            return None # bro
        
        return Account(
            id_=acc[6],
            dob=acc[7],
            display_name=acc[8],
            pfp_url=acc[9],
            customer=Customer(
                id_=acc[0],
                first_name=acc[1],
                last_name=acc[2],
                email=acc[3],
                phone=acc[4],
                driving_license=acc[5]
            )
        )
    
    @staticmethod
    def create_with_customer(first_name, last_name, email, phone, driving_license, pfp_url=None) :
        """ create a new account + customer """
        cust = Customer.create(first_name, last_name, email, phone, driving_license)

        commit_sql(
            "INSERT INTO web_accounts"
            "(customer_id, pfp_url, display_name)"
            "VALUES (%s, %s, %s);",
            cust.id, pfp_url, first_name + " " + last_name
        )
        acc = execute_sql_one("SELECT * FROM web_accounts WHERE account_id = LAST_INSERT_ID()")
        return Account(
            id_=acc[0],
            customer=cust,
            dob=acc[1],
            display_name=acc[2],
            pfp_url=acc[3]
        )