""" เกี่ยวกับจองรถ """
from flask import Blueprint
from .utils.database import execute_sql, execute_sql_one

bp = Blueprint('booking', __name__)

@bp.route("/branches", methods=["GET"])
def branches() :
    """ branch ทั้งหมด """
    results = execute_sql("SELECT branch_id, name, manager_employee_id FROM branches")
    return {"branches" : [{
        "branch_id" : x[0],
        "branch_name" : x[1]
    } for x in results]}

@bp.route("/reservation/<reservation_id>/summary", methods=["GET"])
def reservation(reservation_id=None) :
    """ ดึงข้อมูลการจองตาม reservation_id ที่ระบุแบบสรุป """
    result = execute_sql_one("""
SELECT
 reservation_id AS "reservation_id",

 customer.first_name AS "customer_first_name",
 customer.last_name AS "customer_last_name",

 car.license_plate AS "car_plate",
 model.name AS "car_model",
 manu.name AS "car_manufacturer",

 start_datetime AS "start_date",
 end_datetime AS "end_date",
 status
FROM reservations
JOIN customers customer USING (customer_id)
JOIN cars car USING (car_id)
JOIN car_models model ON (car.car_model_id = model.model_id)
JOIN car_manufacturers manu USING (manu_id)

WHERE reservation_id = %s
;""", reservation_id)
    if not result :
        return {"error" : "Reservation not found"}, 404
    
    return {
        "reservation_id" : result[0],
        "customer" : {
            "first_name" : result[1],
            "last_name" : result[2]
        },
        "car" : {
            "plate" : result[3],
            "model" : result[4],
            "manufacturer" : result[5]
        },
        "start_date" : result[6],
        "end_date" : result[7],
        "status" : result[8]
    }
