""" employee model """
from app.utils.database import execute_sql_one, commit_sql

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
    
    @staticmethod
    def get_by_email(email) :
        emp = execute_sql_one(
            "SELECT * FROM employees WHERE e_email = %s"
            , email
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
    
    @staticmethod
    def create(first_name, last_name, email, phone, manager_id, branch_id, role) :
        """ create a new customer """
        commit_sql(
            "INSERT INTO employees"
            "(e_first_name, e_last_name, e_email, e_phone_number, manager_id, branch_id, role)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s);",
            first_name, last_name, email, phone, manager_id, branch_id, role
        )

    @staticmethod
    def update(emp_id, first_name, last_name, email, phone, manager_id, branch_id, role) :
        """ update a customer """
        commit_sql(
            "UPDATE employees SET e_first_name = %s, e_last_name = %s, e_email = %s, e_phone_number = %s, manager_id = %s, branch_id = %s, role = %s WHERE employee_id = %s",
            (first_name, last_name, email, phone, manager_id, branch_id, role, emp_id)
        )

    @staticmethod
    def delete(emp_id) :
        """ delete a customer """
        commit_sql(
            "DELETE FROM employees WHERE employee_id = %s",
            emp_id
        )

    @staticmethod
    def get_all() :
        """ get all customer """
        emps = execute_sql_one("SELECT * FROM employees")
        if not emps :
            return None
        
        emps = [Employee(
            id_=emp[0],
            first_name=emp[1],
            last_name=emp[2],
            email=emp[3],
            phone=emp[4],
            manager_id=emp[5],
            branch_id=emp[6],
            role=emp[7]
        ) for emp in emps]
        return emps
    
    @staticmethod
    def get_by_branch_id(branch_id) :
        """ get all customer """
        emps = execute_sql_one("SELECT * FROM employees WHERE branch_id = %s", branch_id)
        if not emps :
            return None
        
        emps = [Employee(
            id_=emp[0],
            first_name=emp[1],
            last_name=emp[2],
            email=emp[3],
            phone=emp[4],
            manager_id=emp[5],
            branch_id=emp[6],
            role=emp[7]
        ) for emp in emps]
        return emps
    
    @staticmethod
    def get_by_manager_id(manager_id) :
        """ get all customer """
        emps = execute_sql_one("SELECT * FROM employees WHERE manager_id = %s", manager_id)
        if not emps :
            return None
        
        emps = [Employee(
            id_=emp[0],
            first_name=emp[1],
            last_name=emp[2],
            email=emp[3],
            phone=emp[4],
            manager_id=emp[5],
            branch_id=emp[6],
            role=emp[7]
        ) for emp in emps]
        return emps
    
    @staticmethod
    def get_by_name(first_name, last_name) :
        """ get all customer """
        emps = execute_sql_one("SELECT * FROM employees WHERE e_first_name = %s AND e_last_name = %s", (first_name, last_name))
        if not emps :
            return None
        
        emps = [Employee(
            id_=emp[0],
            first_name=emp[1],
            last_name=emp[2],
            email=emp[3],
            phone=emp[4],
            manager_id=emp[5],
            branch_id=emp[6],
            role=emp[7]
        ) for emp in emps]
        return emps
    
    @staticmethod
    def get_by_name_and_email(first_name, last_name, email) :
        """ get all customer """
        emps = execute_sql_one("SELECT * FROM employees WHERE e_first_name = %s AND e_last_name = %s AND e_email = %s", (first_name, last_name, email))
        if not emps :
            return None
        
        emps = [Employee(
            id_=emp[0],
            first_name=emp[1],
            last_name=emp[2],
            email=emp[3],
            phone=emp[4],
            manager_id=emp[5],
            branch_id=emp[6],
            role=emp[7]
        ) for emp in emps]
        return emps
    
    @staticmethod
    def get_by_name_and_phone(first_name, last_name, phone) :
        """ get all customer """
        emps = execute_sql_one("SELECT * FROM employees WHERE e_first_name = %s AND e_last_name = %s AND e_phone_number = %s", (first_name, last_name, phone))
        if not emps :
            return None
        
        emps = [Employee(
            id_=emp[0],
            first_name=emp[1],
            last_name=emp[2],
            email=emp[3],
            phone=emp[4],
            manager_id=emp[5],
            branch_id=emp[6],
            role=emp[7]
        ) for emp in emps]
        return emps
    
    @staticmethod
    def get_by_name_and_manager_id(first_name, last_name, manager_id) :
        """ get all customer """
        emps = execute_sql_one("SELECT * FROM employees WHERE e_first_name = %s AND e_last_name = %s AND manager_id = %s", (first_name, last_name, manager_id))
        if not emps :
            return None
        
        emps = [Employee(
            id_=emp[0],
            first_name=emp[1],
            last_name=emp[2],
            email=emp[3],
            phone=emp[4],
            manager_id=emp[5],
            branch_id=emp[6],
            role=emp[7]
        ) for emp in emps]
        return emps
    
    @staticmethod
    def get_by_name_and_branch_id(first_name, last_name, branch_id) :
        """ get all customer """
        emps = execute_sql_one("SELECT * FROM employees WHERE e_first_name = %s AND e_last_name = %s AND branch_id = %s", (first_name, last_name, branch_id))
        if not emps :
            return None
        
        emps = [Employee(
            id_=emp[0],
            first_name=emp[1],
            last_name=emp[2],
            email=emp[3],
            phone=emp[4],
            manager_id=emp[5],
            branch_id=emp[6],
            role=emp[7]
        ) for emp in emps]
        return emps