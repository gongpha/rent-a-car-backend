""" transaction model """
from app.utils.database import execute_sql_one, commit_sql, execute_sql

class TotalPrice() :
    def __init__(self,
        reservation_id,
        discount_code,
        cost
    ) :
        self.reservation_id = reservation_id
        self.discount_code = discount_code
        self.cost = cost

    @staticmethod
    def get_total_price(reservation_id) :
        total_price = execute_sql_one(
            "SELECT * FROM total_price WHERE reservation_id = %s", reservation_id
        )
        if not total_price :
            return None # bro
        
        total_price = TotalPrice(
            reservation_id=total_price[0],
            discount_code=total_price[1],
            cost=total_price[2]
        )
        return total_price
    
    @staticmethod
    def get_all() :
        total_prices = execute_sql_one("SELECT * FROM total_price")
        if not total_prices :
            return None # bro
        
        total_prices = [TotalPrice(
            reservation_id=total_price[0],
            discount_code=total_price[1],
            cost=total_price[2]
        ) for total_price in total_prices]
        return total_prices
    

    @staticmethod
    def create(reservation_id, discount_code, cost) :
        commit_sql(
            "INSERT INTO total_price"
            "(reservation_id, discount_code, cost)"
            "VALUES (%s, %s, %s);",
            reservation_id, discount_code, cost
        )

class TransactionBill() :
    def __init__(self,
        customer,
        transaction,
        transaction_bill,
        total_price
    ) -> None:
        self.customer = customer
        self.transaction = transaction
        self.transaction_bill = transaction_bill
        self.total_price = total_price

    @staticmethod
    def get_all() :
        transaction_bills = execute_sql_one("SELECT * FROM transaction_bill")
        if not transaction_bills :
            return None # bro
        
        transaction_bills = [TransactionBill(
            customer=transaction_bill[0],
            transaction=transaction_bill[1],
            transaction_bill=transaction_bill[2],
            total_price=transaction_bill[3]
        ) for transaction_bill in transaction_bills]
        return transaction_bills
    
    @staticmethod
    def get_by_transaction_bill(transaction_bill) :
        transaction_bill = execute_sql_one(
            "SELECT * FROM transaction_bill WHERE transaction_bill = %s", transaction_bill
        )
        if not transaction_bill :
            return None # bro
        
        transaction_bill = TransactionBill(
            customer=transaction_bill[0],
            transaction=transaction_bill[1],
            transaction_bill=transaction_bill[2],
            total_price=transaction_bill[3]
        )
        return transaction_bill
    
    @staticmethod
    def create(customer, transaction, transaction_bill, total_price) :
        commit_sql(
            "INSERT INTO transaction_bill"
            "(customer, transaction, transaction_bill, total_price)"
            "VALUES (%s, %s, %s, %s);",
            customer, transaction, transaction_bill, total_price
        )

    

class Transaction() :
    def __init__(self,
        transaction,
        reservation,
        timestamp,
        method
    ) :
        self.transaction = transaction
        self.reservation = reservation
        self.timestamp = timestamp
        self.method = method
        
    @staticmethod
    def get_all() :
        transactions = execute_sql_one("SELECT * FROM transactions")
        if not transactions :
            return None # bro
        
        transactions = [Transaction(
            transaction=transaction[0],
            reservation=transaction[1],
            timestamp=transaction[2],
            method=transaction[3]
        ) for transaction in transactions]
        return transactions
    
    @staticmethod
    def get_by_id(id) :
        transaction = execute_sql_one(
            "SELECT * FROM transactions WHERE transaction = %s", id
        )
        if not transaction :
            return None
        
        transaction = Transaction(
            transaction=transaction[0],
            reservation=transaction[1],
            timestamp=transaction[2],
            method=transaction[3]
        )
        return transaction
    
    @staticmethod
    def create(reservation, timestamp, method) :
        commit_sql(
            "INSERT INTO transactions"
            "(reservation, timestamp, method)"
            "VALUES (%s, %s, %s);",
            reservation, timestamp, method
        )
        transaction = execute_sql_one("SELECT * FROM transactions WHERE transaction = LAST_INSERT_ID()")
        return Transaction(
            transaction=transaction[0],
            reservation=transaction[1],
            timestamp=transaction[2],
            method=transaction[3]
        )
    
    @staticmethod
    def delete(transaction) :
        commit_sql(
            "DELETE FROM transactions WHERE transaction = %s",
            transaction
        )

class PaymentMethod() :
    def __init__(self,
        method,
        name,
        card_number,
        expiration_date,
        cvv
    ) :
        self.method = method
        self.name = name
        self.card_number = card_number
        self.expiration_date = expiration_date
        self.cvv = cvv

    @staticmethod
    def get_all() :
        payment_methods = execute_sql_one("SELECT * FROM payment_methods")
        if not payment_methods :
            return None # bro
        
        payment_methods = [PaymentMethod(
            method=payment_method[0],
            name=payment_method[1],
            card_number=payment_method[2],
            expiration_date=payment_method[3],
            cvv=payment_method[4]
        ) for payment_method in payment_methods]
        return payment_methods
    
    @staticmethod
    def get_by_id(id) :
        payment_method = execute_sql_one(
            "SELECT * FROM payment_methods WHERE method = %s", id
        )
        if not payment_method :
            return None
        
        payment_method = PaymentMethod(
            method=payment_method[0],
            name=payment_method[1],
            card_number=payment_method[2],
            expiration_date=payment_method[3],
            cvv=payment_method[4]
        )
        return payment_method
    
    @staticmethod
    def create(name, card_number, expiration_date, cvv) :
        commit_sql(
            "INSERT INTO payment_methods"
            "(name, card_number, expiration_date, cvv)"
            "VALUES (%s, %s, %s, %s);",
            name, card_number, expiration_date, cvv
        )
        payment_method = execute_sql_one("SELECT * FROM payment_methods WHERE method = LAST_INSERT_ID()")
        return PaymentMethod(
            method=payment_method[0],
            name=payment_method[1],
            card_number=payment_method[2],
            expiration_date=payment_method[3],
            cvv=payment_method[4]
        )
    
    @staticmethod
    def delete(method) :
        commit_sql(
            "DELETE FROM payment_methods WHERE method = %s",
            method
        )

class DiscountCode() :
    def __init__(self,
        id,
        code,
        discount
    ) :
        self.id = id
        self.code = code
        self.discount = discount

    @staticmethod
    def get_all() :
        discount_codes = execute_sql_one("SELECT * FROM discount_codes")
        if not discount_codes :
            return None # bro
        
        discount_codes = [DiscountCode(
            id=discount_code[0],
            code=discount_code[1],
            discount=float(discount_code[2])
        ) for discount_code in discount_codes]
        return discount_codes
    
    @staticmethod
    def get_by_code(code) :
        discount_code = execute_sql_one(
            "SELECT * FROM discount_codes WHERE code = %s", code
        )
        if not discount_code :
            return None
        
        discount_code = DiscountCode(
            id=discount_code[0],
            code=discount_code[1],
            discount=float(discount_code[2])
        )
        return discount_code
    
    @staticmethod
    def create(code, discount) :
        commit_sql(
            "INSERT INTO discount_codes"
            "(code, discount)"
            "VALUES (%s, %s);",
            code, discount
        )
        discount_code = execute_sql_one("SELECT * FROM discount_codes WHERE code = LAST_INSERT_ID()")
        return DiscountCode(
            id=discount_code[0],
            code=discount_code[1],
            discount=float(discount_code[2])
        )
    
    @staticmethod
    def delete(code) :
        commit_sql(
            "DELETE FROM discount_codes WHERE code = %s",
            code
        )

