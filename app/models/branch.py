""" car model """
from app.utils.database import execute_sql_one, commit_sql

class Branch() :
    """ car model """
    def __init__(self, id_, name, location) :
        self.id = id_
        self.name = name
        self.location = location

    @staticmethod
    def get(branch_id) :
        """ get a branch info by id """
        branch = execute_sql_one(
            "SELECT * FROM branches WHERE branch_id = %s", branch_id
        )
        if not branch :
            return None # bro
        
        branch = Branch(
            id_=branch[0],
            name=branch[1],
            location=branch[2]
        )
        return branch