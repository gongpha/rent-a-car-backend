""" _ """
from flask import Blueprint
from .utils.database import execute_sql, execute_sql_one, commit_sql
from .auth import admin_required, root_required, manager_required

import requests
import os
import json

from flask import redirect, request, current_app, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt

bp = Blueprint('cars', __name__)

@bp.route("/cars/<from_branch>", methods=["GET"])
def cars(from_branch=0) :
    """ รถทั้งหมด """
    base =  "SELECT car_id, brand, model, car_type, year, seats, fuel_type, price_per_day, gear,"\
    "image_car FROM cars JOIN car_models USING (model_id)"

    args = [from_branch]
    largs = []

    filter_base = " WHERE car_status = \"not_reserve\" AND branch_id = %s"
    limit = ""

    if request.args.get("carType") is not None :
        filter_base += " AND car_type = %s"
        args.append(request.args.get("carType"))

    if request.args.get("minPrice") is not None :
        filter_base += " AND price_per_day >= %s"
        args.append(request.args.get("minPrice"))

    if request.args.get("maxPrice") is not None :
        filter_base += " AND price_per_day <= %s"
        args.append(request.args.get("maxPrice"))

    if request.args.get("seats") is not None :
        filter_base += " AND seats >= %s"
        args.append(request.args.get("seats"))

    if request.args.get("fuelType") is not None :
        filter_base += " AND fuel_type = %s"
        args.append(request.args.get("fuelType"))

    if request.args.get("brand") is not None :
        filter_base += " AND brand = %s"
        args.append(request.args.get("brand"))

    try :
        if request.args.get("limit") is not None :
            limit += " LIMIT %s"
            largs.append(int(request.args.get("limit")))

            if request.args.get("offset") is not None :
                limit += " OFFSET %s"
                largs.append(int(request.args.get("offset")))
    except ValueError :
        return {"error" : "Invalid limit/offset"}, 400
    
    # filters
    filterFuels = request.args.getlist("filterFuels[]")
    if len(filterFuels) > 0 :
        filter_base += " AND fuel_type IN (" + ",".join(["%s"] * len(filterFuels)) + ")"
        args += filterFuels

    filterCarTypes = request.args.getlist("filterCarTypes[]")
    if len(filterCarTypes) > 0 :
        filter_base += " AND car_type IN (" + ",".join(["%s"] * len(filterCarTypes)) + ")"
        args += filterCarTypes

    filterGears = request.args.getlist("filterGears[]")
    if len(filterGears) > 0 :
        filter_base += " AND gear IN (" + ",".join(["%s"] * len(filterGears)) + ")"
        args += filterGears

    filterBrands = request.args.getlist("filterBrands[]")
    if len(filterBrands) > 0 :
        filter_base += " AND brand IN (" + ",".join(["%s"] * len(filterBrands)) + ")"
        args += filterBrands

    sorting = ""

    sortBy = request.args.get("sortBy")
    if sortBy is not None :
        if sortBy == "price" :
            sorting += " ORDER BY price_per_day"
        elif sortBy == "seats" :
            sorting += " ORDER BY seats"
        elif sortBy == "year" :
            sorting += " ORDER BY year"
        elif sortBy == "brand" :
            sorting += " ORDER BY brand"
        elif sortBy == "model" :
            sorting += " ORDER BY model"
        else :
            return {"error" : "Invalid sortBy"}, 400

        if request.args.get("sortDesc") is not None :
            sorting += " DESC"

    results = execute_sql(
        base + filter_base + sorting + limit,
        *(args + largs)
    )

    count = execute_sql_one(
        "SELECT COUNT(*) FROM cars JOIN car_models USING (model_id)" + filter_base,
        *args
    )
    return {
        'total' : count[0],
        'cars' : [{
            "car_id" : x[0],
            "brand" : x[1],
            "model" : x[2],
            "car_type" : x[3],
            "year" : x[4],
            "seats" : x[5],
            "fuel_type" : x[6],
            "price_per_day" : x[7],
            "gear" : x[8],
            "car_image" : x[9]
        } for x in results]
    }

@bp.route("/priceshist/<branch_id>", methods=["GET"])
def priceshist(branch_id=0) :
    """ ราคาทั้งหมดสำหรับการค้นหา """
    results = execute_sql(
        "SELECT price_per_day, COUNT(price_per_day) FROM ("
        " SELECT price_per_day FROM cars"
        " JOIN car_models USING (model_id)"
        " WHERE branch_id = %s"
        " ) a"
        " GROUP BY price_per_day",
        branch_id
    )

    return list(results)

@bp.route("/brandlist", methods=["GET"])
def brandlist() :   
    """ ยี่ห้อทั้งหมดสำหรับการค้นหา """
    results = [x[0] for x in execute_sql(
        "SELECT DISTINCT brand FROM cars JOIN car_models USING (model_id)"
    )]

    return list(results)

@bp.route("/car/<car_id>", methods=["GET"])
def car(car_id=0) :
    """ รถ """

    x = execute_sql_one(
        "SELECT car_id, license_plate, brand, model, car_type, year, seats, fuel_type, price_per_day, gear,"\
        "image_car, car_status FROM cars JOIN car_models USING (model_id) WHERE car_id = %s", car_id
    )
    if not x :
        return {"error" : "Car not found"}, 404
    return {
        "car_id" : x[0],
        "license_plate" : x[1],
        "brand" : x[2],
        "model" : x[3],
        "car_type" : x[4],
        "year" : x[5],
        "seats" : x[6],
        "fuel_type" : x[7],
        "price_per_day" : x[8],
        "gear" : x[9],
        "car_image" : x[10],
        "car_status" : x[11]
    }

@bp.route("/admin/cars", methods=["GET"])
@admin_required()
def admin_cars() :
    """ รถทั้งหมด (มุมมองของพนักงาน) """
    if get_jwt()["role"] == "ROOT" :
        return [] # use admin_cars_branch
    username = get_jwt_identity()
    results = execute_sql(
        "SELECT"
        " car_id, license_plate, mileage, brand, model, car_type, year, seats, fuel_type, price_per_day, gear, image_car, car_status"
        " FROM cars JOIN car_models USING (model_id) WHERE branch_id = ("
        " SELECT branch_id FROM employees WHERE employee_id = ("
        " SELECT employee_id FROM web_accounts_emp WHERE username = %s"
        " )"
        " )", username
    )
    return [{
        "car_id" : x[0],
        "license_plate" : x[1],
        "mileage" : x[2],
        "brand" : x[3],
        "model" : x[4],
        "car_type" : x[5],
        "year" : x[6],
        "seats" : x[7],
        "fuel_type" : x[8],
        "price_per_day" : x[9],
        "gear" : x[10],
        "image_car" : x[11],
        "car_status" : x[12]
    } for x in results]

@bp.route("/admin/cars/<from_branch>", methods=["GET"])
@root_required()
def admin_cars_branch(from_branch=0) :
    """ รถทั้งหมดตามสาขา (มุมมองของพนักงาน) """
    results = execute_sql(
        "SELECT"
        " car_id, license_plate, mileage, brand, model, car_type, year, seats, fuel_type, price_per_day, gear, image_car, car_status"
        " FROM cars JOIN car_models USING (model_id) WHERE branch_id = %s", from_branch
    )
    return [{
        "car_id" : x[0],
        "license_plate" : x[1],
        "mileage" : x[2],
        "brand" : x[3],
        "model" : x[4],
        "car_type" : x[5],
        "year" : x[6],
        "seats" : x[7],
        "fuel_type" : x[8],
        "price_per_day" : x[9],
        "gear" : x[10],
        "image_car" : x[11],
        "car_status" : x[12]
    } for x in results]

@bp.route("/admin/car/<car_id>", methods=["GET"])
@admin_required()
def admin_car(car_id=0) :
    """ รถ (มุมมองของพนักงาน) """

    if get_jwt()["role"] == "ROOT" :
        x = execute_sql_one(
            "SELECT"
            " c.car_id, c.license_plate, c.mileage, c.image_car, gear, c.car_status, c.model_id, brand, model, year, r.reservation_id"
            " FROM cars c"
            " JOIN car_models USING (model_id)"
            " LEFT JOIN reservations r ON (r.status = \"CAR\" AND r.reservation_id = c.car_id)"
            " WHERE c.car_id = %s LIMIT 1", car_id
        )
    else :
        x = execute_sql_one(
            "SELECT"
            " c.car_id, c.license_plate, c.mileage, c.image_car, gear, c.car_status, c.model_id, brand, model, year, r.reservation_id"
            " FROM cars c"
            " JOIN car_models USING (model_id)"
            " LEFT JOIN reservations r ON (r.status = \"CAR\" AND r.reservation_id = c.car_id)"
            " WHERE c.car_id = %s AND branch_id = ("
            " SELECT branch_id FROM employees WHERE employee_id = ("
            " SELECT employee_id FROM web_accounts_emp WHERE username = %s"
            " )"
            " ) LIMIT 1", car_id, get_jwt_identity()
        )
    if not x :
        return {"error" : "Car not found"}, 404
    
    r = execute_sql_one(
        "SELECT COUNT(*) FROM reservations"
        " JOIN cars USING (car_id)"
        " WHERE car_id = %s AND `status` = \"CAR\" AND car_status = \"reserve\"",
        car_id
    )

    p = dump_car_permission(r[0] == 0)

    return {
        "car_id" : x[0],
        "license_plate" : x[1],
        "mileage" : x[2],
        "image_car" : x[3],
        "gear" : x[4],
        "car_status" : x[5],
        "model_id" : x[6],
        "brand" : x[7],
        "model" : x[8],
        "year" : x[9],
        "reservation_id" : x[10],

        # mutating
        "permissions" : p
    }

CAN_ADD = ["MANAGER", "ROOT"]
CAN_DELETE = ["MANAGER", "ROOT"]
CAN_UPDATE = ["MANAGER", "ROOT"]

M_CAN_ADD = ["ROOT"]
M_CAN_DELETE = ["ROOT"]
M_CAN_UPDATE = ["ROOT"]

def dump_car_permission(can_edit_status : bool) :
    return (
        ("A" if get_jwt()["role"] in CAN_ADD else "") +
        ("D" if get_jwt()["role"] in CAN_DELETE else "") +
        ("U" if get_jwt()["role"] in CAN_UPDATE else "") +
        ("s" if can_edit_status else "")
    )

def dump_model_permission() :
    return (
        ("A" if get_jwt()["role"] in M_CAN_ADD else "") +
        ("D" if get_jwt()["role"] in M_CAN_DELETE else "") +
        ("U" if get_jwt()["role"] in M_CAN_UPDATE else "")
    )

@bp.route("/admin/models", methods=["GET"])
@admin_required()
def admin_models() :
    """ รุ่นรถทั้งหมด (มุมมองของพนักงาน) """
    results = execute_sql(
        "SELECT"
        " model_id, brand, model, car_type, year, seats, fuel_type, price_per_day, gear,"
        " COUNT(car_id) AS \"count\" FROM car_models"
        " LEFT JOIN cars USING (model_id)"
        " GROUP BY model_id"
    )
    return {
        'models' : [{
            "model_id" : x[0],
            "brand" : x[1],
            "model" : x[2],
            "car_type" : x[3],
            "year" : x[4],
            "seats" : x[5],
            "fuel_type" : x[6],
            "price_per_day" : x[7],
            "gear" : x[8],
            "count" : x[9],
        } for x in results],
        "permissions" : dump_model_permission()
    }

@bp.route("/admin/model/<model_id>", methods=["GET"])
@admin_required()
def admin_model(model_id=0) :
    """ รุ่นรถ (มุมมองของพนักงาน) """
    x = execute_sql_one(
        "SELECT"
        " model_id, brand, model, car_type, year, seats, fuel_type, price_per_day, gear,"
        " COUNT(car_id) AS \"count\" FROM car_models"
        " LEFT JOIN cars USING (model_id)"
        " WHERE model_id = %s"
        " GROUP BY model_id", model_id
    )
    return {
        "model_id" : x[0],
        "brand" : x[1],
        "model" : x[2],
        "car_type" : x[3],
        "year" : x[4],
        "seats" : x[5],
        "fuel_type" : x[6],
        "price_per_day" : x[7],
        "gear" : x[8],
        "count" : x[9],

        # mutating
        "permissions" : dump_model_permission()
    }

def new_car_data(data, sqlimg, sqlnoimg, target, msg, can_edit_status) :
    if not data :
        return {"error" : "Invalid data"}, 400
    
    mileage = data["mileage"]
    car_status = data["car_status"]
    license_plate = data["license_plate"]
    model_id = data["model_id"]

    r = execute_sql_one(
        "SELECT COUNT(*) FROM reservations"
        " JOIN cars USING (car_id)"
        " WHERE car_id = %s AND `status` = \"CAR\" AND car_status = \"reserve\"",
        target
    )

    if r[0] == 0 and not can_edit_status :
        return {"error" : "Car status cannot be edited"}, 400

    if not mileage.isdigit() or not car_status or not license_plate or not model_id :
        return {"error" : "Invalid data"}, 400
    
    if int(mileage) < 0 :
        return {"error" : "Invalid mileage"}, 400
    
    if car_status not in ["not_reserve", "reserve", "in_use", "unavailable"] :
        return {"error" : "Invalid car status"}, 400

    if "mileage" not in data or "car_status" not in data or "license_plate" not in data or "model_id" not in data :
        return {"error" : "Invalid data"}, 400
    
    img = request.files.get("img", None)
    if img :
        files = {
            "files[0]" : (img.filename, img.stream, img.mimetype)
        }

        jsond = json.dumps({"content":license_plate, "embeds":None})

        r = requests.post(os.getenv("DISCORD_UPLOAD_WEBHOOK"), files=files, data={
            "payload_json" : jsond
        })

        commit_sql(
            sqlimg,
            r.json()["attachments"][0]["url"], mileage, car_status, license_plate, model_id, target
        )
    else :
        commit_sql(
            sqlnoimg,
            mileage, car_status, license_plate, model_id, target
        )
    return {"message" : msg}

@bp.route("/admin/edit/car/<car_id>", methods=["POST"])
@admin_required()
def admin_edit_car(car_id=0) :
    """ แก้ไขข้อมูลรถ (มุมมองของพนักงาน) """

    r = execute_sql_one(
        "SELECT COUNT(*) FROM reservations"
        " JOIN cars USING (car_id)"
        " WHERE car_id = 1 AND `status` = \"CAR\" AND car_status = \"reserve\""
    )

    data = request.form
    return new_car_data(
        data,
        "UPDATE cars SET image_car = %s, mileage = %s, car_status = %s, license_plate = %s, model_id = %s WHERE car_id = %s",
        "UPDATE cars SET mileage = %s, car_status = %s, license_plate = %s, model_id = %s WHERE car_id = %s",
        car_id,
        "Car updated",
        r[0] == 0
    )

@bp.route("/admin/add/car/<branch_id>", methods=["POST"])
@root_required()
def admin_add_car(branch_id=0) :
    """ เพิ่มข้อมูลรถ (มุมมองของพนักงาน) """

    data = request.form
    return new_car_data(
        data,
        "INSERT INTO cars (image_car, mileage, car_status, license_plate, model_id, branch_id)"
        " VALUES (%s, %s, %s, %s, %s, %s)",
        "INSERT INTO cars (mileage, car_status, license_plate, model_id, branch_id)"
        " VALUES (%s, %s, %s, %s, %s)",
        branch_id,
        "Car added",
        True
    )

@bp.route("/admin/delete/car/<car_id>", methods=["DELETE"])
@root_required()
def admin_delete_car(car_id=0) :
    """ ลบข้อมูลรถ (มุมมองของพนักงาน) """

    commit_sql(
        "DELETE FROM cars WHERE car_id = %s", car_id
    )
    return {"message" : "Car deleted"}

@bp.route("/admin/edit/model/<model_id>", methods=["POST"])
@root_required()
def admin_edit_model(model_id=0) :
    """ แก้ไขข้อมูลรุ่นรถ (มุมมองของพนักงาน) """

    data = request.get_json()
    return new_car_model_data(
        data,
        "UPDATE car_models SET brand = %s, model = %s, car_type = %s, year = %s, seats = %s, fuel_type = %s, price_per_day = %s, gear = %s WHERE model_id = %s",
        model_id,
        "Model updated"
    )

@bp.route("/admin/add/model", methods=["POST"])
@root_required()
def admin_add_model() :
    """ เพิ่มข้อมูลรุ่นรถ (มุมมองของพนักงาน) """

    data = request.get_json()
    return new_car_model_data(
        data,
        "INSERT INTO car_models (brand, model, car_type, year, seats, fuel_type, price_per_day, gear)"
        " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        None,
        "Model added"
    )

@bp.route("/admin/delete/model/<model_id>", methods=["DELETE"])
@root_required()
def admin_delete_model(model_id=0) :
    """ ลบข้อมูลรุ่นรถ (มุมมองของพนักงาน) """

    count = execute_sql_one(
        "SELECT"
        " COUNT(car_id) FROM car_models"
        " LEFT JOIN cars USING (model_id)"
        " WHERE model_id = %s"
        " GROUP BY model_id"
    , model_id)

    if count[0] != 0 :
        return {"error" : "Model is in use"}, 400

    commit_sql(
        "DELETE FROM car_models WHERE model_id = %s", model_id
    )
    return {"message" : "Model deleted"}

def new_car_model_data(data, sql, target, msg) :
    if not data :
        return {"error" : "Invalid data"}, 400

    if "brand" not in data or "model" not in data or "car_type" not in data or "year" not in data or "seats" not in data or "fuel_type" not in data or "price_per_day" not in data or "gear" not in data :
        return {"error" : "Invalid data"}, 400

    params = [
        data["brand"], data["model"], data["car_type"], data["year"], data["seats"], data["fuel_type"], data["price_per_day"], data["gear"]
    ]

    if target :
        params.append(target)

    commit_sql(
        sql,
        *params
    )
    return {"message" : msg}