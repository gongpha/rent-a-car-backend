""" เกี่ยวกับจองรถ """
from flask import Blueprint
from .utils.database import execute_sql, execute_sql_one, commit_sqls
from flask import request
from datetime import datetime
from .models.customer import Customer
from .models.account import Account
import re

from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity, get_jwt
)

from .auth import user_required


bp = Blueprint('booking', __name__)

@bp.route("/branches", methods=["GET"])
def branches() :
    """ branch ทั้งหมด """
    results = execute_sql("SELECT branch_id, name, location FROM branches")
    return {"branches" : [{
        "branch_id" : x[0],
        "branch_name" : x[1],
        "location" : x[2]
    } for x in results]}

@bp.route("/branch/<branch_id>", methods=["GET"])
def branch(branch_id=0) :
    """ branch """
    x = execute_sql_one("SELECT branch_id, name, location FROM branches WHERE branch_id = %s", branch_id)
    return {
        "branch_id" : x[0],
        "branch_name" : x[1],
        "location" : x[2]
    }

@bp.route("/insurances", methods=["GET"])
def insurances() :
    """ ประกันรถทั้งหมด """
    results = execute_sql("SELECT * FROM insurance")
    return {"insurances" : [{
        "insurance_id" : x[0],
        "name" : x[1],
        "properties" : {
            "bodily_injury" : x[2] == 'Y',
            "vehicle_damage" : x[3] == 'Y',
            "property_damage" : x[4] == 'Y',
            "thief_fire" : x[5] == 'Y',
        },
        
        "description" : x[6],
        "cost_per_day" : x[7]
    } for x in results]}

@bp.route("/driver/available", methods=["GET"])
def driver_available() :
    """ คนขับที่ว่าง """
    r = execute_sql_one(
        "SELECT COUNT(*) FROM employees"
        " LEFT JOIN reservations ON (employee_id = driver_employee_id)"
        " WHERE job = \"DRIVER\" AND driver_employee_id IS NULL"
    )
    return {'available' : r != 0}

@bp.route("/insurance/<ins_id>", methods=["GET"])
def insurance(ins_id=0) :
    """ ประกันรถทั้งหมด """
    x = execute_sql_one("SELECT * FROM insurance WHERE insurance_id = %s", ins_id)
    return {
        "insurance_id" : x[0],
        "name" : x[1],
        "properties" : {
            "bodily_injury" : x[2] == 'Y',
            "vehicle_damage" : x[3] == 'Y',
            "property_damage" : x[4] == 'Y',
            "thief_fire" : x[5] == 'Y',
        },
        
        "description" : x[6],
        "cost_per_day" : x[7]
    }

@bp.route("/reserve/summary", methods=["GET"])
def reserve_summary() :
    """ ดึงข้อมูลการจองทั้งหมดแบบสรุป """
    
    return craft_summary(False)[0], 200

def craft_summary(use_form : bool) -> dict :
    if use_form :
        rrr = request.get_json()
    else :
        rrr = request.args

    branchStartID = rrr.get("branchStartID")
    branchEndID = rrr.get("branchEndID")
    startDate = rrr.get("startDate")
    endDate = rrr.get("endDate")
    carId = rrr.get("carId")

    insuranceId = rrr.get("insuranceId")
    hireDriver = rrr.get("hireDriver")

    if (
        branchStartID == None or
        branchEndID == None or
        startDate == None or
        endDate == None or
        carId == None
    ) : return {
        "error" : "Missing parameter"
    }, 400

    realStartDate = datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=None)
    realEndDate = datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=None)
    length = (realEndDate - realStartDate).days + 1

    price_per_day = execute_sql_one(
        "SELECT price_per_day FROM cars"
        " JOIN car_models USING (model_id)"
        " WHERE car_id = %s", carId
    )[0]

    if insuranceId == None :
        cost_per_day = 0
    else :
        cost_per_day = execute_sql_one(
            "SELECT cost_per_day FROM insurance"
            " WHERE insurance_id = %s", insuranceId
        )[0]

    if hireDriver == None :
        hire_driver_cost_per_day = 0
    else :
        hire_driver_cost_per_day = 1000

    per_day = price_per_day + cost_per_day + hire_driver_cost_per_day

    lll = [
        {
            "name" : "ราคาเช่ารถต่อวัน",
            "value" : price_per_day
        },
        {
            "name" : "รวมต่อวัน",
            "value" : per_day
        },
    ]

    if insuranceId != None :
        lll.insert(1,
            {
                "name" : "ค่าประกันต่อวัน",
                "value" : cost_per_day
            }
        )

    if hireDriver != None :
        lll.insert(1,
            {
                "name" : "ค่าคนขับต่อวัน",
                "value" : hire_driver_cost_per_day
            }
        )

    return [{
        "summary" : {
            "length" : length
        },
        "costs" : lll,
        "total" : per_day * length
    }, {
        "start_date" : realStartDate,
        "end_date" : realEndDate,
    }]

def check_date_overlap(start1, end1, start2, end2) -> bool :
    return start1 <= end2 and end1 >= start2

@bp.route("/reserve", methods=["POST"])
def reserve() :
    """ จองรถ """
    rrr = request.get_json()

    # payment ?
    cardholder = rrr.get("cardholder")
    cardNumber = rrr.get("cardNumber")
    cardExpiryMonth = rrr.get("cardExpiryMonth")
    cardExpiryYear = rrr.get("cardExpiryYear")
    cardCvc = rrr.get("cardCvc")
    cardFromBank = rrr.get("cardFromBank")
    cardCountry = rrr.get("cardCountry")
    
    if (
        cardholder == None or
        cardNumber == None or
        cardExpiryMonth == None or
        cardExpiryYear == None or
        cardCvc == None or
        cardFromBank == None or
        cardCountry == None
    ) :
        return {"error" : "Missing payment information"}, 400
    
    cardNumber = cardNumber.replace(" ", "")
    storeMyPaymentInfo = rrr.get("storeMyPaymentInfo")

    summary = craft_summary(True)
    if summary is tuple :
        return summary[0], summary[1]
    # check collision

    

    result = execute_sql_one(
        "SELECT reservation_id, start_datetime, end_datetime FROM reservations"
        " WHERE car_id = %s AND `status` = 'CAR'",
        rrr.get("carId")
    )
    if result :
        t_start = result[1]
        t_end = result[2]

        if check_date_overlap(
            summary[1]["start_date"],
            summary[1]["end_date"],
            t_start,
            t_end
        ) :
            return {"error" : "Car is not available", "reason" : "overlap"}, 400

    # pull account data 
    acc_id = rrr.get("accId")
    if acc_id is None :
        # anonymous ?

        if (
            rrr.get("firstName") == None or
            rrr.get("lastName") == None or
            rrr.get("email") == None or
            rrr.get("phone") == None
        ) :
            return {"error" : "Missing personal information"}, 400
        
        v_email = re.search(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", rrr.get("email"))
        v_phone = re.search(r"^[0-9]{10}$", rrr.get("phone"))

        if not v_email :
            return {"error" : "Invalid email"}, 400
        
        if not v_phone :
            return {"error" : "Invalid phone number"}, 400
        
        # existing customer ?
        cust = Customer.get_by_email(rrr.get("email"))

        if cust is None :
            # create new customer
            cust = Customer.create(
                rrr.get("firstName"),
                rrr.get("lastName"),
                rrr.get("email"),
                rrr.get("phone"),
                None
            )
    else :
        acc = Account.get(acc_id)
        if acc is None :
            return {"error" : "Account not found"}, 404
        cust = acc.customer
    
    # hireDriver = int(rrr.get("hireDriver"))
    # if hireDriver :
    #     r = execute_sql_one(
    #         "SELECT employee_id FROM employees"
    #         " LEFT JOIN reservations ON (employee_id = driver_employee_id)"
    #         " WHERE job = \"DRIVER\" AND driver_employee_id IS NULL"
    #     )
    #     if r is None :
    #         return {"error" : "No driver available"}, 400
        
    # else :
    #     r = (None,)

    # payment
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
                    cardholder,
                    cardNumber,
                    cardExpiryMonth,
                    cardExpiryYear,
                    cardCvc,
                    cardFromBank,
                    cardCountry,
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
                    cardholder,
                    cardNumber,
                    cardExpiryMonth,
                    cardExpiryYear,
                    cardCvc,
                    cardFromBank,
                    cardCountry
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
    
@bp.route("/reservations", methods=["GET"])
@user_required()
def reservations() :
    """ ดึงข้อมูลการจองทั้งหมด """
    email = get_jwt_identity()
    results = execute_sql("""
SELECT
    reservation_id AS "reservation_id",
    start_datetime AS "start_date",
    end_datetime AS "end_date",
    car.image_car AS "car_image",
    status,
    car.car_status,
    created
                          
    FROM reservations
    JOIN cars car USING (car_id)
    JOIN customers customer USING (customer_id)
    WHERE c_email = %s
    """, email)

    def status_get(x) :
        if x[4] == "CAR" :
            return x[5]
        elif x[4] == "CANCELED" :
            return "canceled"
        elif x[4] == "COMPLETED" :
            return "completed"

    return {"reservations" : [{
        "reservation_id" : x[0],
        "start_date" : x[1],
        "end_date" : x[2],
        "car_image" : x[3],
        "status" : status_get(x),
        "created_at" : x[6]
    } for x in results]}

@bp.route("/reservation/<resv_id>", methods=["GET"])
@jwt_required(optional=True)
def reservation_id(resv_id=0) :

    email_arg = request.args.get("email")
    if email_arg is None :
        email = get_jwt_identity()
    else :
        email = email_arg

    if email is None :
        return {"error" : "Missing email"}, 400
    
    result = execute_sql_one("""
SELECT
 reservation_id AS "reservation_id",

 customer.c_first_name AS "customer_first_name",
 customer.c_last_name AS "customer_last_name",
 customer.c_email AS "email",

 customer.c_phone_number AS "phone",
 model.model AS "car_model",
 model.brand AS "car_manufacturer",

 start_datetime AS "start_date",
 end_datetime AS "end_date",
 status,

 branch_start.branch_id AS "start_branch_id",                    
 branch_end.branch_id AS "end_branch_id",
                             
 branch_start.name AS "start_branch_name",
 branch_start.location AS "start_branch_location",
                             
 branch_end.name AS "end_branch_name",
 branch_end.location AS "end_branch_location",
 car.image_car AS "car_image",
 model.car_type AS "car_type",
 model.fuel_type AS "fuel_type",
 model.price_per_day AS "price_per_day",
 model.seats AS "seats",
 model.gear AS "gear",
 car.car_id AS "car_id"
 FROM reservations
 JOIN customers customer USING (customer_id)
 JOIN cars car USING (car_id)
 JOIN branches branch_start ON (reservations.pickup_location = branch_start.branch_id)
 JOIN branches branch_end ON (reservations.return_location = branch_end.branch_id)
 JOIN car_models model ON (car.model_id = model.model_id)

WHERE reservation_id = %s
;""", resv_id)
    
    if not result :
        return {"error" : "Reservation not found"}, 404

    if result[3] != email :
        return {"error" : "Reservation not found"}, 404

    return {
        "resv" : {
            "startBranch" : {
                "branchId" : result[10],
                "name" : result[12],
                "location" : result[13]
            },
            "endBranch" : {
                "branchId" : result[11],
                "name" : result[14],
                "location" : result[15]
            },
            "startDate" : result[7],
            "endDate" : result[8],
            "car" : {
                "brand" : result[6],
                "car_id" : result[22],
                "car_image" : result[16],
                "car_type" : result[17],
                "fuel_type" : result[18],
                "price_per_day" : result[19],
                "seats" : result[20],
                "gear" : result[21],
            },
            "insurance" : None,
            "costs" : [],
            "summary" : {
                "length" : 0
            },
            "total" : 0
        },
        "cust" : {
            "firstName" : result[1],
            "lastName" : result[2],
            "email" : result[3],
            "phone" : result[4]
        }
    }