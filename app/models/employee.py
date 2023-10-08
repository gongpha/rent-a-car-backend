""" employee model """
from app.utils.database import execute_sql_one

class Employee() :
    """ customer model """
    def __init__(self, id_, first_name, last_name, email, phone, manager_id, branch_id, role) :
        self.id = id_
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.manager_id = manager_id
        self.branch_id = branch_id
        self.role = role

    @staticmethod
    def get(emp_id) :
        """ get a customer by id """
        emp = execute_sql_one(
            "SELECT * FROM employees WHERE employee_id = %s", emp_id
        )
        if not emp :
            return None
        
        emp = Employee(
            id_=emp[0],
            first_name=emp[1],
            last_name=emp[2],
            email=emp[3],
            phone=emp[4],
            manager_id=emp[5],
            branch_id=emp[6],
            role=emp[7]
        )
        return emp