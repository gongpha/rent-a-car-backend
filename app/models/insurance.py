""" insurance """
from app.utils.database import execute_sql_one, commit_sql, execute_sql

class Insurance() :
    def __init__(self,
        insurance_id,
        insurance_type,

        bodily_injury,
        vehicle_damage,
        property_damage,
        thief_fire,

        description,
        cost_per_day
    ) :
        self.insurance_id = insurance_id
        self.insurance_type = insurance_type

        self.bodily_injury = bodily_injury
        self.vehicle_damage = vehicle_damage
        self.property_damage = property_damage
        self.thief_fire = thief_fire

        self.description = description
        self.cost_per_day = cost_per_day

    @staticmethod
    def get_insurance(insurance_id) :
        insurance = execute_sql_one(
            "SELECT * FROM insurance WHERE insurance_id = %s", insurance_id
        )
        if not insurance :
            return None # bro
        
        insurance = Insurance(
            insurance_id=insurance[0],
            insurance_type=insurance[1],

            bodily_injury=insurance[2],
            vehicle_damage=insurance[3],
            property_damage=insurance[4],
            thief_fire=insurance[5],

            description=insurance[6],
            cost_per_day=insurance[7]
        )
        return insurance
    
    @staticmethod
    def get_all() :
        insurances = execute_sql("SELECT * FROM insurance")
        if not insurances :
            return None # bro
        
        insurances = [Insurance(
            insurance_id=insurance[0],
            insurance_type=insurance[1],

            bodily_injury=insurance[2],
            vehicle_damage=insurance[3],
            property_damage=insurance[4],
            thief_fire=insurance[5],

            description=insurance[6],
            cost_per_day=insurance[7]
        ) for insurance in insurances]
        return insurances
    
    @staticmethod
    def create(
        insurance_type,

        bodily_injury,
        vehicle_damage,
        property_damage,
        thief_fire,

        description,
        cost_per_day
    ) :
        commit_sql(
            "INSERT INTO insurance"
            "(insurance_type, bodily_injury, vehicle_damage, property_damage, thief_fire, description, cost_per_day)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s);",
            insurance_type, bodily_injury, vehicle_damage, property_damage, thief_fire, description, cost_per_day
        )

        