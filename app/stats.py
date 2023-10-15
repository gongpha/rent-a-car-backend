""" _ """
from flask import Blueprint
from .utils.database import execute_sql, execute_sql_one, commit_sql

bp = Blueprint('stats', __name__)

# fixme : admin only

@bp.route("/stats/monthly")
def monthly() :
    res = execute_sql(
        "SELECT MONTHNAME(created), COUNT(*) FROM reservations"
        " JOIN cars USING (car_id)"
        " JOIN car_models USING (model_id)"
        " GROUP BY MONTH(created)"
    )

    return {
        "labels": [row[0] for row in res],
        "data": [row[1] for row in res]
    }

@bp.route("/stats/weekly")
def weekly() :
    res = execute_sql(
        "SELECT WEEKDAY(created), COUNT(*) FROM reservations"
        " JOIN cars USING (car_id)"
        " JOIN car_models USING (model_id)"
        " GROUP BY WEEKDAY(created)"
    )

    return {
        "labels": [row[0] for row in res],
        "data": [row[1] for row in res]
    }

@bp.route("/stats/brands")
def brands() :
    res = execute_sql(
        "SELECT brand, COUNT(*) FROM reservations"
        " JOIN cars USING (car_id)"
        " JOIN car_models USING (model_id)"
        " GROUP BY brand"
    )

    return {
        "labels": [row[0] for row in res],
        "data": [row[1] for row in res]
    }

@bp.route("/stats/models")
def models() :
    res = execute_sql(
        "SELECT model, COUNT(*) FROM reservations"
        " JOIN cars USING (car_id)"
        " JOIN car_models USING (model_id)"
        " GROUP BY model"
    )

    return {
        "labels": [row[0] for row in res],
        "data": [row[1] for row in res]
    }

@bp.route("/stats/years")
def years() :
    res = execute_sql(
        "SELECT YEAR(created), COUNT(*) FROM reservations"
        " JOIN cars USING (car_id)"
        " JOIN car_models USING (model_id)"
        " GROUP BY YEAR(created)"
    )

    return {
        "labels": [row[0] for row in res],
        "data": [row[1] for row in res]
    }