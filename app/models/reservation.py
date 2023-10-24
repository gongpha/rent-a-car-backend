""" reservation model """
from app.utils.database import execute_sql_one, commit_sql, execute_sql, commit_sqls
from .payment import PaymentInfo
from .customer import Customer

class Reservation() :
    """ reservation model """
    def __init__(self, id_, customer_id, car_id, start_date, end_date, status) :
        self.id = id_
        self.customer_id = customer_id
        self.car_id = car_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    @staticmethod
    def get(reservation_id) :
        """ get a reservation by id """
        reservation = execute_sql_one(
            "SELECT * FROM reservations WHERE reservation_id = %s", reservation_id
        )
        if not reservation :
            return None # bro
        
        reservation = Reservation(
            id_=reservation[0],
            customer_id=reservation[1],
            car_id=reservation[2],
            start_date=reservation[3],
            end_date=reservation[4],
            status=reservation[5]
        )
        return reservation
    
    @staticmethod
    def get_all() :
        """ get all reservation """
        reservations = execute_sql_one("SELECT * FROM reservations")
        if not reservations :
            return None # bro
        
        reservations = [Reservation(
            id_=reservation[0],
            customer_id=reservation[1],
            car_id=reservation[2],
            start_date=reservation[3],
            end_date=reservation[4],
            status=reservation[5]
        ) for reservation in reservations]
        return reservations
    
    @staticmethod
    def create(
        cust,
        rrr, # input
        summary, # output
        storeMyPaymentInfo, # yes ?

        paymentInfo : PaymentInfo
    ) :
        if storeMyPaymentInfo :
            exist_payment = execute_sql_one(
                "SELECT * FROM payment_info"
                " WHERE customer_id = %s",
                cust.id
            )

            if exist_payment :
                # replace
                sql3 = (
                    "UPDATE payment_info SET"
                    " cardholder = %s,"
                    " card_number = %s,"
                    " expiry_month = %s,"
                    " expiry_year = %s,"
                    " cvc = %s,"
                    " bank = %s,"
                    " country = %s"
                    " WHERE customer_id = %s",
                    (
                        paymentInfo.cardholder,
                        paymentInfo.cardNumber,
                        paymentInfo.cardExpiryMonth,
                        paymentInfo.cardExpiryYear,
                        paymentInfo.cardCvc,
                        paymentInfo.cardFromBank,
                        paymentInfo.cardCountry,
                        cust.id
                    )
                )
            else :
                # create
                sql3 = (
                    "INSERT INTO payment_info"
                    " (customer_id, cardholder, card_number, expiry_month, expiry_year, cvc, bank, country)"
                    " VALUES"
                    " (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        cust.id,
                        paymentInfo.cardholder,
                        paymentInfo.cardNumber,
                        paymentInfo.cardExpiryMonth,
                        paymentInfo.cardExpiryYear,
                        paymentInfo.cardCvc,
                        paymentInfo.cardFromBank,
                        paymentInfo.cardCountry
                    )
                )
        else :
            sql3 = ("", [])

        # pretend that we paid

        # create reservation
        sql1 = (
            "INSERT INTO reservations"
            " (customer_id, car_id, insurance_id,"
            " start_datetime, end_datetime, driver_employee_id,"
            " pickup_location, return_location, status,"
            " price, created) VALUES"
            " (%s, %s, %s,"
            " %s, %s, %s,"
            " %s, %s, %s,"
            " %s, NOW());",
            (
                cust.id,
                rrr.get("carId"),
                rrr.get("insuranceId"),
                summary[1]["start_date"],
                summary[1]["end_date"],
                None,
                rrr.get("branchStartID"),
                rrr.get("branchEndID"),
                "CAR",
                summary[0]["total"],
            )
        )

        sql2 = (
            "UPDATE cars SET car_status = 'reserve' WHERE car_id = %s"
            , rrr.get("carId")
        )

        commit_sqls(
            [x[0] for x in [sql1, sql2, sql3]],
            [x[1] for x in [sql1, sql2, sql3]]
        )

        return {
            "return" : "OK",
            "reservation_id" : execute_sql_one("SELECT LAST_INSERT_ID()")[0],

            "customer" : {
                "first_name" : cust.first_name,
                "last_name" : cust.last_name,
                "email" : cust.email,
                "phone" : cust.phone
            },
        }, 200

    @staticmethod
    def update(reservation_id, customer_id, car_id, start_date, end_date, status) :
        """ update a reservation """
        commit_sql(
            "UPDATE reservations SET customer_id = %s, car_id = %s, start_date = %s, end_date = %s, status = %s WHERE reservation_id = %s",
            (customer_id, car_id, start_date, end_date, status, reservation_id)
        )

    @staticmethod
    def delete(reservation_id) :
        """ delete a reservation """
        commit_sql(
            "DELETE FROM reservations WHERE reservation_id = %s",
            reservation_id
        )

    @staticmethod
    def get_by_customer_id(customer_id) :
        """ get reservation by customer id """
        reservation = execute_sql_one(
            "SELECT * FROM reservations WHERE customer_id = %s", customer_id
        )
        if not reservation :
            return None # bro
        
        reservation = Reservation(
            id_=reservation[0],
            customer_id=reservation[1],
            car_id=reservation[2],
            start_date=reservation[3],
            end_date=reservation[4],
            status=reservation[5]
        )
        return reservation
    
    @staticmethod
    def get_by_car_id(car_id) :
        """ get reservation by car id """
        reservation = execute_sql_one(
            "SELECT * FROM reservations WHERE car_id = %s", car_id
        )
        if not reservation :
            return None # bro
        
        reservation = Reservation(
            id_=reservation[0],
            customer_id=reservation[1],
            car_id=reservation[2],
            start_date=reservation[3],
            end_date=reservation[4],
            status=reservation[5]
        )
        return reservation
    
    @staticmethod
    def get_by_status(status) :
        """ get reservation by status """
        reservation = execute_sql_one(
            "SELECT * FROM reservations WHERE status = %s", status
        )
        if not reservation :
            return None # bro
        
        reservation = Reservation(
            id_=reservation[0],
            customer_id=reservation[1],
            car_id=reservation[2],
            start_date=reservation[3],
            end_date=reservation[4],
            status=reservation[5]
        )
        return reservation
    
    @staticmethod
    def get_by_start_date(start_date) :
        """ get reservation by start date """
        reservation = execute_sql_one(
            "SELECT * FROM reservations WHERE start_date = %s", start_date
        )
        if not reservation :
            return None # bro
        
        reservation = Reservation(
            id_=reservation[0],
            customer_id=reservation[1],
            car_id=reservation[2],
            start_date=reservation[3],
            end_date=reservation[4],
            status=reservation[5]
        )
        return reservation
    
    @staticmethod
    def get_by_end_date(end_date) :
        """ get reservation by end date """
        reservation = execute_sql_one(
            "SELECT * FROM reservations WHERE end_date = %s", end_date
        )
        if not reservation :
            return None # bro
        
        reservation = Reservation(
            id_=reservation[0],
            customer_id=reservation[1],
            car_id=reservation[2],
            start_date=reservation[3],
            end_date=reservation[4],
            status=reservation[5]
        )
        return reservation
    
    @staticmethod
    def get_by_customer_id_and_car_id(customer_id, car_id) :
        """ get reservation by customer id and car id """
        reservation = execute_sql_one(
            "SELECT * FROM reservations WHERE customer_id = %s AND car_id = %s", (customer_id, car_id)
        )
        if not reservation :
            return None # bro
        
        reservation = Reservation(
            id_=reservation[0],
            customer_id=reservation[1],
            car_id=reservation[2],
            start_date=reservation[3],
            end_date=reservation[4],
            status=reservation[5]
        )
        return reservation