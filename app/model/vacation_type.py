import sqlalchemy as sa

from .base import BaseModel
from .vacation import VacationModel
from .balance import BalanceModel

class VacationTypeModel(BaseModel):
  __tablename__ = "vacation_type"
  
  name = sa.Column(sa.String, nullable=False, unique=True)
  vacations = sa.orm.relationship(
    VacationModel.__name__,
    backref=__tablename__,
    cascade="all, delete",
   	passive_deletes=True
  )
  balances = sa.orm.relationship(
    BalanceModel.__name__,
    backref=__tablename__,
    cascade="all, delete",
   	passive_deletes=True
  )

# class VacationTypes(enum.Enum):
#   paid_leave = "paid_leave"
#   unpaid_leave = "unpaid_leave"
  