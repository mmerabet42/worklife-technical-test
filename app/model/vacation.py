from .base import BaseModel, CustomUUID
import enum
import sqlalchemy as sa

class VacationTypes(enum.Enum):
  paid_leave = "paid_leave"
  unpaid_leave = "unpaid_leave"

class VacationModel(BaseModel):
  __tablename__ = "vacation"
  
  employee_id = sa.Column(CustomUUID(as_uuid=True), sa.ForeignKey("employee.id"))
  vacation_type = sa.Column(sa.Enum(VacationTypes), nullable=False)
  start_date = sa.Column(sa.Date, nullable=False)
  end_date = sa.Column(sa.Date, nullable=False)
  
  