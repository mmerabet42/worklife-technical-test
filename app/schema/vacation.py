from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from app.model.vacation import VacationModel

class VacationSchema(sqlalchemy_to_pydantic(VacationModel)):
  ...
  
class VacationWithoutIdSchema(sqlalchemy_to_pydantic(VacationModel, exclude=["id"])):
  ...