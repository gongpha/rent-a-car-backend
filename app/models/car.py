""" car model """
from app.utils.database import execute_sql_one, commit_sql

class Car() :
    """ car model """
    def __init__(self, id_, model_id, branch_id, license_plate, mileage, car_status, color) :
        self.id = id_
        self.model_id = model_id
        self.branch_id = branch_id
        self.license_plate = license_plate
        self.mileage = mileage
        self.car_status = car_status