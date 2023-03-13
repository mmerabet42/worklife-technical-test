from typing import List
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from app.model.employee import EmployeeModel
from app.schema.vacation import VacationSchema
from app.schema.balance import BalanceSchema


class EmployeeSchema(sqlalchemy_to_pydantic(EmployeeModel)):
    ...


class EmployeeWithRelationshipSchema(sqlalchemy_to_pydantic(EmployeeModel)):
    vacations: List[VacationSchema] = []
    vacations: List[BalanceSchema] = []
    ...



class EmployeeWithoutIdSchema(sqlalchemy_to_pydantic(EmployeeModel, exclude=["id"])):
    ...
