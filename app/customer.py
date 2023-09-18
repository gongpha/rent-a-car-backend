""" เกี่ยวกับข้อมูลลูกค้า """
from flask import Blueprint
from .utils.database import execute_sql, execute_sql_one

bp = Blueprint('customer', __name__)

@bp.route("/customer/<customer_id>", methods=["GET"])
def customer_by_id(customer_id = None) :
    """ ดึงข้อมูลลูกค้าจาก ID """

    # ดึงข้อมูลลูกค้าตาม ID ที่ระบุ
    result = execute_sql_one("SELECT * FROM customers WHERE customer_id = %s", customer_id)
    if result == None : # หาไม่เจอ
        return {"error" : "Customer not found"}, 404
    
    # ดึงเบอร์มา
    results_phone = execute_sql("SELECT number, comment FROM phone_numbers WHERE customer_id = %s", customer_id)

    # หาเจอ
    return {
        "customer_id" : result[0],
        "first_name" : result[1],
        "last_name" : result[2],
        "email" : result[3],

        "phone_numbers" : [{
            "number" : x[0],
            "comment" : x[1]
        } for x in results_phone]
    }
