""" _ """
from flask import Blueprint
from .utils.database import execute_sql, execute_sql_one, commit_sql, commit_sqls
from .auth import admin_required, root_required, manager_required

import requests
import os
import json

from flask import redirect, request, current_app, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt

bp = Blueprint('reservations', __name__)

@bp.route("/admin/reservations/<branch_id>", methods=["GET"])
@admin_required()
def admin_rsvs(branch_id=0) :
    """ _ """

    params = []
    if get_jwt()["role"] != "ROOT" :
        sql = ("SELECT reservation_id, c_first_name, c_last_name,"
        " image_car AS car_image, license_plate AS car_plate,"
        " brand AS model_brand, model AS model_model, year AS model_year,"
        " start_datetime AS start, end_datetime AS end"
        " FROM reservations"
        " JOIN customers USING (customer_id)"
        " JOIN cars USING (car_id)"
        " JOIN car_models USING (model_id)"
        " WHERE"
        " branch_id = ("
        " SELECT branch_id FROM employees WHERE employee_id = ("
        " SELECT employee_id FROM web_accounts_emp WHERE username = %s"
        " )"
        " )"
        " ORDER BY start_datetime ASC")
        params.append(get_jwt_identity())
    else :
        if branch_id == 0 :
            return []
        sql = ("SELECT reservation_id, c_first_name, c_last_name,"
        " image_car AS car_image, license_plate AS car_plate,"
        " brand AS model_brand, model AS model_model, year AS model_year,"
        " start_datetime AS start, end_datetime AS end"
        " FROM reservations"
        " JOIN customers USING (customer_id)"
        " JOIN cars USING (car_id)"
        " JOIN car_models USING (model_id)"
        " WHERE"
        " branch_id = %s"
        " ORDER BY start_datetime ASC")
        params.append(branch_id)

    results = execute_sql(sql, *params)

    return {
        "reservations": [{
            "id": x[0],
            "c_first_name" : x[1],
            "c_last_name" : x[2],
            "car_image": x[3],
            "car_plate": x[4],
            "model_brand": x[5],
            "model_model": x[6],
            "model_year": x[7],
            "start": x[8],
            "end": x[9]
        } for x in results]
    }

@bp.route("/admin/reservations/<branch_id>/today", methods=["GET"])
@admin_required()
def admin_rsv_today(branch_id=0) :
    """ _ """

    params = []
    if get_jwt()["role"] != "ROOT" :
        sql = ("SELECT reservation_id, c_first_name, c_last_name,"
        " image_car AS car_image, license_plate AS car_plate,"
        " brand AS model_brand, model AS model_model, year AS model_year,"
        " start_datetime AS start, end_datetime AS end"
        " FROM reservations"
        " JOIN customers USING (customer_id)"
        " JOIN cars USING (car_id)"
        " JOIN car_models USING (model_id)"
        " WHERE"
        " CURRENT_DATE() BETWEEN DATE(start_datetime) AND DATE(end_datetime)"
        " AND branch_id = ("
        " SELECT branch_id FROM employees WHERE employee_id = ("
        " SELECT employee_id FROM web_accounts_emp WHERE username = %s"
        " )"
        " )"
        " ORDER BY start_datetime ASC")
        params.append(get_jwt_identity())
    else :
        if int(branch_id) == 0 :
            return {'root' : True}
        sql = ("SELECT reservation_id, c_first_name, c_last_name,"
        " image_car AS car_image, license_plate AS car_plate,"
        " brand AS model_brand, model AS model_model, year AS model_year,"
        " start_datetime AS start, end_datetime AS end"
        " FROM reservations"
        " JOIN customers USING (customer_id)"
        " JOIN cars USING (car_id)"
        " JOIN car_models USING (model_id)"
        " WHERE"
        " CURRENT_DATE() BETWEEN DATE(start_datetime) AND DATE(end_datetime)"
        " AND branch_id = %s"
        " ORDER BY start_datetime ASC")
        params.append(branch_id)

    results = execute_sql(sql, *params)

    return {
        "reservations": [{
            "id": x[0],
            "c_first_name" : x[1],
            "c_last_name" : x[2],
            "car_image": x[3],
            "car_plate": x[4],
            "model_brand": x[5],
            "model_model": x[6],
            "model_year": x[7],
            "start": x[8],
            "end": x[9]
        } for x in results]
    }

@bp.route("/admin/reservation/<reservation_id>", methods=["GET"])
@admin_required()
def admin_rsv(reservation_id=0) :
    """ _ """

    params = []
    if get_jwt()["role"] != "ROOT" :
        sql = ("SELECT reservation_id, c_first_name, c_last_name,"
        " image_car AS car_image, license_plate AS car_plate,"
        " brand AS model_brand, model AS model_model, year AS model_year, model_id,"
        " mileage AS car_mileage,"
        " start_datetime AS start, end_datetime AS end"
        " , car_id, status, car_status, note"
        " FROM reservations"
        " JOIN customers USING (customer_id)"
        " JOIN cars USING (car_id)"
        " JOIN car_models USING (model_id)"
        " WHERE"
        " branch_id = ("
        " SELECT branch_id FROM employees WHERE employee_id = ("
        " SELECT employee_id FROM web_accounts_emp WHERE username = %s"
        " ) AND reservation_id = %s"
        " )"
        " ORDER BY start_datetime ASC")
        params.append(get_jwt_identity())
        params.append(reservation_id)
    else :
        sql = ("SELECT reservation_id, c_first_name, c_last_name,"
        " image_car AS car_image, license_plate AS car_plate,"
        " brand AS model_brand, model AS model_model, year AS model_year, model_id,"
        " mileage AS car_mileage,"
        " start_datetime AS start, end_datetime AS end"
        " , car_id, status, car_status, note"
        " FROM reservations"
        " JOIN customers USING (customer_id)"
        " JOIN cars USING (car_id)"
        " JOIN car_models USING (model_id)"
        " WHERE"
        " reservation_id = %s")
        params.append(reservation_id)

    x = execute_sql_one(sql, *params)

    status = x[13]
    car_status = x[14]
    actions = []

    # c = cancelable
    # i = inuseable
    # u = undoable
    # C = completeable

    if status == 'CAR' :
        if car_status == 'reserve' :
            actions.append("ci")
            status = 'RESERVED'
        elif car_status == 'in_use' :
            actions.append("uC")
            status = 'IN_USE'


    return {
        "id": x[0],
        "c_first_name" : x[1],
        "c_last_name" : x[2],
        "car_image": x[3],
        "car_plate": x[4],
        "model_brand": x[5],
        "model_model": x[6],
        "model_year": x[7],
        "model_id": x[8],
        "car_mileage": x[9],
        "start": x[10],
        "end": x[11],
        "car_id": x[12],
        "note": x[15],

        'status': status,
        "actions": ''.join(actions)
    }

@bp.route("/admin/reservation/<reservation_id>/cancel", methods=["POST"])
@admin_required()
def admin_rsv_cancel(reservation_id=0) :
    """ _ """
    # must be (CAR = reserved) (!CANCELED) (!COMPLETED)

    reason = request.args.get("reason", None)

    r = execute_sql_one(
        "SELECT `status`, a.car_status, a.car_id FROM reservations,"
        " (SELECT car_status, car_id FROM cars WHERE car_id ="
        " (SELECT car_id FROM reservations WHERE reservation_id = %s)) AS a WHERE reservation_id = %s",
        reservation_id, reservation_id
    )
    if not r :
        return {"error": "Reservation not found"}, 404
    
    if r[0] == "CANCELED" :
        return {"error": "Reservation already cancelled"}, 400
    elif r[0] == "COMPLETED" :
        return {"error": "Reservation already completed"}, 400
    elif r[0] == "CAR" :
        if r[1] != "reserve" :
            return {"error": "Car already not reserved or on service"}, 400

    params = ["CANCELED", reservation_id]
    if reason :
        params.insert(1, reason)

    commit_sqls([
        "UPDATE reservations SET status = %s"
        + (", note = %s" if reason else "") +
        "WHERE reservation_id = %s",
        "UPDATE cars SET car_status = %s"
        " WHERE car_id = %s"
    ], [
        params,
        ("not_reserve", r[2])
    ])

    return "OK"

@bp.route("/admin/reservation/<reservation_id>/inuse", methods=["POST"])
@admin_required()
def admin_rsv_inuse(reservation_id=0) :
    """ _ """
    # must be (CAR = reserved) (!CANCELED) (!COMPLETED)

    r = execute_sql_one(
        "SELECT `status`, a.car_status, a.car_id FROM reservations,"
        " (SELECT car_status, car_id FROM cars WHERE car_id ="
        " (SELECT car_id FROM reservations WHERE reservation_id = %s)) AS a WHERE reservation_id = %s",
        reservation_id, reservation_id
    )
    if not r :
        return {"error": "Reservation not found"}, 404
    
    if r[0] == "CANCELED" :
        return {"error": "Reservation already canceled"}, 400
    elif r[0] == "COMPLETED" :
        return {"error": "Reservation already completed"}, 400
    elif r[0] == "CAR" :
        if r[1] != "reserve" :
            return {"error": "Car already reserved or on service"}, 400

    commit_sqls([
        "UPDATE reservations SET status = %s"
        " WHERE reservation_id = %s",
        "UPDATE cars SET car_status = %s"
        " WHERE car_id = %s"
    ], [
        ("CAR", reservation_id),
        ("in_use", r[2])
    ])

    return "OK"

@bp.route("/admin/reservation/<reservation_id>/inuseundo", methods=["POST"])
@admin_required()
def admin_rsv_inuseundo(reservation_id=0) :
    """ _ """
    # must be (CAR = in_use) (!CANCELED) (!COMPLETED)

    r = execute_sql_one(
        "SELECT `status`, a.car_status, a.car_id FROM reservations,"
        " (SELECT car_status, car_id FROM cars WHERE car_id ="
        " (SELECT car_id FROM reservations WHERE reservation_id = %s)) AS a WHERE reservation_id = %s",
        reservation_id, reservation_id
    )
    if not r :
        return {"error": "Reservation not found"}, 404
    
    if r[0] == "CANCELED" :
        return {"error": "Reservation already canceled"}, 400
    elif r[0] == "COMPLETED" :
        return {"error": "Reservation already completed"}, 400
    elif r[0] == "CAR" :
        if r[1] != "in_use" :
            return {"error": "Car not in use"}, 400
        
    commit_sqls([
        "UPDATE reservations SET status = %s"
        " WHERE reservation_id = %s",
        "UPDATE cars SET car_status = %s"
        " WHERE car_id = %s"
    ], [
        ("CAR", reservation_id),
        ("reserve", r[2])
    ])

    return "OK"

@bp.route("/admin/reservation/<reservation_id>/complete", methods=["POST"])
@admin_required()
def admin_rsv_complete(reservation_id=0) :
    """ _ """
    # must be (CAR = in_use) (!CANCELED) (!COMPLETED)

    r = execute_sql_one(
        "SELECT `status`, a.car_status, a.car_id FROM reservations,"
        " (SELECT car_status, car_id FROM cars WHERE car_id ="
        " (SELECT car_id FROM reservations WHERE reservation_id = %s)) AS a WHERE reservation_id = %s",
        reservation_id, reservation_id
    )
    if not r :
        return {"error": "Reservation not found"}, 404
    
    if r[0] == "CANCELED" :
        return {"error": "Reservation already canceled"}, 400
    elif r[0] == "COMPLETED" :
        return {"error": "Reservation already completed"}, 400
    elif r[0] == "CAR" :
        if r[1] != "in_use" :
            return {"error": "Car not in use"}, 400
        
    commit_sqls([
        "UPDATE reservations SET status = %s"
        " WHERE reservation_id = %s",
        "UPDATE cars SET car_status = %s"
        " WHERE car_id = %s"
    ], [
        ("COMPLETED", reservation_id),
        ("not_reserve", r[2])
    ])

    return "OK"