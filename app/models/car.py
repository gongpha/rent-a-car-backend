""" car model """
from app.utils.database import execute_sql_one, commit_sql

class CarModel() :
    """ car model """
    def __init__(self, id_, name) :
        self.id = id_
        self.name = name

    def get_car_model_by_id(self, id_) :
        """ get car model by id """
        sql = "SELECT * FROM car_model WHERE id = %s"
        return execute_sql_one(sql, (id_,))

    def get_all_car_model(self) :
        """ get all car model """
        sql = "SELECT * FROM car_model"
        return execute_sql_one(sql)

    def update_car_model_by_id(self, id_, name) :
        """ update car model by id """
        sql = "UPDATE car_model SET name = %s WHERE id = %s"
        commit_sql(sql, (name, id_))

    def delete_car_model_by_id(self, id_) :
        """ delete car model by id """
        sql = "DELETE FROM car_model WHERE id = %s"
        commit_sql(sql, (id_,))

    def create_car_model(self, name) :
        """ create car model """
        sql = "INSERT INTO car_model (name) VALUES (%s)"
        commit_sql(sql, (name,))

class CarInformation() :
    """ car info """
    def __init__(self, id_, model, branch_id, license_plate, mileage, car_status) :
        self.id = id_
        self.model = model
        self.branch_id = branch_id
        self.license_plate = license_plate
        self.mileage = mileage
        self.car_status = car_status

    def get_car_by_id(self, id_) :
        """ get car by id """
        sql = "SELECT * FROM car_information WHERE id = %s"
        return execute_sql_one(sql, (id_,))

    def get_car_by_branch_id(self, branch_id) :
        """ get car by branch id """
        sql = "SELECT * FROM car_information WHERE branch_id = %s"
        return execute_sql_one(sql, (branch_id,))

    def get_car_by_license_plate(self, license_plate) :
        """ get car by license plate """
        sql = "SELECT * FROM car_information WHERE license_plate = %s"
        return execute_sql_one(sql, (license_plate,))

    def get_all_car(self) :
        """ get all car """
        sql = "SELECT * FROM car_information"
        return execute_sql_one(sql)

    def update_car_by_id(self, id_, model, branch_id, license_plate, mileage, car_status, color) :
        """ update car by id """
        sql = "UPDATE car_information SET model = %s, branch_id = %s, license_plate = %s, mileage = %s, car_status = %s, color = %s WHERE id = %s"
        commit_sql(sql, (model, branch_id, license_plate, mileage, car_status, color, id_))

    def delete_car_by_id(self, id_) :
        """ delete car by id """
        sql = "DELETE FROM car_information WHERE id = %s"
        commit_sql(sql, (id_,))

    def create_car(self, model, branch_id, license_plate, mileage, car_status, color) :
        """ create car """
        sql = "INSERT INTO car_information (model, branch_id, license_plate, mileage, car_status, color) VALUES (%s, %s, %s, %s, %s, %s)"
        commit_sql(sql, (model, branch_id, license_plate, mileage, car_status, color))
        