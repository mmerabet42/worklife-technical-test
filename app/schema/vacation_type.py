from typing import List
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from app.model.vacation_type import VacationTypeModel
from app.schema.vacation import VacationSchema
from app.schema.balance import BalanceSchema

class VacationTypeSchema(sqlalchemy_to_pydantic(VacationTypeModel)):
  ...
  

class VacationTypeWithRelationshipSchema(sqlalchemy_to_pydantic(VacationTypeModel)):
  vacations: List[VacationSchema] = []
  balances: List[BalanceSchema] = []
  ...  

  
class VacationTypeWithoutIdSchema(sqlalchemy_to_pydantic(VacationTypeModel, exclude=["id"])):
  ...