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
    
    @staticmethod
    def get_all() :
        """ get all branch """
        branches = execute_sql_one("SELECT * FROM branches")
        if not branches :
            return None # bro
        
        branches = [Branch(
            id_=branch[0],
            name=branch[1],
            location=branch[2]
        ) for branch in branches]
        return branches
    
    @staticmethod
    def create(name, location) :
        """ create a branch """
        commit_sql(
            "INSERT INTO branches (name, location) VALUES (%s, %s)",
            (name, location)
        )

    @staticmethod
    def update(branch_id, name, location) :
        """ update a branch """
        commit_sql(
            "UPDATE branches SET name = %s, location = %s WHERE branch_id = %s",
            (name, location, branch_id)
        )

    @staticmethod
    def delete(branch_id) :
        """ delete a branch """
        commit_sql(
            "DELETE FROM branches WHERE branch_id = %s",
            branch_id
        )

    @staticmethod
    def get_branch_by_name(name) :
        """ get branch by name """
        branch = execute_sql_one(
            "SELECT * FROM branches WHERE name = %s", name
        )
        if not branch :
            return None # bro
        
        branch = Branch(
            id_=branch[0],
            name=branch[1],
            location=branch[2]
        )
        return branch
    
    @staticmethod
    def get_branch_by_location(location) :
        """ get branch by location """
        branch = execute_sql_one(
            "SELECT * FROM branches WHERE location = %s", location
        )
        if not branch :
            return None # bro
        
        branch = Branch(
            id_=branch[0],
            name=branch[1],
            location=branch[2]
        )
        return branch
    
    @staticmethod
    def get_branch_by_name_and_location(name, location) :
        """ get branch by name and location """
        branch = execute_sql_one(
            "SELECT * FROM branches WHERE name = %s AND location = %s", (name, location)
        )
        if not branch :
            return None # bro
        
        branch = Branch(
            id_=branch[0],
            name=branch[1],
            location=branch[2]
        )
        return branch