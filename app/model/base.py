import uuid as uid

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import as_declarative

class CustomUUID(postgresql.UUID):
  python_type = uid.UUID

@as_declarative()
class BaseModel:
  id = Column(
    CustomUUID(as_uuid=True),
    primary_key=True,
    index=True,
    default=uid.uuid4,
  )

  def __str__(self):
    columns = ' '.join([f'{k}={getattr(self, k)}' for k in self.__table__.columns.keys()])
    return f"<#{self.__class__.__name__}: {columns}>"
