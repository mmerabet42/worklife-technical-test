from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from app.model.balance import BalanceModel

class BalanceSchema(sqlalchemy_to_pydantic(BalanceModel)):
  ...
  
class BalanceWithoutIdSchema(sqlalchemy_to_pydantic(BalanceModel, exclude=["id"])):
  ...