from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from app.model.employee import EmployeeModel


class EmployeeSchema(sqlalchemy_to_pydantic(EmployeeModel)):
    ...

class EmployeeWithoutIdSchema(sqlalchemy_to_pydantic(EmployeeModel, exclude=["id"])):
    ...
