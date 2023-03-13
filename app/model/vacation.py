from .base import BaseModel, CustomUUID
import enum
import sqlalchemy as sa

# from .vacation_types import VacationTypes

class VacationModel(BaseModel):
  __tablename__ = "vacation"
  
  employee_id = sa.Column(CustomUUID(as_uuid=True), sa.ForeignKey("employee.id", ondelete="cascade"))
  vacation_type_id = sa.Column(CustomUUID(as_uuid=True), sa.ForeignKey("vacation_type.id", ondelete="cascade"))
  start_date = sa.Column(sa.Date, nullable=False)
  end_date = sa.Column(sa.Date, nullable=False)
  
  __table_args__ = (
    sa.CheckConstraint("start_date <= end_date"),
  )
  
  