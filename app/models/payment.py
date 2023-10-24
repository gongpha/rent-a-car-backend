from app.utils.database import execute_sql_one, commit_sql, execute_sql

class PaymentInfo() :
    """ payment info model"""
    def __init__(self,
        cardholder,
        cardNumber,
        cardExpiryMonth,
        cardExpiryYear,
        cardCvc,
        cardFromBank,
        cardCountry,
    ) :
        self.cardholder = cardholder
        self.cardNumber = cardNumber
        self.cardExpiryMonth = cardExpiryMonth
        self.cardExpiryYear = cardExpiryYear
        self.cardCvc = cardCvc
        self.cardFromBank = cardFromBank
        self.cardCountry = cardCountry

    @staticmethod
    def get_by_customer_id(customer_id) :
        payment_info = execute_sql_one(
            "SELECT * FROM payment_info WHERE customer_id = %s", customer_id
        )
        if not payment_info :
            return None
        
        payment_info = PaymentInfo(
            cardholder=payment_info[1],
            cardNumber=payment_info[2],
            cardExpiryMonth=payment_info[3],
            cardExpiryYear=payment_info[4],
            cardCvc=payment_info[5],
            cardFromBank=payment_info[6],
            cardCountry=payment_info[7]
        )
        return payment_info
    
    @staticmethod
    def create(
        customer_id,
        cardholder,
        cardNumber,
        cardExpiryMonth,
        cardExpiryYear,
        cardCvc,
        cardFromBank,
        cardCountry,
    ) :
        commit_sql(
            "INSERT INTO payment_info VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            customer_id,
            cardholder,
            cardNumber,
            cardExpiryMonth,
            cardExpiryYear,
            cardCvc,
            cardFromBank,
            cardCountry
        )