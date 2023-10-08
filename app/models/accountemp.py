""" account model """
from .employee import Employee
from app.utils.database import execute_sql_one, commit_sql

class AccountEmp() :
    """ customer model """
    def __init__(self, id_, employee, username, password_md5) :
        self.id = id_
        self.employee = employee
        self.username = username
        self.password_md5 = password_md5

    @staticmethod
    def get(acc_id) :
        acc = execute_sql_one(
            "SELECT * FROM employees JOIN web_accounts_emp USING (employee_id) WHERE accemp_id = %s", acc_id
        )
        if not acc :
            return None # bro
        
        return AccountEmp(
            id_=acc[8],
            username=acc[9],
            password_md5=acc[10],
            employee=Employee(
                id_=acc[0],
                first_name=acc[1],
                last_name=acc[2],
                email=acc[3],
                phone=acc[4],
                manager_id=acc[5],
                branch_id=acc[6],
                role=acc[7]
            )
        )
    
    @staticmethod
    def get_by_username(username) :
        acc = execute_sql_one(
            "SELECT * FROM employees JOIN web_accounts_emp USING (employee_id) WHERE username = %s"
            , username
        )
        if not acc :
            return None # bro
        
        return AccountEmp(
            id_=acc[8],
            username=acc[9],
            password_md5=acc[10],
            employee=Employee(
                id_=acc[0],
                first_name=acc[1],
                last_name=acc[2],
                email=acc[3],
                phone=acc[4],
                manager_id=acc[5],
                branch_id=acc[6],
                role=acc[7]
            )
        )