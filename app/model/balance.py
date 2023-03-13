from .base import BaseModel, CustomUUID

import sqlalchemy as sa

class BalanceModel(BaseModel):
  __tablename__ = "balance"
  
  employee_id = sa.Column(CustomUUID(as_uuid=True), sa.ForeignKey("employee.id", ondelete="cascade"))
  vacation_type_id = sa.Column(CustomUUID(as_uuid=True), sa.ForeignKey("vacation_type.id", ondelete="cascade"))
  amount = sa.Column(sa.Integer, nullable=False)
  
  __table_args__ = (
    sa.UniqueConstraint("employee_id", "vacation_type_id"),
  )